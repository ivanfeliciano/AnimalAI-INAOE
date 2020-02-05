# Ambiente simplicado

Dada la complejidad de la tarea de Animal AI Olympics, se propone 
comenzar con escenarios mucho más simples donde se conserven relaciones 
causales del tipo: observación + acción -> efecto (meta, submeta, estados no deseados).

Para esto se configuró el ambiente de la clase ml-agents de Unity.
En esta modificación se fija una velocidad del agente constante, es decir, 
al realizar la acción de movimiento hacia atrás o adelante se le aplica una fuerza al 
agente, pero se regresa su velocidad a cero.
Además, las rotaciones son de 90 grados en cualquiera de los sentidos.
Con estas modificaciones se propone limitar los movimientos del agente, y así
tratar a la arena más como una cuadrícula. Donde el agente se mueve en pasos
de una unidad completa (1 metro en la arena).
Así las posiciones y tamaños de los objetos de los objetos se manejan facilmente (de manera burda
los objetos tiene posiciones discretas con respecto a la cuadrícula).


Algunas reglas que se siguen en esta modificación son las siguientes:

+ El agente comienza en una posición (0.5n, 0, 0.5m), donde n,m pertenecen a los enteros positivos.
+ Los objetos son inmóviles e inician en una posición (0.5n, 0, 0.5m), donde n,m pertenecen a los enteros positivos.
+ Se dejan fuera aquellos objetos que alteran la posición del agente, por ejemplo
las rampas o plataformas. (TO DO, hacer una proyección).

## Relaciones

Algunos de las escenarios que se pueden encontrar donde haya relaciones causales son
los siguientes.

### Metas y submetas

| Observación      | Acción  | Efecto                           |
|------------------|---------|----------------------------------|
| GoodGoal         | Forward | Acabar y obtener goodGoal reward |
| BadGoal          | Forward | Morir y obtener badGooal reward  |
| DeathZone        | Forward | Morir y obtener badGooal reward  |
| HotZone          | Forward | Obtener y bad reward             |
| Caja y encerrado | Forward | Cerca de comida                  |
| Pared            | Forward | perderme                         |




