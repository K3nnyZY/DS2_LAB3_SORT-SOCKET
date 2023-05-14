import socket
import json
import time
import threading
from utils import merge_sort, heap_sort, quick_sort, send_data, recv_data

def process_request(conn, addr, worker_id, other_worker_addr):
    """Procesa las solicitudes entrantes de los clientes.

    Args:
        conn: Conexión al cliente.
        addr: Dirección del cliente.
        worker_id: Identificador del worker actual.
        other_worker_addr: Dirección del otro worker.
    """
    while True:
        try:
            data = recv_data(conn)
            if not data:
                break

            print(f"Worker {worker_id}: Datos recibidos del cliente: {data}")

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
            print(f"Worker {worker_id}: El cliente en la dirección {addr} se ha desconectado.")
            break

    conn.close()

def start_worker(worker_id, host, port, other_worker_addr):
    """Inicia un worker y escucha las solicitudes de los clientes.

    Args:
        worker_id: Identificador del worker actual.
        host: Dirección IP del host del worker.
        port: Puerto en el que el worker escuchará las conexiones.
        other_worker_addr: Dirección del otro worker.
    """
    s = socket.socket()
    s.bind((host, port))
    s.listen(5)
    print(f"Worker {worker_id} ha iniciado y está escuchando en el puerto {port}. Esperando conexiones...")

    while True:
        conn, addr = s.accept()
        print(f"Worker {worker_id}: Conexión establecida con el cliente en la dirección {addr}")

        thread = threading.Thread(target=process_request, args=(conn, addr, worker_id, other_worker_addr))
        thread.start()

if __name__ == "__main__":
    worker_id = 2
    host = "0.0.0.0"
    port = 12346
    other_worker_addr = ("127.0.0.1", 12345)  # Cambia la dirección IP y el puerto según su configuración
    start_worker(worker_id, host, port, other_worker_addr)