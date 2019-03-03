# coding=utf-8
import random
import numpy as np
import datetime
from estudiantes import Afectado, NoAfectado
from collections import defaultdict
import json


class Sala:
    def __init__(self):
        self.asientos = []
        self.afectados = []
        self.estudiantes = []
        for j in range(8):
            for i in range(11):
                if i != 3 and i != 7 and j % 2 == 0:
                    self.asientos.append((i + 1, j + 1))
        self.crear_alumnos()
        self.ordenar_alumnos()
        self.hora = datetime.timedelta(hours=8, minutes=30)
        self.tiempo_incremento = datetime.timedelta(minutes=1)
        self.cont = 0

    def crear_alumnos(self):
        """
        Genera los estudiantes que estarán en la sala según números enteros
        de hombres y mujeres que no deben sumar más de 36. Los almacena en la
        lista self.estudiantes de forma desordenada
        """
        crear = False
        while not crear:
            print("El número de mujeres y hombres no debe sumar más de 36")

            estudiantes = input("Ingrese cantidad de estudiantes totales \n")
            afectados = input("Ingrese cantidad de estudiantes afectados \n")

            if not estudiantes.isdigit() or not afectados.isdigit():
                print("Se debe ingresar números enteros")
            elif int(estudiantes) > 36:
                print("Los alumnos deben ser máximo 36")
            elif int(afectados) > int(estudiantes):
                print("Los alumnos afectados no pueden superar al total")
            else:
                crear = True
                estudiantes = int(estudiantes)
                afectados = int(afectados)

        # Poblar estudiantes no afectados
        for k in range(estudiantes - afectados):
            genero = random.choice(["mujer", "hombre"])
            self.estudiantes.append(NoAfectado(genero))

        # Poblar estudiantes afectados
        for k in range(afectados):
            genero = random.choice(["mujer", "hombre"])
            estudiante = Afectado(genero)
            self.estudiantes.append(estudiante)
            self.afectados.append(estudiante)

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

    def tick(self, tick_value):
        """
        Es un ciclo de simulación. Equivale a un minuto

        """
        for i in self.estudiantes:
            i.definir_interactuar()
            i.cambiar_emocion(tick_value)
        for i in self.estudiantes:
            if i.sociabilizar and not i.sociabilizando:
                candidatos_interaccion = []
                for j in self.estudiantes:
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

                    str = i.__repr__() + " interactuando con " + elegido.__repr__()
                    print(str)
        self.hora += self.tiempo_incremento
        self.cont += 1

    def simular(self):
        while self.cont < 120:
            self.tick(self.cont)
        self.generar_reporte()

    def generar_reporte(self):
        registros = defaultdict(dict)
        for estudiante in self.estudiantes:
            id_estudiante = estudiante.nombre + estudiante.apellido
            registros[id_estudiante]['Emociones'] = estudiante.registro_emociones
            registros[id_estudiante]['Interacciones'] = estudiante.registro_interacciones

        with open('registro.json', 'w') as out:
            json.dump(registros, out)

        with open('afectado.txt', 'w') as out:
            for afectado in self.afectados:
                id_afectado = afectado.nombre + afectado.apellido
                out.write(id_afectado)

        """
        reporte = open('reporte.txt', 'w')
        for i in self.estudiantes:
            reporte.write("--------------------------\n")
            reporte.write(f"Nombre: {i.__repr__()} \n")
            reporte.write(f"Sociabilidad: {i.sociabilidad} \n")
            sociabilizacion = "{:.2f}".format(
                i.sociabilizacion_cont * 100 / self.cont)
            reporte.write(f"Sociabilización: {sociabilizacion}% \n")
            emocion_total = i.miedo_cont + i.disgusto_cont + i.alegria_cont +\
                i.neutro_cont + i.sorpresa_cont + i.enojo_cont + i.tristeza_cont
            reporte.write(f"Puesto: {i.puesto} \n")
            reporte.write("--Emociones--\n")
            miedo = "{:.2f}".format(
                i.miedo_cont * 100 / emocion_total)
            reporte.write(f"Miedo: {miedo}% \n")
            disgusto = "{:.2f}".format(
                i.disgusto_cont * 100 / emocion_total)
            reporte.write(f"Disgusto: {disgusto}% \n")
            alegria = "{:.2f}".format(
                i.alegria_cont * 100 / emocion_total)
            reporte.write(f"Alegria: {alegria}% \n")
            neutro = "{:.2f}".format(
                i.neutro_cont * 100 / emocion_total)
            reporte.write(f"Neutro: {neutro}% \n")
            sorpresa = "{:.2f}".format(
                i.sorpresa_cont * 100 / emocion_total)
            reporte.write(f"Sorpresa: {sorpresa}% \n")
            enojo = "{:.2f}".format(
                i.enojo_cont * 100 / emocion_total)
            reporte.write(f"Enojo: {enojo}% \n")
            tristeza = "{:.2f}".format(
                i.tristeza_cont * 100 / emocion_total)
            reporte.write(f"Tristeza: {tristeza}% \n")
        """


if __name__ == '__main__':
    sala = Sala()
    sala.simular()
