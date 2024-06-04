import time
import json
from socket import *

DIR_IP_SERVIDOR = '158.42.188.200'
PUERTO_SERVIDOR = 64010
DIR_SOCKET_SERVIDOR = (DIR_IP_SERVIDOR, PUERTO_SERVIDOR)

def iniciar_conexion():
    try:
        s = socket(AF_INET, SOCK_STREAM)
        s.connect(DIR_SOCKET_SERVIDOR)
        return s
    except Exception as e:
        print(f"Error al intentar conectar: {e}")
        return False
    return False

def enviar_mensaje(s, message):
    s.send(message.encode())

def recibir_mensaje(s, buffer_size=2048):
    return s.recv(buffer_size).decode()

def login(s, username, password):
    if not s:
        return False

    mensaje_hello = f"HELLO {s.getsockname()[0]}\r\n"
    enviar_mensaje(s, mensaje_hello)
    mensaje_rx = recibir_mensaje(s)
    print(mensaje_rx)
    if mensaje_rx.startswith("200"):
        enviar_mensaje(s, f"USER {username}\r\n")
        response = recibir_mensaje(s)
        if response.startswith("200"):
            enviar_mensaje(s, f"PASS {password}\r\n")
            response = recibir_mensaje(s)
            return response.startswith("200")
    return False

def get_leaderboard(s):
    enviar_mensaje(s, "GET_LEADERBOARD\r\n")
    response = recibir_mensaje(s)
    if response.startswith("400"):
        print("Error en el comando GET_LEADERBOARD:", response)
        return []
    elif response.startswith("200"):
        ranking = []
        while True:
            response = recibir_mensaje(s, 1024)
            if response.startswith("202"):
                break
            else:
                ranking.append(response.strip())
        parsed_ranking = []
        for item in ranking:
            try:
                json_data = json.loads(item)
                parsed_ranking.append(json_data)
            except json.JSONDecodeError as e:
                print(f"Error al decodificar JSON: {e}")
        return parsed_ranking
    else:
        print("Respuesta inesperada del servidor.")
        return []

def send_data(s, data):
    nombre = data[0]
    grupo_Promu = data[1]
    altura = data[2]
    fecha = data[3]

    mensaje_final = 'SEND_DATA {"nombre":'+nombre+',"grupo_ProMu":'+grupo_Promu+',"altura":'+altura+',"fecha":'+fecha+'}\r\n'
    enviar_mensaje(s, mensaje_final)
    response = recibir_mensaje(s)
    time.sleep(1)
    if response.startswith("201"):
        return False
    else:
        return True

def quit_session(s):
    enviar_mensaje(s, "QUIT\r\n")
    s.close()
