import random
import numpy as np
import datetime

NOMBRES_H = ["Aldo", "Benito", "Carlos", "Damián", "Edgar", "Fabián",
             "Gabriel", "Hugo", "Iván", "Jorge", "Kevin", "Lucas", "Marcos",
             "Nicolás", "Óscar", "Pablo", "Rafael", "Sergio", "Tomás",
             "Ulises", "Vicente"]

NOMBRES_M = ["Adela", "Berta", "Camila", "Delia", "Ema", "Florencia", "Gilda",
             "Hilda", "Inés", "Jacinta", "Karen", "Lara", "Maite", "Natalia",
             "Octavia", "Pía", "Romina", "Sabrina", "Telma", "Úrsula", "Viviana"]

APELLIDOS = ["Gonzalez", "Muñoz", "Rojas", "Diaz", "Perez", "Soto", "Silva",
             "Contreras", "Lopez", "Rodriguez", "Morales", "Martinez",
             "Fuentes", "Valenzuela", "Araya", "Sepulveda", "Espinoza",
             "Torres", "Castillo", "Ramirez", "Flores", "Castro", "Fernandez",
             "Alvarez", "Hernandez", "Herrera", "Vargas", "Gutierrez", "Gomez"]


class Estudiante:
    def __init__(self, genero):
        self.genero = genero
        if genero is "hombre":
            self.nombre = random.choice(NOMBRES_H)
        elif genero is "mujer":
            self.nombre = random.choice(NOMBRES_M)
        self.apellido = random.choice(APELLIDOS)
        self.definir_sociabilidad()
        self.interactuar = False  # indica disposición a interactuar
        self.interactuando = False  # indica si ya está interactuando o no
        self.puesto = None
        self.sociabilizacion_cont = 0

        self.emocion = "neutro"
        self.miedo_cont = 0
        self.disgusto_cont = 0
        self.alegria_cont = 0
        self.neutro_cont = 0
        self.sorpresa_cont = 0
        self.enojo_cont = 0
        self.tristeza_cont = 0

    def definir_sociabilidad(self):
        """
        Define de forma aleatoria la sociabilidad como baja, media o alta.
        Los estudiantes tienen tendencia a ser más sociables (dado por la media
        de cada distribución).
        """
        baja = random.gauss(1, 0.4)
        media = random.gauss(1.2, 0.4)
        alta = random.gauss(1.4, 0.4)
        output = max([baja, media, alta])
        if output == baja:
            self.sociabilidad = "baja"
        elif output == media:
            self.sociabilidad = "media"
        elif output == alta:
            self.sociabilidad = "alta"

    def definir_interactuar(self):
        """
        Define si en esta 'ronda' (tick de simulación) el estudiante está
        dispuesto a interactuar o no. Los pesos de ambas opciones dependen de
        su sociabilidad.
        Además, vuelve el "sociabilizando" a False
        """
        self.sociabilizando = False
        if self.sociabilidad == "baja":
            peso = [0.7, 0.3]
        elif self.sociabilidad == "media":
            peso = [0.5, 0.5]
        elif self.sociabilidad == "alta":
            peso = [0.3, 0.7]
        sociabilizar = np.random.choice(["false", "true"], p=peso)
        if sociabilizar == "false":
            self.sociabilizar = False
        elif sociabilizar == "true":
            self.sociabilizar = True

    def cambiar_emocion(self):
        """
        Las emociones cambian pero tienen predisposición a mantenerse.
        Se incrementa un contador para llevar una estadística de las emociones.
        Los pesos de cada emoción dependen de la sociabilidad.
        Pesos deben sumar 1 o da error
        """
        if self.sociabilidad == "baja":
            peso = [0.1, 0.1, 0.05, 0.1, 0.1, 0.1, 0.45]
        elif self.sociabilidad == "media":
            peso = [0.1, 0.1, 0.1, 0.45, 0.05, 0.1, 0.1]
        elif self.sociabilidad == "alta":
            peso = [0.1, 0.1, 0.45, 0.1, 0.1, 0.1, 0.05]

        if random.gauss(0.5, 0.2) > 0.5:
            self.emocion = np.random.choice(
                ["miedo", "disgusto", "alegria", "neutro", "sorpresa",
                 "enojo", "tristeza"], p=peso)

        if self.emocion == "miedo":
            self.miedo_cont += 1
        elif self.emocion == "disgusto":
            self.disgusto_cont += 1
        elif self.emocion == "alegria":
            self.alegria_cont += 1
        elif self.emocion == "neutro":
            self.neutro_cont += 1
        elif self.emocion == "sorpresa":
            self.sorpresa_cont += 1
        elif self.emocion == "enojo":
            self.enojo_cont += 1
        elif self.emocion == "tristeza":
            self.tristeza_cont += 1

    def __repr__(self):
        return self.nombre + " " + self.apellido


class Sala:
    def __init__(self):
        self.asientos = []
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
            mujeres = input("ingrese el número de mujeres \n")
            hombres = input("Ingrese el número de hombres \n")
            if not mujeres.isdigit() or not hombres.isdigit():
                print("Se debe ingresar números enteros")
            elif int(hombres) + int(mujeres) > 36:
                print("Los alumnos deben ser máximo 36")
            else:
                crear = True
                hombres = int(hombres)
                mujeres = int(mujeres)

        for k in range(hombres):
            self.estudiantes.append(Estudiante("hombre"))
        for k in range(mujeres):
            self.estudiantes.append(Estudiante("mujer"))
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

    def tick(self):
        """
        Es un ciclo de simulación. Equivale a un minuto

        """
        for i in self.estudiantes:
            i.definir_interactuar()
            i.cambiar_emocion()
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
                    str = i.__repr__() + " interactuando con " + elegido.__repr__()
                    print(str)
        self.hora += self.tiempo_incremento
        self.cont += 1

    def simular(self):
        while self.cont < 120:
            self.tick()
        self.generar_reporte()

    def generar_reporte(self):
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


sala = Sala()
sala.simular()
