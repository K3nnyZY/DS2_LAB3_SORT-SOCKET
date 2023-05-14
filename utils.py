import socket
import json
import time
import random

def send_data(conn, data):
    """Envía datos a través de una conexión de socket.
    
    Args:
        conn: Conexión de socket.
        data: Datos a enviar.
    """
    try:
        msg = json.dumps(data).encode()
        conn.sendall(msg)
    except BrokenPipeError:
        print("Error al enviar datos: conexión rota.")


def recv_data(conn):
    """Recibe datos a través de una conexión de socket.
    
    Args:
        conn: Conexión de socket.
    
    Returns:
        Decodifica y devuelve los datos recibidos en formato JSON.
    """
    buffer_size = 16384
    data = b""
    while True:
        part = conn.recv(buffer_size)
        data += part
        if len(part) < buffer_size:
            break
    return json.loads(data.decode())


def merge_sort(arr, worker_id, other_worker_addr, start_time, time_limit):
    """Implementa el algoritmo de ordenamiento por mezcla (merge sort).
    
    Si el tiempo de ejecución excede el límite establecido, se pasa el vector al otro worker.
    
    Args:
        arr: Vector a ordenar.
        worker_id: Identificador del worker actual.
        other_worker_addr: Dirección del otro worker.
        start_time: Tiempo de inicio del proceso de ordenamiento.
        time_limit: Límite de tiempo para el proceso de ordenamiento.
    
    Returns:
        Vector ordenado.
    """
    if time.time() - start_time > time_limit:
        print(f"Worker {worker_id} excedió el tiempo límite. Pasando el vector al otro worker.")
        return pass_to_other_worker(arr, worker_id, other_worker_addr, start_time, time_limit, "1")

    if len(arr) <= 1:
        return arr

    middle = len(arr) // 2
    left = arr[:middle]
    right = arr[middle:]

    left = merge_sort(left, worker_id, other_worker_addr, start_time, time_limit)
    right = merge_sort(right, worker_id, other_worker_addr, start_time, time_limit)

    return merge(left, right, worker_id, other_worker_addr, start_time, time_limit)

def merge(left, right, worker_id, other_worker_addr, start_time, time_limit):
    """Combina dos subvectores ordenados en un vector ordenado.
    
    Args:
        left: Subvector izquierdo.
        right: Subvector derecho.
        worker_id: Identificador del worker actual.
        other_worker_addr: Dirección del otro worker.
        start_time: Tiempo de inicio del proceso de ordenamiento.
        time_limit: Límite de tiempo para el proceso de ordenamiento.
    
    Returns:
        Vector ordenado.
    """
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if time.time() - start_time > time_limit:
            return pass_to_other_worker(result + left[i:] + right[j:], worker_id, other_worker_addr, start_time, time_limit, "1")

        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result += left[i:]
    result += right[j:]
    return result

def heapify(arr, n, i):
    """Reorganiza un subárbol con raíz en el índice `i` en un montículo máximo (heap).

    Args:
        arr: Vector a reorganizar.
        n: Tamaño del montículo.
        i: Índice de la raíz del subárbol.
    """
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < n and arr[left] > arr[largest]:
        largest = left

    if right < n and arr[right] > arr[largest]:
        largest = right

    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)

