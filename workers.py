# workers.py

import threading
import socket
import pickle
from sorting_algorithms import merge_sort, heap_sort, quick_sort

def timed_worker_process(worker_func, args, timeout):
    result = []

    def worker_wrapper():
        nonlocal result
        result.append(worker_func(*args))

    timer = threading.Timer(timeout, worker_wrapper)
    timer.start()
    timer.join()

    return result[0] if result else None

def worker(data):
    arr = data['vector']
    sorting_algorithm = data['sorting_algorithm']
    pivot = data.get('pivot')

    if sorting_algorithm == 'merge_sort':
        return merge_sort(arr)
    elif sorting_algorithm == 'heap_sort':
        return heap_sort(arr)
    elif sorting_algorithm == 'quick_sort':
        return quick_sort(arr, pivot)
    else:
        raise ValueError("Invalid sorting algorithm")

def run_worker_with_timeout(data, timeout):
    result = timed_worker_process(worker, (data,), timeout)
    return result if result else (data['vector'], False)

def run_workers(data, timeout):
    worker1_result, worker2_result = None, None
    while not worker1_result or not worker2_result:
        worker1_result = run_worker_with_timeout(data, timeout)
        if worker1_result[1]:
            return worker1_result
        worker2_result = run_worker_with_timeout(data, timeout)
        if worker2_result[1]:
            return worker2_result
    return None

def create_worker_socket():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('localhost', 12346))
        return s

def send_data_to_worker(worker_socket, data):
    serialized_data = pickle.dumps(data)
    worker_socket.sendall(serialized_data)

def receive_data_from_worker(worker_socket):
    received_data = worker_socket.recv(1024)
    deserialized_data = pickle.loads(received_data)
    return deserialized_data
