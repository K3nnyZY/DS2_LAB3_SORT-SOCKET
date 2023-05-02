import time
import random
import json
import heapq

def merge_sort(arr, conn, other_worker_addr, start_time, time_limit):
    if time.time() - start_time > time_limit:
        send_data(conn, {"vector": arr, "other_worker": other_worker_addr})
        response = recv_data(conn)
        return response["vector"]

    if len(arr) > 1:
        mid = len(arr) // 2
        left = arr[:mid]
        right = arr[mid:]

        left = merge_sort(left, conn, other_worker_addr, start_time, time_limit)
        right = merge_sort(right, conn, other_worker_addr, start_time, time_limit)

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

def heap_sort(arr, conn, other_worker_addr, start_time, time_limit):
    if time.time() - start_time > time_limit:
        send_data(conn, {"vector": arr, "other_worker": other_worker_addr})
        response = recv_data(conn)
        return response["vector"]

    heapq.heapify(arr)

    sorted_arr = []
    while arr:
        sorted_arr.append(heapq.heappop(arr))

        if time.time() - start_time > time_limit:
            break

    return sorted_arr

def quick_sort(arr, low, high, conn, other_worker_addr, start_time, time_limit):
    if time.time() - start_time > time_limit:
        send_data(conn, {"vector": arr, "other_worker": other_worker_addr})
        response = recv_data(conn)
        return response["vector"]

    if low < high:
        pivot_index = partition(arr, low, high)
        quick_sort(arr, low, pivot_index, conn, other_worker_addr, start_time, time_limit)
        quick_sort(arr, pivot_index + 1, high, conn, other_worker_addr, start_time, time_limit)

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
    msg = json.dumps(data).encode()
    conn.sendall(msg)

def recv_data(conn):
    buffer_size = 4096
    data = b""
    while True:
        part = conn.recv(buffer_size)
        data += part
        if len(part) < buffer_size:
            break

    return json.loads(data.decode())
