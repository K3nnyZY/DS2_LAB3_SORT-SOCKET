# Socket y Ordenamiento

## Integrantes:
- Kenny Zhu
- Juan Aragon
- Tomas Cervera

## Laboratorio:
En este laboratorio su tarea es investigar cómo funcionan los sockets en Java o Python y usarlos para resolver lo siguiente:
Se desea tener un computador corriendo un programa y que sea el cliente, al comienzo del programa debe preguntarle al usuario qué problema quiere resolver. Los problemas a resolver son:
● Dado un vector de n posiciones, ordenarlo de manera ascendente usando el algoritmo de mergesort
● Dado un vector de n posiciones, ordenarlo de manera ascendente usando el algoritmo de heapsort
● Dado un vector de n posiciones, ordenarlo de manera ascendente usando el algoritmo de quicksort. El pivote inicial debe poderse escoger (las opciones son, el más a la izquierda o el más a la derecha).
Nota: Puede crear los vectores de manera aleatoria pero piense en valores de n grandes, entre 1000 y 1000000.
Una vez decidido el problema a resolver este debe ser mandado a otro computador (distinto del cliente) llamado worker_# el cual junto con la ayuda de otro worker_#, deben ordenar el vector. Cada worker contara con un tiempo Z para poder resolver hasta donde pueda del problema, si en el tiempo Z el worker que actualmente tiene el vector no ha terminado la tarea debe mandar el vector como lo lleve al otro worker y este debe continuar el trabajo. Una vez resuelto el problema, el cliente worker que haya terminado el problema de devolver el vector ordenado al cliente junto con el tiempo que le tomó resolverlo. Finalmente, esta información debe ser mostrada por el cliente.
