import random
import socket
import pickle
from workers import run_workers, create_worker_socket, send_data_to_worker, receive_data_from_worker

def generate_random_vector(n):
    return [random.randint(1, 1000000) for _ in range(n)]

def client(vector, sorting_algorithm, pivot=None):
    data_to_send = {
        'vector': vector,
        'sorting_algorithm': sorting_algorithm,
        'pivot': pivot
    }

    worker1_socket = create_worker_socket()
    send_data_to_worker(worker1_socket, data_to_send)
    worker1_result = receive_data_from_worker(worker1_socket)

    if worker1_result['finished']:
        return worker1_result['sorted_vector'], worker1_result['time_taken']

    worker2_socket = create_worker_socket()
    send_data_to_worker(worker2_socket, worker1_result)
    worker2_result = receive_data_from_worker(worker2_socket)

    return worker2_result['sorted_vector'], worker2_result['time_taken']

def main():
    print("Seleccione el algoritmo de ordenamiento:")
    print("1. MergeSort")
    print("2. HeapSort")
    print("3. QuickSort")
    option = int(input("Opción: "))

    n = int(input("Ingrese el tamaño del vector (entre 1000 y 1000000): "))
    vector = generate_random_vector(n)

    Z = float(input("Ingrese el tiempo límite (en segundos) para cada worker: "))

    if option == 1:
        sorted_vector, time_taken = client(vector, 'merge_sort')
    elif option == 2:
        sorted_vector, time_taken = client(vector, 'heap_sort')
    elif option == 3:
        pivot = input("Seleccione el pivote para QuickSort (left/right): ")
        sorted_vector, time_taken = client(vector, 'quick_sort', pivot)
    else:
        raise ValueError("Invalid option")

    # Mostrar los resultados
    print("Vector ordenado:", sorted_vector)
    print("Tiempo de procesamiento:", time_taken)

if __name__ == "__main__":
    main()
