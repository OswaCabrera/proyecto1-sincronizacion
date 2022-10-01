from timeit import default_timer as timer
from dateutil import parser
import threading
import datetime
import socket
import time


# funcion para mandar el tiempo con ayuda de los hilos al cliente
def enviarTiempo(socketClient):

	while True:
		hora = datetime.datetime.now()
        
		socketClient.send(str(hora).encode())
		hora = hora.strftime("%H:%M:%S")
		print("\n=================== RELOJ ====================")
		print("\nEnvio exitoso del reloj: ",hora) 		
		time.sleep(5) #Las rondas de sincronización tienen lugar periódicamente en T = 5 segundos .


# funcion para recibir el tiempo con ayuda de los hilos al cliente
def recibirTiempo(socketClient):

	while True:
		tiempoRecibido = parser.parse(socketClient.recv(1024).decode())         
		hora = tiempoRecibido.strftime("%H:%M:%S")
		print("Cliente: Sincronizacion tiempo ",hora)


# Funcion para iniciar el cliente 
def iniciarCliente(port = 8000):  #colocamos el puerto 9999 del UDP 

	socketClient = socket.socket()		
	
	# conectar con el servidor
	socketClient.connect(('127.0.0.1', port))

    #Tiempo del servidor 
	print("\n==============================================")
	print("\nEmpezando tiempo del Servidor...")
	envioHilo = threading.Thread(target = enviarTiempo,args = (socketClient, ))
	envioHilo.start()

    #Sincronizacion 
	print("\nEmpezando Sincronizacion con el servidor...")
	hiloRecibido = threading.Thread(target = recibirTiempo,args = (socketClient, ))  
	hiloRecibido.start()



if __name__ == '__main__':

	iniciarCliente(port = 8000)  #inicializamos el puerto 
