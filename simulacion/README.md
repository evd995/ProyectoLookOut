# Simulacion

## Personalidades

- Afectado: Tendencia emocional negativa y baja tendencia a interactuar
- No afectado: Tendencia emocional positiva y tendencia a intactuar media o alta

## Calidad de interacción

_EDIT 03/03/2019: Se decidió dejar esto de lado_

Una interacción es mala cuando al menos uno de los dos presenta emociones negativas (enojo, disgusto, triste, miedo)

## Formato de salida

_EDIT 22/04/2019: Se agregan datos del alumno_

_registro.json_

- Personas
  - ID_Persona
    - emociones
      - Timestamp
        - Emocion
          - % de seguridad con que detectó la emoción
    - interacciones
      - ID_otra_persona
        - Timestamp
    - data
      - nombre
      - apellido
      - domicilio
      - comuna
      - apoderado
      - profesor_jefe
      - telefono
      - genero
      - promedio_ant
      - promedio_parcial
      - n_evaluaciones_deficientes
      - citas_psicologo
      - tests_realizados
        - nombre
        - resultados

_afectado.txt_

- Nombres de personas que sean `Afectado`

## Relleno de datos

La simulación consta de los siguentes pasos

1. Inicializar la sala

   1. Se crean alumnos

   2. Se ordenan en la sala

2. Correr 'tick'

   1. Se definen los alumnos que van a interactuar

   2. Se definen las personas que van a cambiar de opinión

3. Generar reporte
