"""
2018 - Proyecto LookOut

Este codigo tiene por intencion recopilar las funciones que ayuden a la deteccion de una interaccion en
la sala de clases.

Los tipos de interacciones que se definiran son:

    - Simple Interaction:
        Dos personas conversan sin obstaculos entremedio

    - Complex interaction:
        Tres interacctuan o dos con una persona entremedio que no lo hace.


Restricciones:
    1) Una persona solo puede interactuar con personas en la misma fila o, como maximo, dentro de una
    distancia definida de la fila (esta debe poder ser modificable)

    2) Una persona solo puede interactuar con personas con las que tenga como maximo una persona de separacion.
    Esto es, pueden interactuar personas que se encuentren al lado o con maximo una persona entre ellas.

        ** Idea: Que la distancia entre personas sea un parametro

    3) Dos personas interactuan si sus miradas se cruzan y se cumplen las restricciones 1) y 2)

    4) 3 personas interactuan si dos de ellas interactuan (siguiendo la restriccion 3)) con una tercera en comun.

* Notese que dos personas pueden interactuar entre si y tener una persona entre ellas que no interactua


Atributos utiles de la API:

    - faces [list]: lista de caras, cada cara es un diccionario cuyos atributos utiles se especifican a continuacion:

        - face_token [string]: id de la cara
        - face_rectangle [dict]: coordenadas ("width", "top", "bottom", "height") de la cara
        - attributes [dict]:

            - headpose [dict]: angulos de "yaw_angle", "pitch_angle" y "roll_angle" (valores en [-180,180])
            - (soon) eyegaze [dict]: Representa la posicion y la direccion de la mirada de cada ojo.
                Contiene los elementos left_eye_gaze y right_eye_gaze, cada uno con los atributos:
                    - position_x_coordinate: the x coordinate of eye center
                    - position_y_coordinate: the y coordinate of eye center
                    - vector_x_component: the x component of eye gaze direction vector
                    - vector_y_component: the y component of eye gaze direction vector
                    - vector_z_component: the z component of eye gaze direction vector

"""


def do_eyegazes_cross(data, face_token1, face_token2):
    """
    Revisar si las miradas dos personas se cruzan

    :param data: JSON data
    :type data: dict

    :param face_token1: Face token del primer sujeto a comparar
    :type face_token1: str

    :param face_token2: Face token del segundo sujeto a comparar
    :type face_token2: str

    :return: [bool] True si las miradas de dos personas se cruzan
    """
    pass


def check_separation(data, face_token1, face_token2):
    """
    Revisar si dos personas cumplen la restriccion de separacion (saltarse maximo una persona)

    :param data: JSON data
    :type data: dict

    :param face_token1: Face token del primer sujeto a comparar
    :type face_token1: str

    :param face_token2: Face token del segundo sujeto a comparar
    :type face_token2: str

    :return: [bool] Sujetos cumplen las restricciones
    """
    pass


def check_row(data, face_token, row_definitions):
    """
    Recibe los datos, un face token y a definicion de las filas y retorna todas las filas en la que se
    encuntra el sujeto.

    :param data: JSON data

    :param face_token: Face token del sujeto a comparar
    :type face_token: str

    :param row_definitions: lista de tuplas que definen el inicio y el fin de una fila (pueden sobrelaparse)

    :return: Lista de filas en las que se encuentra el sujeto
    """
    pass


def check_single_interaction(data, face_token1, face_token2):
    """
    Revisa si dos personas cumplen las restricciones de interaccion

    :param data: JSON data
    :type data: dict

    :param face_token1: Face token del primer sujeto a comparar
    :type face_token1: str

    :param face_token2: Face token del segundo sujeto a comparar
    :type face_token2: str

    :return: [bool] Sujetos interactuan
    """
    pass


def check_interactions(data):
    """
    Recibe el JSON de la API y retorna lista de tupla de interacciones. Las tuplas no pueden repetirse
    (es decir, si (A, B) esta en la lista no puede estar (B, A)).

    :param data: JSON data
    :return: [list] lista de tuplas de los tokens de personas que interactuan
    """
    pass








