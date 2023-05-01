import json

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
    
    result += left[i:]
    result += right[j:]

    return result


def merge_sort(arr, conn):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = arr[:mid]
    right = arr[mid:]

    left = merge_sort(left, conn)
    right = merge_sort(right, conn)

    sorted_arr = merge(left, right)

    response = {"Flag": "Bandera", "arr": sorted_arr, "Side": "Merge"}
    conn.send(json.dumps(response).encode())
    conn.recv(1024)

    return sorted_arr


def heapify(arr, n, i, conn):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < n and arr[left] > arr[largest]:
        largest = left

    if right < n and arr[right] > arr[largest]:
        largest = right

    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest, conn)

        response = {"Flag": "Bandera", "arr": arr}
        conn.send(json.dumps(response).encode())
        conn.recv(1024)


def heap_sort(arr, conn):
    n = len(arr)

    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i, conn)

    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        heapify(arr, i, 0, conn)

    return arr


def partition(arr, low, high, conn, pivot_type):
    if pivot_type == "3":
        pivot = arr[low]
    elif pivot_type == "4":
        pivot = arr[high]

    i = low
    j = high

    while True:
        while arr[i] < pivot:
            i += 1

        while arr[j] > pivot:
            j -= 1

        if i <= j:
            arr[i], arr[j] = arr[j], arr[i]
            i += 1
            j -= 1
        else:
            break

    response = {"Flag": "Bandera", "arr": arr}
    conn.send(json.dumps(response).encode())
    conn.recv(1024)

    return i


def _quick_sort(arr, low, high, conn, pivot_type):
    if low < high:
        pi = partition(arr, low, high, conn, pivot_type)

        _quick_sort(arr, low, pi - 1, conn, pivot_type)
        _quick_sort(arr, pi, high, conn, pivot_type)


def quick_sort(arr, conn, pivot_type):
    low = 0
    high = len(arr) - 1
    _quick_sort(arr, low, high, conn, pivot_type)
    return arr
