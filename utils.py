import socket
import json
import time
import random

def send_data(conn, data):
    try:
        msg = json.dumps(data).encode()
        conn.sendall(msg)
    except BrokenPipeError:
        print("Error al enviar datos: conexión rota.")


def recv_data(conn):
    buffer_size = 16384
    data = b""
    while True:
        part = conn.recv(buffer_size)
        data += part
        if len(part) < buffer_size:
            break
    return json.loads(data.decode())


def merge_sort(arr, worker_id, other_worker_addr, start_time, time_limit):
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

def quick_sort(arr, low, high, worker_id, other_worker_addr, start_time, time_limit, pivot_type, connection_count, max_connections):
    if connection_count >= max_connections:
        raise Exception(f"Se alcanzó el límite máximo de conexiones ({max_connections}). Deteniendo la ejecución.")
    if low < high:
        if time.time() - start_time > time_limit:
            print(f"Worker {worker_id} excedió el tiempo límite. Pasando el vector al otro worker.")
            return pass_to_other_worker(arr, worker_id, other_worker_addr, start_time, time_limit, "3", low, high, pivot_type, connection_count)

        pivot_index = partition(arr, low, high, pivot_type)
        quick_sort(arr, low, pivot_index, worker_id, other_worker_addr, start_time, time_limit, pivot_type, connection_count, max_connections)
        quick_sort(arr, pivot_index + 1, high, worker_id, other_worker_addr, start_time, time_limit, pivot_type, connection_count, max_connections)

    return arr


def partition(arr, low, high, pivot_type):
    if pivot_type == "3":
        pivot_index = random.randint(low, high - 1)
        pivot = arr[pivot_index]
        arr[pivot_index], arr[low] = arr[low], arr[pivot_index]
    else:
        pivot = arr[low]

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