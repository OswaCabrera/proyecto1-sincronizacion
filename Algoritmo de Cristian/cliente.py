from datetime import *
from socket import *
import time
import datetime

def convertir_cadena_a_hora(cadena):
    formato = '%Y%m%d %H:%M:%f'

    hora_cadena = datetime.datetime.strptime(cadena, formato)

    return hora_cadena

IPServidor = "localhost"
puertoServidor = 8000
socketCliente = socket(AF_INET, SOCK_STREAM)

inicio = time.time()
socketCliente.connect((IPServidor, puertoServidor))

hora_cadena = socketCliente.recv(4096).decode()

final = time.time()
tiempo = final - inicio
hora = convertir_cadena_a_hora(hora_cadena)

print("El tiempo total de ida y vuelta fue:", tiempo)

mitadTiempo = tiempo/2

print("El tiempo de ida: ", mitadTiempo)

print("Hora servidor: ", hora_cadena)
print("La hora exacta es : ", hora + datetime.timedelta(seconds=mitadTiempo))
time.sleep(5)

socketCliente.close()
