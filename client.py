import random
import socket
import json
import time

class Client:
    def __init__(self):
        self.s1 = socket.socket()
        self.s2 = socket.socket()

    def leer_tiempo_limite(self):
        t = float(input("\nIngrese el tiempo límite para cada worker en segundos: "))
        while t <= 0:
            print("El tiempo límite debe ser mayor a 0.")
            t = float(input("\nIngrese el tiempo límite para cada worker en segundos: "))
        return t

    def conectar_a_servidor(self, host, port1, port2):
        self.s1.connect((host, port1))
        self.s2.connect((host, port2))

    def send_data(self, sock, data):
        print(f"\nenviando datos a worker {data['worker_id']} ...")
        msg = json.dumps(data).encode()
        sock.sendall(msg)

    def recv_data(self, sock):
        buffer_size = 16384
        data = b""
        while True:
            part = sock.recv(buffer_size)
            data += part
            if len(part) < buffer_size:
                break
        decoded_data = json.loads(data.decode())
        if 'worker_id' not in decoded_data:
            print("Error: 'worker_id' no encontrado en datos recibidos")
        else:
            print(f"\ndatos recibidos del worker {decoded_data['worker_id']}: {decoded_data}")
        return decoded_data

    def generate_random_vector(self, n):
        min_value = 1
        max_value = 1000000
        return [random.randint(min_value, max_value) for _ in range(n)]

    def leer_vector(self, v):
        n = int(input("\nIngrese el tamaño del vector a generar (entre 1000 y 1000000): "))
        while n < 1000 or n > 1000000:
            print("El tamaño del vector debe estar entre 1000 y 1000000.")
            n = int(input("\nIngrese el tamaño del vector a generar (entre 1000 y 1000000): "))
        v.extend(self.generate_random_vector(n))

    def escoger_algoritmo(self):
        print("Escoja entre los algoritmos de ordenamiento:"+
              "\n1. MergeSort.\n2. HeapSort.\n3. QuickSort.")
        opc = (input("Ingrese su opción: ")).strip()

        while opc not in ("1", "2", "3"):
            print("Opción inválida. Intente de nuevo.")
            opc = (input("\nIngrese su opción: ")).strip()

        return opc

try:
    client = Client()
    host = "localhost"
    port1 = 12345
    port2 = 12346
    client.conectar_a_servidor(host, port1, port2)

    time_limit = client.leer_tiempo_limite()

    while True:
        # Lee el vector y valida que esté compuesto únicamente por números
        v = []
        client.leer_vector(v)

        if len(v) < 1:
            # Si desea cerrar el programa
            data = json.dumps({"a": 1, "b": "5"})
            client.send_data(client.s1, data)
            client.send_data(client.s2, data)
            break

        else:
            opc = client.escoger_algoritmo()
            print("\nArray original:", v)

            algoritmo = {
                "1": "MergeSort",
                "2": "HeapSort",
                "3": "QuickSort"
            }
            print("\n* Ejecutando {} *\n".format(algoritmo[opc]))
            if opc == "3":
                pivote = input("Seleccione su pivote (1/Izquierda o 2/Derecha): ").strip()
                while pivote not in("1", "2"):
                    print("La opción ingresada es inválida. Intente de nuevo.")
                    pivote = input("\nSeleccione su pivote (1/Izquierda o 2/Derecha): ").strip()
            else:
                pivote = None
            data = {"a": v, "b": opc, "c": float(time_limit), "d": pivote}

        time.sleep(0.1)
        data["worker_id"] = 1
        client.send_data(client.s1, data)

        # Esperar el límite de tiempo
        time.sleep(time_limit)

        # Recibir el resultado del primer worker
        worker1_result = client.recv_data(client.s1)
        if 'tiempo' not in worker1_result:
            print("Error: 'tiempo' no encontrado en los datos recibidos")
            continue

        if worker1_result["tiempo"] <= time_limit:
            # Si el primer worker finalizó a tiempo
            sorted_array = worker1_result["vector"]
            total_time = worker1_result["tiempo"]
        else:
            # Si el primer worker no finalizó a tiempo, enviar la data parcialmente ordenada al segundo worker
            time.sleep(0.1)
            data["worker_id"] = 2
            data["a"] = worker1_result["vector"]  # Enviar el vector parcialmente ordenado
            client.send_data(client.s2, data)

            # Recibir el resultado del segundo worker
            worker2_result = client.recv_data(client.s2)
            if 'tiempo' not in worker2_result:
                print("Error: 'tiempo' no encontrado en los datos recibidos")
                continue

            sorted_array = worker2_result["vector"]
            total_time = worker1_result["tiempo"] + worker2_result["tiempo"]

        print("\nresultado final")
        print("Array ordenado:", sorted_array)
        print("T\niempo total de ordenamiento: {:.5f} segundos".format(total_time))

    print("\nEl programa ha sido interrumpido.")
    print("Cerrando conexión y liberando el puerto.\n")

except KeyboardInterrupt:
    # Para cerrar todo por si acaso
    print("\n* * * * * * * * * * * * *\n")
    print("El programa ha sido interrumpido de forma repentina.")
    print("Cerrando conexión y liberando el puerto.\n")

except ConnectionRefusedError:
    print("\nLa conexión ha sido negada. Revise si el servidor está corriendo.\n")

except json.decoder.JSONDecodeError or ConnectionResetError:
    print("\n* * * * * * * * * * * * *\n")
    print("El servidor ha dejado de responder")
    print("Cerrando conexión y liberando el puerto.\n")

finally:
    client.s1.close()
    client.s2.close()