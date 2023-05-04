import socket
import json
import time
import threading
from utils import merge_sort, heap_sort, quick_sort, send_data, recv_data

def process_request(conn, addr, worker_id, other_worker_addr):
    while True:
        try:
            data = recv_data(conn)
            if not data:
                break

            print(f"Worker {worker_id} recibió datos del cliente: {data}")

            vector = data.get("a", [])
            algoritmo = data["b"]
            tiempo_limite = data.get("c", 0)
            pivot_type = data.get("d", "1")

            if algoritmo == "1":
                start_time = time.time()
                vector = merge_sort(vector, worker_id, other_worker_addr, start_time, tiempo_limite)
                end_time = time.time()
            elif algoritmo == "2":
                start_time = time.time()
                vector = heap_sort(vector, worker_id, other_worker_addr, start_time, tiempo_limite)
                end_time = time.time()
            elif algoritmo in ("3", "4"):
                start_time = time.time()
                vector = quick_sort(vector, 0, len(vector) - 1, worker_id, other_worker_addr, start_time, tiempo_limite, pivot_type)
                end_time = time.time()

            tiempo = round(end_time - start_time, 5)

            response = {"worker_id": worker_id, "tiempo": tiempo, "vector": vector}
            send_data(conn, response)

        except (json.decoder.JSONDecodeError, ConnectionResetError):
            print(f"El cliente {addr} se ha desconectado.")
            break

    conn.close()

def start_worker(worker_id, host, port, other_worker_addr):
    s = socket.socket()
    s.bind((host, port))
    s.listen(5)
    print(f"Worker {worker_id} iniciado y escuchando en el puerto {port}.")

    while True:
        conn, addr = s.accept()
        print(f"Conexión establecida con {addr}")

        thread = threading.Thread(target=process_request, args=(conn, addr, worker_id, other_worker_addr))
        thread.start()

if __name__ == "__main__":
    worker_id = 2
    host = "0.0.0.0"
    port = 12346
    other_worker_addr = ("127.0.0.1", 12345)  # Cambia la dirección IP y el puerto según su configuración
    start_worker(worker_id, host, port, other_worker_addr)
