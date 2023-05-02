import time
import random
import json
import heapq
import socket


def is_sorted(arr):
    return all(arr[i] <= arr[i + 1] for i in range(len(arr) - 1))


def send_data_to_other_worker(worker_id, other_worker_addr, vector):
    if is_sorted(vector):
        print(f"Worker {worker_id}: Vector is already sorted. Not sending to other worker.")
        return vector

    print(f"Worker {worker_id}: Sending data to other worker at {other_worker_addr}")
    with socket.socket() as other_worker_conn:
        other_worker_conn.connect(other_worker_addr)
        send_data(other_worker_conn, {"a": vector, "b": "1", "c": 0})
        response = recv_data(other_worker_conn)
        sorted_vector = response["arr"]
        print(f"Worker {worker_id}: Received sorted data from other worker at {other_worker_addr}: {sorted_vector}")
        return sorted_vector


def merge_sort(arr, worker_id, other_worker_addr, start_time, time_limit):
    if time.time() - start_time > time_limit:
        print(f"Worker {worker_id}: Tiempo límite alcanzado en merge_sort, enviando al otro worker...")
        return send_data_to_other_worker(worker_id, other_worker_addr, arr)

    if len(arr) > 1:
        mid = len(arr) // 2
        left = arr[:mid]
        right = arr[mid:]

        left = merge_sort(left, worker_id, other_worker_addr, start_time, time_limit)
        right = merge_sort(right, worker_id, other_worker_addr, start_time, time_limit)

        arr = merge(left, right)

    return arr


def merge(left, right):
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])

    return result


def heap_sort(arr, worker_id, other_worker_addr, start_time, time_limit):
    if time.time() - start_time > time_limit:
        print(f"Worker {worker_id}: Tiempo límite alcanzado en heap_sort, enviando al otro worker...")
        return send_data_to_other_worker(worker_id, other_worker_addr, arr)

    heapq.heapify(arr)

    sorted_arr = []
    while arr:
        sorted_arr.append(heapq.heappop(arr))

        if time.time() - start_time > time_limit:
            break
    return sorted_arr


def quick_sort(arr, low, high, worker_id, other_worker_addr, start_time, time_limit):
    if time.time() - start_time > time_limit:
        print(f"Worker {worker_id}: Tiempo límite alcanzado en quick_sort, enviando al otro worker...")
        return send_data_to_other_worker(worker_id, other_worker_addr, arr)

    if low < high:
        pivot_index = partition(arr, low, high)
        quick_sort(arr, low, pivot_index, worker_id, other_worker_addr, start_time, time_limit)
        quick_sort(arr, pivot_index + 1, high, worker_id, other_worker_addr, start_time, time_limit)
    return arr


def partition(arr, low, high):
    pivot = arr[low]
    left = low + 1
    right = high
    done = False

    while not done:
        while left <= right and arr[left] <= pivot:
            left += 1

        while arr[right] >= pivot and right >= left:
            right -= 1

        if right < left:
            done = True
        else:
            arr[left], arr[right] = arr[right], arr[left]

    arr[low], arr[right] = arr[right], arr[low]

    return right


def generate_vector(n):
    vector = [random.randint(1, 1000000) for _ in range(n)]
    return vector


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

    try:
        return json.loads(data.decode())
    except json.JSONDecodeError:
        print("Error al decodificar los datos recibidos.")
        return {}  # Retorna un diccionario vacío como valor predeterminado


