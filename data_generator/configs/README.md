# Archivos de configuración de Animal AI


Los archivos XML de acuerdo con el Testbed de Animal AI. Estos archivos sirven para generar configuraciones del ambiente con respecto a diferentes experimentos.
Se puede dividir en las siguientes categorías.

+ Experimentos basados en la cognición animal. Estas tareas se han realizado por
al menos un tipo de animal.

+ Experimentos introductorios. Estas tareas son simples son para ir introduciendo diferentes características del ambiente al agente.

+ Otros. Incluyen experimentos tales como uso de la rampa, comida moviéndose, evación de zonas rojas, etc.


## Cognición animal

+ **Laberintos en Y**. Una rama contiene una recompensa preferida a la otra y, por lo general, ambas se pueden ver al mismo tiempo.

+ **Gratificación retrasada**. Resolver esto de manera robusta en el entorno Animal-AI requiere comprender que habrá una mayor recompensa demorada basada en la física del entorno.
*¿Cómo represento esto? ¿Comida que tarda en aparecer? ¿Comida buena que está cerca, pero hay comida mejor lejos?*

+ **Tareas de desvío**. Se prueba la habilidad para rodear un objeto para alcanzar la comida y tomar el camino más corto.

+ **Tareas de cilindro**. Se incluyen cilindros opacos y transparente.

+ **Experimentos de escape de Thorndike**. El agente debe escapar de un área confinada y la comida está afuera.

+ **Laberitos en T**. Parecido al Y, sólo que no se ven ambos brazos a la vez.

+ **Eliminación espacial**. Propiedades espaciales pueden ser usadas para inferir la localización de la comida, e.g., no puede estar en un el lugar abierto así que debe estar detrás de una pared.

+ **Soporte y sesgo de gravedad**. Las tareas involucran gravedad y comida apoyada en otros objetos.

+ **Laberitnos radiales**. Laberintos con una serie de radios que irradian desde un eje central.

+ **Permanencia de objetos**. Todas estas pruebas involucran alimentos que se mueven fuera de la vista que el agente aún necesita alcanzar.

+ **Numerosidad**. Todas estas pruebas involucran contar para navegar al compartimiento  con más comida.

+ **Uso de herramientas**. Estas pruebas se basan en la capacidad de usar los objetos empujables en la arena como herramientas improvisadas para obtener comida. Son los más complicados en el banco de pruebas y se extienden a la capacidad de realizar razonamientos causales simples sobre el resultado de la acción.



## Experimentos introductorios


+ **Comida básica en frente**. Comida (verde) directamente en frente del agente.

+ **Navegación básica**. Tareas muy simples para navegar hacia comida visible.

+ **Variaciones de comida**. Navergar hacia comida visible de diferentes tipos.

+ **Exploración básica**. Arenas vacías con una sóla pelota verde de diferentes tamaños y tipos. No son necesariamente visibles al principio.

+ **Mútiple comida**. Arenas vacías con muchas pelotas amarillas las cuales debes ser todas recolectadas.

+ **Comida básica y obstáculos**. Las pruebas introdutorias que pueden contener obstáculos que necesitan ser rodeados para alcanzar la comida.

## Otros

+ **Comida móvil**. Arenas simples con una sola pieza de comida moviéndose.

+ **Comida no alzable**. Problemas donde sólo hay recompensa negativa.

+ **Múltiple comida estacionaria**. Arena vacía con todo tipo de comida. La amarilla necesita ser recogida antes que la verde.

+ **Múltiple comida móvil**. Igual que la anterior pero móvil xd.

+ **Evación de zonas rojas**. Se necesita navegar alrederdor de recompensas negativas para obtener la comida.

+ **Uso de rampa**. En estas tareas el agente debe usar la rampa para ganar acceso a otra parte del ambiente.

+ **Cajas empujables**. Se necesitan empujar las cajas para entrar a otras zonas del ambiente.

+ **Zonas calientes**. Se integran las superficies que van descontando recompensa al estar sobre ellas (zonas naranjas).

+ **Generalización y adaptabilidad**. Se cambian los colores de los objetos, excepto la comida.

+ **Modelos internos**. Involucran que se vaya la luz.



