import socket
import json
import time
import threading
from sorting_algortihms import merge_sort, heap_sort, quick_sort

def process_request(conn, addr):
    while True:
        try:
            data = conn.recv(1024)
            if not data:
                break

            data = json.loads(data.decode())
            vector = data["a"]
            algoritmo = data["b"]

            if algoritmo == "5":
                print(f"El cliente {addr} ha decidido salir.")
                break

            print(f"\nCliente {addr}: Vector recibido: {vector}")
            print(f"Cliente {addr}: Algoritmo seleccionado: {algoritmo}")

            if algoritmo == "1":
                start_time = time.time()
                vector = merge_sort(vector, conn)
                end_time = time.time()
                algoritmo_nombre = "Merge Sort"
            elif algoritmo == "2":
                start_time = time.time()
                vector = heap_sort(vector, conn)
                end_time = time.time()
                algoritmo_nombre = "Heap Sort"
            elif algoritmo in ("3", "4"):
                start_time = time.time()
                vector = quick_sort(vector, conn, algoritmo)
                end_time = time.time()
                algoritmo_nombre = "Quick Sort"
            else:
                raise ValueError("Algoritmo no válido")

            tiempo = round(end_time - start_time, 5)

            print(f"Cliente {addr}: Vector ordenado usando {algoritmo_nombre}: {vector}")
            print(f"Cliente {addr}: Tiempo de ejecución: {tiempo} segundos")

            response = {"Flag": tiempo, "arr": vector}
            conn.send(json.dumps(response).encode())

        except (json.decoder.JSONDecodeError, ConnectionResetError):
            print(f"El cliente {addr} se ha desconectado.")
            break
        except ValueError as e:
            print(e)
            break

    conn.close()


class Server:
    def __init__(self):
        self.s = socket.socket()
        self.host = ""
        self.port = 12345

    def start(self):
        self.s.bind((self.host, self.port))
        self.s.listen(5)
        print(f"El servidor está corriendo en {self.host}:{self.port}\n")

        while True:
            conn, addr = self.s.accept()
            print(f"Conexión establecida con {addr}")

            thread = threading.Thread(target=process_request, args=(conn, addr))
            thread.start()


if __name__ == "__main__":
    server = Server()
    server.start()
