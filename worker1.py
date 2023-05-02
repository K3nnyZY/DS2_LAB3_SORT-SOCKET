import socket
import json
import time
import threading
from utils import merge_sort, heap_sort, quick_sort, send_data, recv_data

def process_request(conn, addr, other_worker_addr):
    while True:
        try:
            data = recv_data(conn)
            if not data:
                break

            vector = data["a"]
            algoritmo = data["b"]
            tiempo_limite = data["c"]

            if algoritmo == "1":
                start_time = time.time()
                vector = merge_sort(vector, conn, other_worker_addr, start_time, tiempo_limite)
                end_time = time.time()
            elif algoritmo == "2":
                start_time = time.time()
                vector = heap_sort(vector, conn, other_worker_addr, start_time, tiempo_limite)
                end_time = time.time()
            elif algoritmo == "3":
                start_time = time.time()
                vector = quick_sort(vector, 0, len(vector) - 1, conn, other_worker_addr, start_time, tiempo_limite)
                end_time = time.time()

            tiempo = round(end_time - start_time, 5)

            response = {"Flag": tiempo, "arr": vector}
            send_data(conn, response)

        except (json.decoder.JSONDecodeError, ConnectionResetError):
            print(f"El cliente {addr} se ha desconectado.")
            break

    conn.close()

class Worker:
    def __init__(self, other_worker_addr):
        self.s = socket.socket()
        self.host = "0.0.0.0"
        self.port = 12345
        self.other_worker_addr = other_worker_addr

    def start(self):
        self.s.bind((self.host, self.port))
        self.s.listen(5)
        print(f"El worker1 está corriendo en {self.host}:{self.port}")

        while True:
            conn, addr = self.s.accept()
            print(f"Conexión establecida con {addr}")

            thread = threading.Thread(target=process_request, args=(conn, addr, self.other_worker_addr))
            thread.start()

if __name__ == "__main__":
    other_worker_addr = ("127.0.0.1", 12346)  # Cambie la dirección IP y el puerto según su configuración
    worker1 = Worker(other_worker_addr)
    worker1.start()