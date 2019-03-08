import random
import numpy as np
import datetime
from collections import defaultdict


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

    # Parametros para function beta (distribucion de emocion)
    #TENDENDIA_ALTA = (1, 5)
    #TENDENCIA_BAJA = (5, 1)
    TENDENDIA_ALTA = (5, 2)
    TENDENCIA_BAJA = (2, 5)
    TENDENCIA_NEUTRA = (1.5, 1.5)

    def __init__(self, genero):
        self.genero = genero
        if genero is "hombre":
            self.nombre = random.choice(NOMBRES_H)
        elif genero is "mujer":
            self.nombre = random.choice(NOMBRES_M)
        self.apellido = random.choice(APELLIDOS)

        # Tendencias a interactuar y tendencia emocional
        self.sociabilidad = None
        self.tendencia_emocional = None

        self.interactuar = False  # indica disposición a interactuar
        self.interactuando = False  # indica si ya está interactuando o no
        self.puesto = None
        self.sociabilizacion_cont = 0

        # Datos a guardar: emociones e interacciones
        self.registro_emociones = {}  #  key: hora, values: maximo, score_emociones
        self.registro_interacciones = defaultdict(list)

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

    def cambiar_emocion(self, tick):
        """
        Las emociones cambian pero tienen predisposición a mantenerse.
        Se incrementa un contador para llevar una estadística de las emociones.
        Los pesos de cada emoción dependen de la sociabilidad.
        Pesos deben sumar 1 o da error
        """
        scores = {}
        if self.tendencia_emocional == "negativa":
            # Tendencia alta de emociones: miedo, disgusto, enojo y tristeza
            # Tendencia baja de emociones: sorpresa, alegria
            # Tendencia neutra de emociones: neutro

            for emocion in ['miedo', 'disgusto', 'enojo', 'trizteza']:
                scores[emocion] = random.betavariate(
                    *Estudiante.TENDENDIA_ALTA)

            for emocion in ['sorpresa', 'alegria']:
                scores[emocion] = random.betavariate(
                    *Estudiante.TENDENCIA_BAJA)

            for emocion in ['neutro']:
                scores[emocion] = random.betavariate(
                    *Estudiante.TENDENCIA_NEUTRA)

        elif self.tendencia_emocional == "positiva":
            # Tendencia alta de emociones: sorpresa, alegria
            # Tendencia baja de emociones: miedo, disgusto, enojo y tristeza
            # Tendencia neutra de emociones: neutro

            for emocion in ['miedo', 'disgusto', 'enojo', 'trizteza']:
                scores[emocion] = random.betavariate(
                    *Estudiante.TENDENCIA_BAJA)

            for emocion in ['sorpresa', 'alegria']:
                scores[emocion] = random.betavariate(
                    *Estudiante.TENDENDIA_ALTA)

            for emocion in ['neutro']:
                scores[emocion] = random.betavariate(
                    *Estudiante.TENDENCIA_NEUTRA)

        maximo_val = 0
        maximo_key = None
        for (key, val) in scores.items():
            if val > maximo_val:
                maximo_val = val
                maximo_key = key

        self.registro_emociones[tick] = {
            'maximo': maximo_key,
            'scores': scores
        }

    def agregar_interaccion(self, otro, tick):
        """
        Agrega interacción con otra persona
        """
        id_otro = otro.nombre + otro.apellido
        self.registro_interacciones[id_otro].append(tick)

    def __repr__(self):
        return self.nombre + " " + self.apellido


class Afectado(Estudiante):
    def __init__(self, *args, **kwargs):
        """
        El afectado es un estudiante que sociabiliza poco y tiene tendencia emocional negativa.
        """

        # Iniciar atributos de estudiante
        super().__init__(*args, **kwargs)

        self.sociabilidad = 'baja'
        self.tendencia_emocional = 'negativa'


class NoAfectado(Estudiante):
    def __init__(self, *args, **kwargs):
        """
        El afectado es un estudiante con sociabilidad media o alta y tiene tendencia emocional positiva.
        """

        # Iniciar atributos de estudiante
        super().__init__(*args, **kwargs)

        self.sociabilidad = random.choice(['media', 'alta'])
        self.tendencia_emocional = 'positiva'


class Vulnerable(Estudiante):
    def __init__(self, vulnerabilidad=0.1, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.sociabilidad = random.choice(['media', 'alta'])
        self.tendencia_emocional = 'positiva'

        # Probabilidad de que se presente un caso que exponga al alumno
        self.vulnerabilidad = vulnerabilidad
        self.tendencia_actual = 'positiva'

    def cambiar_tendencia(self):
        """
        Cambia la tendencia emocional actual del estudiante
        """
        if self.tendencia_actual == 'positiva':
            self.sociabilidad = 'baja'
            self.tendencia_emocional = 'negativa'
            self.tendencia_actual = 'negativa'

        else:
            self.sociabilidad = random.choice(['media', 'alta'])
            self.tendencia_emocional = 'positiva'
            self.tendencia_actual = 'positiva'

    def definir_cambio(self):
        """
        Decide de forma aleatoria, según la vulnerabilidad del niño, si
        sufrirá de una situación que lo exponga.
        """
        hay_cambio = np.random.choice(
            [False, True], p=[1 - self.vulnerabilidad, self.vulnerabilidad])
        if hay_cambio:
            self.cambiar_tendencia()
