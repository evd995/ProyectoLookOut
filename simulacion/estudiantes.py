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

        # Default de datos
        self.apellido = None
        self.nombre = None
        self.apoderado = None
        self.domicilio = None
        self.comuna = None
        self.apoderado = None
        self.profesor_jefe = None
        self.telefono = None
        self.promedio_ant = None
        self.promedio_parcial = None
        self.n_evaluaciones_deficientes = None
        self.citas_psicologo = None
        self.tests_realizados = None

        self.rellenar_datos()

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

        # Asistencias
        self.inasistencias = {}
        self.presente = False

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

    def rellenar_datos(self):
        """
        Función que rellena los datos del alumno
        """

        # Seleccionar nombre
        if self.genero == "hombre":
            self.nombre = random.choice(NOMBRES_H)
        elif self.genero == "mujer":
            self.nombre = random.choice(NOMBRES_M)

        # Seleccionar apellido
        self.apellido = random.choice(APELLIDOS)

        # Seleccionar nombre de apoderado
        self.apoderado = random.choice(NOMBRES_H) + ' ' + self.apellido

        # Seleccionar comuna
        self.comuna = random.choice(
            ['Santiago', 'Providencia', 'Ñuñoa', 'Estación Central'])

        # Seleccionar domicilio
        prefijo_calle = random.choice(['Pdte.', 'Sta.'])
        if prefijo_calle == 'Pdte.':
            self.domicilio = prefijo_calle + ' ' + random.choice(APELLIDOS)
        elif prefijo_calle == 'Sta.':
            self.domicilio = prefijo_calle + ' ' + random.choice(NOMBRES_M)

        # Seleccionar notas
        self.promedio_ant = random.choice(np.arange(5, 7, 0.1))
        variacion_nota = random.choice([-0.2, -0.1, 0, 0.1, 0.2])
        nueva_nota = self.promedio_ant + variacion_nota
        self.promedio_parcial = min(nueva_nota, 7)

        # Seleccionar profesor jefe
        self.profesor_jefe = 'Valentina Mansilla'

        # Evaluaciones deficientes
        self.n_evaluaciones_deficientes = random.choice(range(0, 4))

        # Citas al psicologo
        self.citas_psicologo = random.choice(range(0, 3))

        self.tests_realizados = {}
        # Tests realizados
        if self.citas_psicologo:
            tests_posibles = [
                [],
                ['My bullying'],
                ['Test de Lúscher'],
                ['My bullying', 'Test de Lúscher']
            ]
            tests_psicologicos = random.choice(tests_posibles)
            for i, nombre_test in enumerate(tests_psicologicos):
                self.tests_realizados[i] = {
                    'nombre': nombre_test,
                    'resultado': random.choice(['positivo', 'negativo'])
                }

        self.telefono = random.choice(range(10000000, 99999999, 10))

    def definir_asistencia(self, dia):
        """
        Se define si la persona esta ausente o presente en un dia

        Si un alumno estuvo ausente tiene una probabilidad más alta de seguir ausente
        al día siguiente
        """
        if self.presente:
            peso = [0.95, 0.05]
        else:
            peso = [0.8, 0.2]

        self.presente = np.random.choice([True, False], p=peso)

        if not self.presente:
            self.inasistencias[dia] = True

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
