import json
from socket import *
import time

dir_IP_servidor = '158.42.188.200'
puerto_servidor = 64010
dir_socket_servidor = (dir_IP_servidor, puerto_servidor)
s = socket(AF_INET, SOCK_STREAM)

mensaje_hello = f"HELLO 10.237.15.100\r\n"

s.connect(dir_socket_servidor)
s.send(mensaje_hello.encode())
mensaje_rx = s.recv(2048)
if mensaje_rx.decode().startswith("200"):
    nombre_usu = input("introduce el nombre de usuario: ")
    mensaje_user = f"USER {nombre_usu}\r\n"
    s.send(mensaje_user.encode())
    mensaje_rx = s.recv(2048)
    if mensaje_rx.decode().startswith("200"):
        pass_usu = input(f"introduce la contraseña del usuario {nombre_usu.upper()}: ")
        mensaje_pass = f"PASS {pass_usu}\r\n"
        s.send(mensaje_pass.encode())
        mensaje_rx = s.recv(2048)
        if mensaje_rx.decode().startswith("200"):
            print(f"------------------- BIENVENIDO {nombre_usu.upper()} -------------------\n")
            while True:
                print("MENÚ:")
                print("1. Ver ranking")
                print("2. Enviar datos")
                print("3. Salir")

                seleccion = int(input("Elige una opción: "))
                if 1 > seleccion > 3:
                    print("Selecciona una opción valida del menú")
                elif seleccion == 1:
                    s.send("GET_LEADERBOARD\r\n".encode())
                    mensaje_rx = s.recv(2048)
                    mensaje_descifrado = mensaje_rx.decode()
                    ranking = []
                    if mensaje_descifrado.startswith("400"):
                        print("Error en el comando GET_LEADERBOARD:", mensaje_descifrado)
                    elif mensaje_descifrado.startswith("200"):
                        print("Tabla de clasificación:")
                        while True:
                            respuesta = s.recv(1024).decode()
                            if respuesta.startswith("202"):
                                break
                            else:
                                ranking.append(respuesta[:])
                        parsed_ranking = []
                        for respuesta in ranking:
                            try:
                                json_data = json.loads(respuesta.strip())
                                parsed_ranking.append(json_data)
                            except json.JSONDecodeError as e:
                                print(f"Error al decodificar JSON: {e}")
                    else:
                        print("Respuesta inesperada del servidor.")
                elif seleccion == 2:
                    nombre = input("Nombre: ")
                    grupo_Promu = input("Grupo promu: ")
                    altura = input("Altura: ")
                    fecha = input("Fecha: ")

                    mensaje_final = 'SEND_DATA {"nombre":'+nombre+',"grupo_ProMu":'+grupo_Promu+',"altura":'+altura+',"fecha":'+fecha+'}\r\n'

                    s.send(mensaje_final.encode())
                    mensaje_rx = s.recv(2048)
                    time.sleep(1)
                    print(mensaje_rx.decode())
                else:
                    s.send("QUIT\r\n".encode())
                    s.close()
                    break
    else:
        print(mensaje_rx.decode())

print("SESIÓN FINALIZADA")
