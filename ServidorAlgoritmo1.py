from functools import reduce
from dateutil import parser
import threading
import datetime
import socket
import time

datosCliente = {}

#funcion para recibir el tiempo 
def recibirTiempo(conector, direccion):

	while True:
		tiempoCadena = conector.recv(1024).decode()
		tiempo = parser.parse(tiempoCadena)
        
		diferenciaTiempo = datetime.datetime.now() - tiempo

		datosCliente[direccion] = {
			"tiempo": tiempo,
			"diferencia": diferenciaTiempo,
			"conector": conector
			}
		print("\n==============================================")
		print("\nActualización del cliente: ",str(direccion))
		time.sleep(5)

#funcion para la conexion 
def conexion(socketServer):

	while True:
		
		servidorClienteConector, addr = socketServer.accept()
		direccionCliente = str(addr[0]) + ":" + str(addr[1])
        
		print("\n\n",direccionCliente, "La conexion fue exitosa")
		sincronizacionHilo = threading.Thread(target = recibirTiempo,args = (servidorClienteConector,direccionCliente, ))
		sincronizacionHilo.start()


#funcion que devuelve el promedio del reloj
def promReloj():

	diferencia_list = list(client['diferencia']
								for client_addr, client
									in datosCliente.items())						
	sumDiferencias = sum(diferencia_list, datetime.timedelta(0, 0))
	#obtenemos el promedio...
	promDiferencias = sumDiferencias / (len(datosCliente)+1)
	return promDiferencias


def SincronizarRelojes():

	while True:

		print("\n\n================ Nueva Sincronizacion =================")
		print("\nNumero de clientes:", len(datosCliente))

		if len(datosCliente) > 0:

			promDiferencias = promReloj()
			tiempoSincronizado = datetime.datetime.now() + promDiferencias
			hora = tiempoSincronizado.strftime("%H:%M:%S")
			
			print("\nServidor: Sincronizacion tiempo ",hora)

			for client_addr, client in datosCliente.items():
				try:
					client['conector'].send(str(tiempoSincronizado).encode())

				except Exception as e:
					print("\n\nError al mandar el tiempo", str(client_addr))

		else :
			print("\n=======================================================")
			print("\nEsperando datos del cliente...")
		print("\n\n")
		time.sleep(5) 
#Las rondas de sincronización tienen lugar periódicamente en T = 5 segundos .

# Iniciar Servidor
def iniciarServidor(port = 8000):

	socketServer = socket.socket()
    
	socketServer.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1)

	print("\n===================== Servidor =======================")
	print("Iniciando servidor...")
	print("\nServidor inicializado exitosamente")
	socketServer.bind(('', port))

    #Soporta 10 clientes 
	socketServer.listen(10) 
	print("\nConectando servidor...")
	hiloPrincipal = threading.Thread(target = conexion,args = (socketServer,))
	hiloPrincipal.start()

	print("\nSincronizacion paralela exitosa...")
	print("=======================================================\n")
	hilosSincronizados = threading.Thread(target = SincronizarRelojes,args = ())
	hilosSincronizados.start()


if __name__ == '__main__':

	#incializamos el puerto 
	iniciarServidor(port = 8000)
