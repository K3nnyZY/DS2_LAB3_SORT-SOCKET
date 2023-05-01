import socket
import json

class Client:
    def __init__(self):
        self.s = socket.socket()
    
    def conectar_a_servidor(self):
        self.s.connect(("", 12345))
        
    def leer_vector(self, v):
        v_list = []
        while len(v)<1 and not(len(v_list)==1 and v_list[0]=="s"):
            v_list = (input("\nIngrese el vector a ordenar o \"s\" para salir: ")).split(",")
            for e in v_list:
                if e.strip().isnumeric():
                    v.append(int(e.strip()))
                else:
                    if not(len(v_list)==1 and v_list[0]=="s" 
                        or ((e.strip().isspace() or e.strip()=="")
                            and v_list.index(e)==len(v_list)-1
                            and len(v)>1)):
                        print("El vector ingresado no cumple con las "+
                            "instrucciones dadas:\nEl elemento \""+e.strip()+
                            "\" no puede añadirse al vector. \nRecuerde que "+
                            "solo puede contener números y debe separarlos "+
                            "por comas.")
                        v = []
                        break

    def escoger_algoritmo(self):
        # Preguntamos que algoritmo quiere escoger
        print("Escoja entre los algoritmos de ordenamiento:"+
              "\n1. MergeSort.\n2. HeapSort.\n3. QuickSort.")
        opc = (input("Ingrese su opción: ")).strip()
                
        while opc not in ("1", "2", "3"):
            print("Opción inválida. Intente de nuevo.")
            opc = (input("\nIngrese su opción: ")).strip()
            
        return opc
    

try:
    client = Client()
    client.conectar_a_servidor()
    
    while True:
        
        # Lee el vector y valida que este compuesto únicamente por números
        v = []
        client.leer_vector(v)
        
        if len(v)<1:
            
            # Si desea cerrar el programa
            data = json.dumps({"a": 1, "b": "5"})
            client.s.send(data.encode())
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
                opc = "4" if pivote == "2" else "3"

            # Codificamos el vector y una variable para indicarle al server 
            # lo que hay que hacer
            data = json.dumps({"a": v, "b": opc})
                
            # Mandamos la data codificada al server
            client.s.send(data.encode())
                
            # Recibimos una respuesta del server (esta es para el ping)
            rcvd_data = client.s.recv(1024)
            rcvd_data = json.loads(rcvd_data.decode())
            
            # Se responde al server para que continúe
            data = json.dumps(rcvd_data)
            client.s.send(data.encode())

            print("Progreso de ordenamiento del array:")

            while rcvd_data.get("Flag") == "Bandera":

                # Recibimos respuestas del server
                rcvd_data = client.s.recv(1024)
                rcvd_data = json.loads(rcvd_data.decode())

                # Si el server acaba el ordenamiento,
                # manda un ping para romper el ciclo
                if rcvd_data.get("Flag") != "Bandera":
                    break
                else:
                    # Se imprime lo que nos manda el server
                    print(rcvd_data.get("arr"))

                    # Responde al server para que continúe
                    data = json.dumps(rcvd_data)
                    client.s.send(data.encode())

            # Se imprime el resultado final
            print("\nTiempo de ejecución:", rcvd_data.get("Flag"), "segundos")
            print("Resultado final:", rcvd_data.get("arr"), "\n")    

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
    client.s.close()

