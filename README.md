# Socket y Ordenamiento
En este laboratorio su tarea es investigar cómo funcionan los sockets en Java o Python y usarlos para resolver lo siguiente:
Se desea tener un computador corriendo un programa y que sea el cliente, al comienzo del programa debe preguntarle al usuario qué problema quiere resolver. Los problemas a resolver son:
- Dado un vector de n posiciones, ordenarlo de manera ascendente usando el algoritmo de mergesort
- Dado un vector de n posiciones, ordenarlo de manera ascendente usando el algoritmo de heapsort
- Dado un vector de n posiciones, ordenarlo de manera ascendente usando el algoritmo de quicksort. El pivote inicial debe poderse escoger (las opciones son, el más a la izquierda o el más a la derecha).

Nota: Puede crear los vectores de manera aleatoria pero piense en valores de n grandes, entre 1000 y 100000.
Una vez decidido el problema a resolver este debe ser mandado a otro computador (distinto del cliente) llamado worker_# el cual junto con la ayuda de otro worker_#, deben ordenar el vector. Cada worker contara con un tiempo Z para poder resolver hasta donde pueda del problema, si en el tiempo Z el worker que actualmente tiene el vector no ha terminado la tarea debe mandar el vector como lo lleve al otro worker y este debe continuar el trabajo. Una vez resuelto el problema, el cliente worker que haya terminado el problema de devolver el vector ordenado al cliente junto con el tiempo que le tomó resolverlo. Finalmente, esta información debe ser mostrada por el cliente.

## Integrantes:
- Kenny Zhu
- Juan Aragon
- Tomas Cervera

## Información:
### Contenido
- worker1.py y worker2.py: implementan dos wokers que reciben solicitudes de ordenamiento de vectores del cliente. Cada woker puede ejecutar uno de los tres algoritmos de ordenamiento y manejar el tiempo límite establecido por el cliente. Si un woker no puede completar la tarea dentro del tiempo límite, enviará el vector parcialmente ordenado al otro woker para que continúe el trabajo.
- client.py: programa del cliente, que le pregunta al usuario qué problema quiere resolver, genera un vector aleatorio de tamaño 'n' y selecciona un algoritmo de ordenamiento para usar. Luego, el cliente envía el vector y el algoritmo seleccionado a uno de los wokers y espera los resultados. Si un woker no puede completar la tarea en el tiempo límite, el programa cambia al otro woker y continúa con la tarea. Una vez que el vector esté ordenado, el cliente mostrará el vector ordenado y el tiempo total de ordenamiento.
- utils.py: contiene las funciones para los algoritmos de ordenamiento: MergeSort, HeapSort y QuickSort. Además, también incluye funciones para enviar y recibir datos entre clientes y wokers.

### Ejecución
1. Asegúra tener Python instalado en tu computadora. 
2. Abre 3 terminales o ventanas de línea de comandos, puede hacerlo en VsCode creando o abriendo 3 terminales, para no dificultarse en cambiar los IP. En cada una de ellas, navega hasta la carpeta donde se encuentran los archivos.
3. En la primera terminal, ejecuta el primer woker ejecutando este comando:
```
python worker1.py
```
En la segunda terminal, ejecuta el segundo woker ejecutando este comando:
```
python worker2.py
```
En la tercera terminal, ejecuta el cliente ejecutando este comando:
```
python client.py
```

### Ejecucion en computadoras distintas
Para probar el programa en 3 computadoras diferentes, sigue estos pasos:
1. Asegúrate de que las 3 computadoras estén conectadas en la misma red local o puedan comunicarse entre sí a través de la red.
2. En la computadora que actuará como el cliente, copia el archivo client.py. En las otras dos computadoras, copia los archivos worker1.py, worker2.py y utils.py.
3. Determina las direcciones IP de las dos computadoras que ejecutarán los workers. Puedes hacerlo ejecutando ipconfig en Windows o en mac buscarlo en preferencias de sistemas.
4. Actualiza la dirección y el puerto de other_worker_addr en worker1.py y worker2.py para que apunte a la dirección IP y el puerto del otro worker.
- Por ejemplo, si la dirección IP de la computadora que ejecuta worker2.py es 192.168.1.102, deberás cambiar la línea en worker1.py que define other_worker_addr a:
```
other_worker_addr = ("192.168.1.102", 12346)
```
- Haz lo mismo en worker2.py, pero usando la dirección IP de la computadora que ejecuta worker1.py.
5. En la computadora cliente, actualiza las direcciones IP y los puertos de host, port1 y port2 en client.py para que coincidan con las direcciones IP y los puertos de las computadoras que ejecutan los workers. Por ejemplo, si la dirección IP de la computadora que ejecuta worker1.py es 192.168.1.101 y la de worker2.py es 192.168.1.102, debes cambiar las líneas en client.py de host = "localhost a:
```
host = "192.168.1.101"
ports = [12345, 12346]
```
6. Ejecuta worker1.py en la primera computadora de worker y worker2.py en la segunda computadora de worker. Estos programas ahora deberían estar escuchando conexiones entrantes.
7. Ejecuta client.py en la computadora cliente. El programa cliente debería conectarse a ambos workers y podrás comenzar a probar las funciones de ordenamiento.

