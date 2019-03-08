# Simulacion

## Personalidades

- Afectado: Tendencia emocional negativa y baja tendencia a interactuar
- No afectado: Tendencia emocional positiva y tendencia a intactuar media o alta

## Calidad de interacción

*EDIT 03/03/2018: Se decidió dejar esto de lado*

Una interacción es mala cuando al menos uno de los dos presenta emociones negativas (enojo, disgusto, triste, miedo)

## Formato de salida

*registro.json*
- Personas
  - ID_Persona
    - Nombre
    - Emociones
      - Dia-Hora
        - Emocion
          - % de seguridad con que detectó la emoción
    - Interacciones
      - ID_otra_persona
        - Día-Hora
        
*afectado.txt*
- Nombres de personas que sean `Afectado`
