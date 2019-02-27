# Simulacion


## Cosas por agregar:

- [1] Personalidades, la mayoría debe ser promedio 
- [1] Calidad de interacción (buena o malo) 
- [2] Guardar los tiempos de cada "tick" y que se guarden los datos relevantes asociados a cada tiempo (interacciones, emociones, etc)
- [1] Cambiar el output de las emociones a vectores

[1]: Se pueden hacer rápido (Feña)

[2]: Hay que pensar en cómo se guardarán los datos en la base de datos y en el dashboard


## Personalidades

- Aislado: Persona que se siente incomoda interactuando. Cuando está sola tiene mayor tendencia a estar neutra.
- Acosado: Tiene tendencia a tener malas interacciones
- Popular: Una persona que tiene buenas interacciones y estas son buenas. Tendencia más histriónica (felicidad y sorpresa)
- Persona promedio: Interacciones moderadas, buenas interacciones, mas tendencia a emociones neutras (neutro, feliz, disgusto). 
- Acosador: Muchas interacciones malas con persona acosada o aislada, pero buenas con popular u otros. Emoción contenta o neutra. 
- Amargado: Mayor tendencia a disgusto o enojo. Puede tener interacciones tanto buenas como malas de forma aleatoria.
- Otros...

## Calidad de interacción

Una interacción es mala cuando al menos uno de los dos presenta emociones negativas (enojo, disgusto, triste, miedo)

## Formato de salida

- Personas
  - ID_Persona
    - Emociones
      - Dia-Hora
        - Emocion
        - % de seguridad con que detectó la emoción
    - Interacciones
      - Dia-Hora
        - Persona con quien interacuó
        - Emocion que sentia
