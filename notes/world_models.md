# World Models

Proponen un *modelo del mundo* que se puede entrenar rápido y de manera no supervisada para
aprender una representación comprimida espacial y temporal del ambiente. Usando características
extraídas del modelo del mundo  como entradas para el agente, se puede entrenar una política que 
resuelva la tarea requerida.
Incluso se puede entrenar al agenete enteramente dentro del *ambiente soñado* generado por
su modelo del mundo y transferir esta políticia al ambiente real.


*Modelo mental:* La imagen del mundo a nuestro alrededor, el cual llevamos en nuestra mente, es 
sólo un modelo. Nadie en su cabeza imagina todo el mundo, gobierno o país. Tenemos solo
conceptos seleccinados y relaciones entre ellos y usamos éstas para represetar el sistema real.

Nuestro cerebro aprende una representación abstracta de ambos aspectos (espacio, tiempo)
de la inmensa cantidad de información diaria. Por lo tanto, somos capaces de observar una escena y 
recordar una descripción abstracta. Lo que percibimos en cualquier momento está gobernado
por la predicción del futuro de nuestro cerebo basado en nuestro modelo interno.

Este modelo de predicción puede que no prediga el futuro en general, pero predice 
futuros datos sensoriales dado nuestro motor de acciones actual.

En varios problemas de RL, un agente se benefiica de tener una buena representación de los
estados del presente y del pasado y de un buen modelo predictivo del futuro, de preferencia 
una modelo predictivo poderos implementado en un computadora de propósito general como una
RNN.

RNN son modelos altamente expresivos que pueden aprender representaciones espaciales y temporales
de los datos.

Idealmente, nos gustaría ser capaces de entrenar eficientemente agenter basados en RNN muy grandes.

En este trabajo se busca entrenar una red neuronal grande para tareas de RL, dividiéndola en un
modelo grande del mundo y modelo controlador pequeño.
Se entra una red neurnal para aprender el modelo del mundo del agente de una manera no supervisada,
luego se entrena un modelo controlador para aprender a realizar la tarea usando este modelo 
del mundo.

El controlador deja que el algoritmo de entrenamiento se enfoque en el problema de asignación
de crédito sobre un espacio de búsqueda más pequeño, mientra no sacrifica la capacidad y 
expresividad a través de un modelo del mundo más grande.

Al entrenar al agente a través de los lentes de su modelo del mundo, se muestra que
puede aprender una política compacta pra realizar su tarea.

## Modelo del agente


El agente tiene los siguientes componentes:

* Un modelo del mundo:
	* El *modelo de visión* **V** codifica la observación de alta dimensionalidad a un
vector latente de baja dimensión.
	* La *memoria RNN* **M** integra los códigos históricos para crear una representación que pueda predecir estados futuros.

* Un pequeño *controlador* **C** que utiliza las representaciones de ambos V y M para seleccionar buenas acciones.

**Creo que en el paso anterior está la clave y la aportación, ahora falta integrar esa medida
de cusa diferida xd**.

* El agente realiza las acciones que "go back" y afectan al ambiente.

V -> M -> C

### Modelo VAE  (V)

El papel del modelo V es aprender un representación abstracta y comprimida de cada fotograma de
entrada observado.

Se utiliza un Variational Autoencoder (VAE) como el modelo V en los experimentos. 

### Modelo MDN-RNN (M)

Mientras que es el rol del modelo V comprimir lo que el agente ve en cada fotograma de tiempo,
también se desea comprimir lo que pasa a lo largo del tiempo. Para esto, el rol de M es predecir 
el futuro.
El modelo M sirve como un modelo predictivo de los futuros vectores z  que se esperan que V produzca.

Se entrena la RNN para que su salida sea una función de densidad de probabilidad p(z).
Se aproxima p(z) con una distribución de mezclas Gaussianas, y se entrena la RNN para tener como
salida la distribución de probabilidad del siguiente vector latente z<sub>t+1</sub> dado la información
del paso y del presente disponible.

Más específicamente, la RNN modela P(z<sub> t + 1</sub>)


