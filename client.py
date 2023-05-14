import random
import socket
import json
import time

def leer_tiempo_limite():
    """Lee el tiempo límite para cada worker en segundos."""
    t = float(input("\nIngrese el tiempo límite para cada worker en segundos: "))
    while t <= 0:
        print("El tiempo límite debe ser mayor a 0.")
        t = float(input("\nIngrese el tiempo límite para cada worker en segundos: "))
    return t

def conectar_a_servidor(host, port, s):
    """Conecta al cliente a dos workers.

    Args:
        host: Dirección IP del host de los workers.
        port1: Puerto del primer worker.
        port2: Puerto del segundo worker.
        s1: Socket del primer worker.
        s2: Socket del segundo worker.
    """
    s.connect((host, port))
    print(f"Conectado al servidor en {host}:{port}")

def send_data(sock, data):
    """Envía datos al worker correspondiente.

    Args:
        sock: Socket del worker al que se enviarán los datos.
        data: Datos a enviar al worker.
    """
    print(f"\nEnviando datos al worker {data['worker_id']}...")
    msg = json.dumps(data).encode()
    sock.sendall(msg)

def recv_data(sock):
    """Recibe datos del worker.

    Args:
        sock: Socket del worker del que se recibirán los datos.

    Returns:
        decoded_data: Datos recibidos del worker.
    """
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
        print(f"\nDatos recibidos del worker {decoded_data['worker_id']}: {decoded_data}")
    return decoded_data

def send_data_to_worker(sockets, worker_id, data):
    """Envía datos al worker correspondiente.

    Args:
        sockets: Lista de sockets de los workers.
        worker_id: ID del worker al que se enviarán los datos.
        data: Datos a enviar al worker.
    """
    send_data(sockets[worker_id - 1], data)

def recv_data_from_worker(sockets, worker_id):
    """Recibe datos del worker.

    Args:
        sockets: Lista de sockets de los workers.
        worker_id: ID del worker del que se recibirán los datos.

    Returns:
        decoded_data: Datos recibidos del worker.
    """
    return recv_data(sockets[worker_id - 1])

def generate_random_vector(n):
    """Genera un vector aleatorio de tamaño n.

    Args:
        n: Tamaño del vector a generar.

    Returns:
        vector: Vector aleatorio generado.
    """
    min_value = 1
    max_value = 100000
    return [random.randint(min_value, max_value) for _ in range(n)]

def leer_vector():
    """Lee el tamaño del vector y genera un vector aleatorio con ese tamaño."""
    while True:
        try:
            n = int(input("\nIngrese el tamaño del vector a generar (entre 1000 y 100000): "))
            if n < 1000 or n > 100000:
                print("El tamaño del vector debe estar entre 1000 y 100000.")
            else:
                break
        except ValueError:
            print("Por favor, ingrese un número válido.")
    return generate_random_vector(n)

def escoger_algoritmo():
    """Permite al usuario seleccionar un algoritmo de ordenamiento."""
    print("Escoja entre los algoritmos de ordenamiento:"+
          "\n1. MergeSort.\n2. HeapSort.\n3. QuickSort.\n4. Terminar programa")
    opc = (input("Ingrese su opción: ")).strip()

    while opc not in ("1", "2", "3", "4"):
        print("Opción inválida. Intente de nuevo.")
        opc = (input("\nIngrese su opción: ")).strip()

    return opc

try:
    host = "localhost" # si quiere utilizar en diferente pc cambia el host segun el ip de su computadora
    ports = [12345, 12346]
    sockets = [socket.socket() for _ in ports]

    for i, port in enumerate(ports):
        conectar_a_servidor(host, port, sockets[i])

    Z_time = leer_tiempo_limite()

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
            data = {"a": v, "b": opc, "c": float(Z_time), "d": pivote}

        success = False
        total_time = 0
        current_worker = 1
        while not success:
            data["worker_id"] = current_worker
            send_data_to_worker(sockets, current_worker, data)

            # Esperar el límite de tiempo
            time.sleep(Z_time)

            # Recibir el resultado del worker actual
            worker_result = recv_data_from_worker(sockets, current_worker)
            if 'tiempo' not in worker_result:
                print("Error: 'tiempo' no encontrado en los datos recibidos")
                continue

            if worker_result["tiempo"] <= Z_time:
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

    print("\nEl programa ha sido detenido por el usuario.")
    print("Cerrando conexiones y liberando recursos.\n")

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
    for s in sockets:
        s.close()