### Funcionalidad:
El proyecto funciona utilizando sockets para comunicarse entre el cliente y dos trabajadores (worker1 y worker2) en diferentes archivos. El cliente envía solicitudes de ordenamiento de vectores a los trabajadores, que procesan la solicitud y devuelven el vector ordenado al cliente. La solución utiliza subprocesos (threads) para manejar múltiples conexiones en los trabajadores.

1. Cliente (client.py):
- El cliente solicita información al usuario, como el tamaño del vector, el algoritmo de ordenamiento y el tiempo límite para cada trabajador.
- Conecta a dos trabajadores utilizando sockets.
- Envía datos del problema al primer trabajador y espera el tiempo límite.
- Si el primer trabajador no termina a tiempo, el vector parcial se envía al segundo trabajador, y así sucesivamente hasta que el vector esté completamente ordenado.
- Muestra el vector ordenado y el tiempo total de ordenamiento.

2. Trabajadores (worker1.py y worker2.py):
- Ambos trabajadores son similares en estructura y funcionamiento, solo difieren en el ID del trabajador y el puerto en el que escuchan.
- Los trabajadores crean un socket y escuchan conexiones entrantes.
- Cuando se establece una conexión, se crea un nuevo hilo (thread) para manejar esa conexión, utilizando la función process_request.
- La función process_request recibe datos del cliente, extrae la información relevante y realiza el ordenamiento utilizando el algoritmo seleccionado (merge sort, heap sort o quick sort) importado desde utils.py.
- Si el tiempo de procesamiento excede el tiempo límite, el trabajador envía el vector parcialmente ordenado al otro trabajador, que continuará con el proceso.
- Una vez que el vector esté completamente ordenado, el trabajador envía el vector ordenado y el tiempo de procesamiento al cliente.

3. Módulo de utilidades (utils.py):
- Contiene las implementaciones de los algoritmos de ordenamiento: merge sort, heap sort y quick sort.
- También contiene funciones auxiliares para enviar y recibir datos a través de sockets.

El uso de subprocesos (threads) en los trabajadores permite manejar múltiples conexiones entrantes. En este caso, cada trabajador puede procesar solicitudes de ordenamiento de diferentes clientes de manera concurrente. Cuando un trabajador recibe una solicitud, crea un nuevo hilo y le pasa la conexión y la información relevante. Este enfoque asegura que el trabajador pueda seguir escuchando nuevas conexiones mientras procesa las solicitudes existentes.

### Recomendación y nota importante
Como el proyecto funciona creando nuevos Threads o hilos donde hay límites en la cantidad de hilos que se pueden crear en un sistema. Los límites provienen de varias fuentes, como la implementación del sistema operativo, la configuración del sistema y los recursos disponibles, como la memoria y la capacidad de la CPU, entonces es importante usar un tiempo limite adecuado ya que se podria llegar al limite de Threads, mientras menos tiempo le deja a un worker para que ordene va a pasar más veces el vector parcialmente ordenado al otro worker por lo que se creara mas hilos y podria llegar a un momento que se pasa del limite, es decir mientras más tiempo, más posibilidad de que un solo worker trabaje, y mientras menos tiempo le da pasarán el vector mas veces, entonces la recomendación es:

- Si quiere utilizar los algoritmos de MergeSort y HeapSort, utiliza un tiempo limite de 0.002s y con n = 1000 si quiere poner n mas grande es recomendable ampliar el tiempo para que pueda ver el proceso de comunicación entre workers.

- Para el QuickSort es recomendable utilizar un tiempo mucho mayor, ya que se dio cuenta que crea demasiados hilos por lo que el tiempo de 0.002s llegara al limite de hilos, por lo que para el Quicksort hay que buscar un buen tiempo para ver la comunicación que no se encontró, entonces la recomendación es utilizar segundos grandes que trabaje un solo worker solo para ver el ordenamiento.

Cabe resaltar que son vectores muy grandes de [1000, 100000], por lo que mientras mas grande sea el vector hay mas posibilidad de que tambien llegue al limite de hilos creados o que el programa se interrumpa, para no tener problema seria mejor darle mas tiempo a los wokers mientras mayor sea el vector, con el tiempo de 0.002s se recomienda probarlo con n = 1000.

### Bibliografia
- https://socket.io/docs/v4/
- https://docs.python.org/3/library/socket.html
- https://chat.openai.com/
- https://www.youtube.com/watch?v=nJYp3_X_p6c
- https://realpython.com/sorting-algorithms-python/