def heap_sort(arr, worker_id, other_worker_addr, start_time, time_limit):
    """Implementa el algoritmo de ordenamiento por montículos (heap sort).

    Si el tiempo de ejecución excede el límite establecido, se pasa el vector al otro worker.

    Args:
        arr: Vector a ordenar.
        worker_id: Identificador del worker actual.
        other_worker_addr: Dirección del otro worker.
        start_time: Tiempo de inicio del proceso de ordenamiento.
        time_limit: Límite de tiempo para el proceso de ordenamiento.

    Returns:
        Vector ordenado.
    """
    n = len(arr)

    for i in range(n // 2 - 1, -1, -1):
        if time.time() - start_time > time_limit:
            print(f"Worker {worker_id} excedió el tiempo límite. Pasando el vector al otro worker.")
            return pass_to_other_worker(arr, worker_id, other_worker_addr, start_time, time_limit, "2")
        heapify(arr, n, i)

    for i in range(n - 1, 0, -1):
        if time.time() - start_time > time_limit:
            return pass_to_other_worker(arr, worker_id, other_worker_addr, start_time, time_limit, "2")
        arr[i], arr[0] = arr[0], arr[i]
        heapify(arr, i, 0)

    return arr

def quick_sort(arr, low, high, worker_id, other_worker_addr, start_time, time_limit, pivot_type):
    """Implementa el algoritmo de ordenamiento rápido (quick sort) con diferentes tipos de pivotes.

    Si el tiempo de ejecución excede el límite establecido, se pasa el vector al otro worker.

    Args:
        arr: Vector a ordenar.
        low: Índice inferior del rango de ordenamiento.
        high: Índice superior del rango de ordenamiento.
        worker_id: Identificador del worker actual.
        other_worker_addr: Dirección del otro worker.
        start_time: Tiempo de inicio del proceso de ordenamiento.
        time_limit: Límite de tiempo para el proceso de ordenamiento.
        pivot_type: Tipo de pivote a utilizar (1 - primer elemento, 2 - último elemento, 3 - elemento aleatorio).

    Returns:
        Vector ordenado.
    """
    if low < high:
        if time.time() - start_time > time_limit:
            print(f"Worker {worker_id} excedió el tiempo límite. Pasando el vector al otro worker.")
            return pass_to_other_worker(arr, worker_id, other_worker_addr, start_time, time_limit, "3", low, high, pivot_type)

        pivot_index = partition(arr, low, high, pivot_type)
        quick_sort(arr, low, pivot_index, worker_id, other_worker_addr, start_time, time_limit, pivot_type)
        quick_sort(arr, pivot_index + 1, high, worker_id, other_worker_addr, start_time, time_limit, pivot_type)

    return arr


def partition(arr, low, high, pivot_type):
    """Función de partición para el algoritmo de ordenamiento rápido (quick sort).

    Args:
        arr: Vector a ordenar.
        low: Índice inferior del rango de ordenamiento.
        high: Índice superior del rango de ordenamiento.
        pivot_type: Tipo de pivote a utilizar (1 - primer elemento, 2 - último elemento, 3 - elemento aleatorio).

    Returns:
        Índice del pivote en su posición ordenada.
    """
    if pivot_type == "3":
        pivot_index = random.randint(low, high - 1)
    else:
        pivot_index = low if pivot_type == "1" else high
    pivot = arr[pivot_index]
    arr[pivot_index], arr[low] = arr[low], arr[pivot_index]
    i = low + 1
    j = high - 1
    while True:
        while i <= j and arr[i] < pivot:
            i += 1
        while i <= j and arr[j] >= pivot:
            j -= 1
        if i <= j:
            arr[i], arr[j] = arr[j], arr[i]
        else:
            break
    arr[low], arr[j] = arr[j], arr[low]
    return j


def pass_to_other_worker(arr, worker_id, other_worker_addr, start_time, time_limit, algorithm, low=None, high=None, pivot_type=None, connection_count=0):
    """Pasa el vector a otro worker para continuar el proceso de ordenamiento.

    Args:
        arr: Vector a ordenar.
        worker_id: Identificador del worker actual.
        other_worker_addr: Dirección del otro worker.
        start_time: Tiempo de inicio del proceso de ordenamiento.
        time_limit: Límite de tiempo para el proceso de ordenamiento.
        algorithm: Algoritmo de ordenamiento utilizado (1 - merge sort, 2 - heap sort, 3 - quick sort).
        low: Índice inferior del rango de ordenamiento (para quick sort).
        high: Índice superior del rango de ordenamiento (para quick sort).
        pivot_type: Tipo de pivote a utilizar (para quick sort).
        connection_count: Contador de conexiones entre workers.

    Returns:
        Vector ordenado parcialmente.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(other_worker_addr)

        data = {
            "a": arr,
            "b": algorithm,
            "c": float(time_limit),
            "d": pivot_type,
            "e": low,
            "f": high,
            "g": connection_count
        }

        send_data(s, data)
        print(f"\nWorker {worker_id} pasó el vector al otro worker. Esperando resultados...")
        received_data = recv_data(s)
        print(f"\nWorker {worker_id} recibió el vector ordenado parcialmente del otro worker.")
        return received_data["vector"]