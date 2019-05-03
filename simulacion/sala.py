# coding=utf-8
import random
import numpy as np
import datetime
from estudiantes import Afectado, NoAfectado, Vulnerable
from collections import defaultdict
import json
import pandas as pd


class Sala:
    def __init__(self):
        self.asientos = []
        self.afectados = []
        self.estudiantes = []
        self.vulnerables = []

        for j in range(8):
            for i in range(11):
                if i != 3 and i != 7 and j % 2 == 0:
                    self.asientos.append((i + 1, j + 1))
        self.crear_alumnos()
        self.ordenar_alumnos()
        # self.hora = datetime.timedelta(hours=8, minutes=30)
        # self.tiempo_incremento = datetime.timedelta(minutes=1)
        # self.dia_incremento = datetime.timedelta(days=1)
        self.hora = pd.Timestamp(year=2019, month=3, day=1, hour=8)
        self.tiempo_incremento = pd.Timedelta("1m")
        # Para pasar a de las 4pm a las 8am
        self.dia_incremento = pd.Timedelta("16h")
        self.cont = 0

    def crear_alumnos(self):
        """
        Genera los estudiantes que estarán en la sala según números enteros
        de hombres y mujeres que no deben sumar más de 36. Los almacena en la
        lista self.estudiantes de forma desordenada
        """
        crear = False
        print(
            """\n##########################################
############ SIMULACIÓN ##################
##########################################

Bienvenidos a la simulación! Esta simulación genará datos de un curso
durante una cantidad arbitraria de días. Se asumen que las jornadas 
escolares serán de 8 horas y se obtiene información cada 1 minuto.

Los datos que se deben ingresar son:

- Estudiantes totales: Cantidad de estudiantes. Por como se define la
                        distribución de la sala se sugiere que este sea un 
                        múltiplo de 3.

- Estudiantes afectados: Cantidad de estudiantes que están siendo afectados
                         por alguna situación. Tienen constantemente una tendencia
                         emocional negativa y suelen no interactuar mucho

- Estudiantes vulnerables: Estudiantes que, a pesar de no presentar siempre una 
                            tendencia negativa, es posible que durante este periodo
                            muestren comportamientos con tendencia negativa.


NOTAS:

    - Para maximizar las posibilidades de interacción entre personas los puestos 
    serán cambiados de forma aleatoria todos los días


##############################################


""")
        while not crear:
            estudiantes = input("Ingrese cantidad de estudiantes totales \n")
            print()
            afectados = input("Ingrese cantidad de estudiantes afectados \n")
            print()
            vulnerables = input(
                "Ingrese cantidad de estudiantes vulnerables \n")
            print()
            self.dias = int(input("Ingrese cantidad dias para simular \n"))
            print()

            if not estudiantes.isdigit() or not afectados.isdigit() or not vulnerables.isdigit():
                print("Se debe ingresar números enteros")
            elif int(estudiantes) > 36:
                print("Los alumnos deben ser máximo 36")
            elif (int(vulnerables) + int(afectados)) > int(estudiantes):
                print("Los alumnos afectados no pueden superar al total")
            else:
                crear = True
                estudiantes = int(estudiantes)
                afectados = int(afectados)
                vulnerables = int(vulnerables)

        # Poblar estudiantes no afectados
        for _ in range(estudiantes - afectados - vulnerables):
            genero = random.choice(["mujer", "hombre"])
            self.estudiantes.append(NoAfectado(genero=genero))

        # Poblar estudiantes afectados
        for _ in range(afectados):
            genero = random.choice(["mujer", "hombre"])
            estudiante = Afectado(genero=genero)
            self.estudiantes.append(estudiante)
            self.afectados.append(estudiante)

        for _ in range(vulnerables):
            genero = random.choice(["mujer", "hombre"])
            estudiante = Vulnerable(genero=genero)
            self.estudiantes.append(estudiante)
            self.vulnerables.append(estudiante)

        random.shuffle(self.estudiantes)

    def ordenar_alumnos(self):
        """
        asigna puestos de la sala a los alumnos en su atributo
        Estudiante.puesto. Los puestos son tuplas que designan (fila,columna)
        y se salta números en los pasillos.
        xxx|xxx|xxx
        xxx|xxx|xxx
        xxx|xxx|xxx
        xxx|xxx|xxx
        """
        for i in self.estudiantes:
            i.puesto = self.asientos.pop(0)

    def cambiar_puestos(self):
        """
        Cambia los puestos de los alumnos de forma
        aleatoria
        """
        self.asientos = []
        for j in range(8):
            for i in range(11):
                if i != 3 and i != 7 and j % 2 == 0:
                    self.asientos.append((i + 1, j + 1))

        random.shuffle(self.estudiantes)

        self.ordenar_alumnos()

    def tick(self, tick_value, asistentes):
        """
        Es un ciclo de simulación. Equivale a un minuto

        """
        for i in asistentes:
            # Se cambia "sociabilizando" a false y si quiere interactuar
            i.definir_interactuar()
            # Se cambia la emocion
            i.cambiar_emocion(tick_value)
        for i in asistentes:
            if i.sociabilizar and not i.sociabilizando:
                candidatos_interaccion = []
                for j in asistentes:
                    if j.sociabilizar and not j.sociabilizando and j != i:
                        i_fila, i_columna = i.puesto
                        j_fila, j_columna = j.puesto
                        # 1 es la distancia Incrementarlo permite sociabilizar a mayor distancia.
                        if (abs(i_fila - j_fila) + abs(i_columna - j_columna)) <= 2:
                            candidatos_interaccion.append(j)
                if candidatos_interaccion:
                    elegido = random.choice(candidatos_interaccion)
                    i.sociabilizando = True
                    i.sociabilizacion_cont += 1
                    elegido.sociabilizando = True
                    elegido.sociabilizacion_cont += 1

                    # Agregar interacciones
                    i.agregar_interaccion(elegido, tick_value)
                    elegido.agregar_interaccion(i, tick_value)

                    #str = i.__repr__() + " interactuando con " + elegido.__repr__()
                    # print(str)

    def simular(self):
        for dia in range(self.dias):
            print(f"\nSimulando dia {dia} de {self.dias}")
            print(f"Fecha: {self.hora.strftime('%Y/%m/%d')}")
            weekday = self.hora.weekday()
            if weekday % 7 == 5 or weekday % 7 == 6:
                print('Fin de semana')
                self.hora += pd.Timedelta('1d')
                continue

            # Definir asisentes
            asistentes = []
            for estudiante in self.estudiantes:
                estudiante.definir_asistencia(self.hora.strftime('%Y/%m/%d'))
                if estudiante.presente:
                    asistentes.append(estudiante)

            # Ver si las personas vulnerables cambian su comportamiento
            for estudiante in self.vulnerables:
                estudiante.definir_cambio()

            # Simular por cada minuto durante 8 horas
            for _ in range(60 * 8):
                self.tick(self.hora.strftime('%Y/%m/%d, %H:%M:%S'), asistentes)

                # Aumentar el tiempo
                self.hora += self.tiempo_incremento
                self.cont += 1

            # Cambiar de dia
            self.hora += self.dia_incremento
            # Cambiar los puestos en la sala
            self.cambiar_puestos()

        self.generar_reporte()

    def generar_reporte(self):
        registros = defaultdict(dict)
        for estudiante in self.estudiantes:
            id_estudiante = estudiante.nombre + estudiante.apellido
            registros[id_estudiante]['emociones'] = estudiante.registro_emociones
            registros[id_estudiante]['interacciones'] = estudiante.registro_interacciones

            # Rellenar datos de alumnos
            registros[id_estudiante]['data'] = defaultdict(dict)
            registros[id_estudiante]['data']['nombre'] = estudiante.nombre
            registros[id_estudiante]['data']['apellido'] = estudiante.apellido
            registros[id_estudiante]['data']['comuna'] = estudiante.comuna
            registros[id_estudiante]['data']['apoderado'] = estudiante.apoderado
            registros[id_estudiante]['data']['profesor_jefe'] = estudiante.profesor_jefe
            registros[id_estudiante]['data']['telefono'] = estudiante.telefono
            registros[id_estudiante]['data']['genero'] = estudiante.genero
            registros[id_estudiante]['data']['promedio_ant'] = estudiante.promedio_ant
            registros[id_estudiante]['data']['promedio_parcial'] = estudiante.promedio_parcial
            registros[id_estudiante]['data']['n_evaluaciones_deficientes'] = estudiante.n_evaluaciones_deficientes
            registros[id_estudiante]['data']['citas_psicologo'] = estudiante.citas_psicologo
            if hasattr(estudiante, 'test_realizados'):
                registros[id_estudiante]['data']['test_realizados'] = estudiante.test_realizados

            # Guardar inasistencias
            registros[id_estudiante]['inasistencias'] = estudiante.inasistencias

        with open('registro.json', 'w') as out:
            json.dump(registros, out)

        with open('afectados.txt', 'w') as out:
            out.write("Afectados:\n")
            for afectado in self.afectados:
                id_afectado = afectado.nombre + afectado.apellido
                out.write(id_afectado + "\n")
            out.write("\nVulnerables:\n")
            for vulnerable in self.vulnerables:
                id_vulnerable = vulnerable.nombre + vulnerable.apellido
                out.write(id_vulnerable + "\n")


if __name__ == '__main__':
    sala = Sala()
    sala.simular()
