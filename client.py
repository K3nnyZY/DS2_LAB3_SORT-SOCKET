import random
import socket
import json
import time

def leer_tiempo_limite():
    t = float(input("\nIngrese el tiempo límite para cada worker en segundos: "))
    while t <= 0:
        print("El tiempo límite debe ser mayor a 0.")
        t = float(input("\nIngrese el tiempo límite para cada worker en segundos: "))
    return t

def conectar_a_servidor(host, port1, port2, s1, s2):
    s1.connect((host, port1))
    s2.connect((host, port2))

def send_data(sock, data):
    print(f"\nenviando datos a worker {data['worker_id']} ...")
    msg = json.dumps(data).encode()
    sock.sendall(msg)

def recv_data(sock):
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

def generate_random_vector(n):
    min_value = 1
    max_value = 1000000
    return [random.randint(min_value, max_value) for _ in range(n)]

def leer_vector():
    n = int(input("\nIngrese el tamaño del vector a generar (entre 1000 y 1000000): "))
    while n < 1000 or n > 1000000:
        print("El tamaño del vector debe estar entre 1000 y 1000000.")
        n = int(input("\nIngrese el tamaño del vector a generar (entre 1000 y 1000000): "))
    return generate_random_vector(n)

def escoger_algoritmo():
    print("Escoja entre los algoritmos de ordenamiento:"+
          "\n1. MergeSort.\n2. HeapSort.\n3. QuickSort.\n4. Terminar programa")
    opc = (input("Ingrese su opción: ")).strip()

    while opc not in ("1", "2", "3", "4"):
        print("Opción inválida. Intente de nuevo.")
        opc = (input("\nIngrese su opción: ")).strip()

    return opc


try:
    host = "localhost"
    port1 = 12345
    port2 = 12346
    s1 = socket.socket()
    s2 = socket.socket()
    conectar_a_servidor(host, port1, port2, s1, s2)

    time_limit = leer_tiempo_limite()

    while True:
        # Lee el vector y valida que esté compuesto únicamente por números
        v = leer_vector()

        opc = escoger_algoritmo()

        if opc == "4":
            print("Terminando programa...")
            break

        else:
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

        success = False
        total_time = 0
        current_worker = 1
        while not success:
            data["worker_id"] = current_worker
            if current_worker == 1:
                send_data(s1, data)
            else:
                send_data(s2, data)

            # Esperar el límite de tiempo
            time.sleep(time_limit)

            # Recibir el resultado del worker actual
            worker_result = recv_data(s1) if current_worker == 1 else recv_data(s2)
            if 'tiempo' not in worker_result:
                print("Error: 'tiempo' no encontrado en los datos recibidos")
                continue

            if worker_result["tiempo"] <= time_limit:
                # Si el worker actual finalizó a tiempo
                sorted_array = worker_result["vector"]
                total_time += worker_result["tiempo"]
                success = True
            else:
                # Si el worker actual no finalizó a tiempo, cambiar al otro worker
                total_time += worker_result["tiempo"]
                data["a"] = worker_result["vector"]  # Enviar el vector parcial
                current_worker = 2 if current_worker == 1 else 1

        print("\nresultado final")
        print("Array ordenado:", sorted_array)
        print("\nTiempo total de ordenamiento: {:.5f} segundos".format(total_time))

    print("\nEl programa ha sido interrumpido.")
    print("Cerrando conexión y liberando el puerto.\n")

except KeyboardInterrupt:
    # Para cerrar todo por si acaso
    print("\n----------------------------\n")
    print("El programa ha sido interrumpido de forma repentina.")
    print("Cerrando conexión y liberando el puerto.\n")

except ConnectionRefusedError:
    print("\nLa conexión ha sido negada. Revise si los servidores está corriendo.\n")

except json.decoder.JSONDecodeError or ConnectionResetError:
    print("\n-----------------------------\n")
    print("El servidor ha dejado de responder")
    print("Cerrando conexión y liberando el puerto.\n")

finally:
    s1.close()
    s2.close()
