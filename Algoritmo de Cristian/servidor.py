from socket import *
from datetime import *
    
def prenderServer(): 
  
    s = socket( AF_INET, SOCK_STREAM) 
    print("Socket creado exitosamente") 
            
    port = 8000
    direccionServidor = "localhost"
  
    s.bind((direccionServidor, port)) 
    
    s.listen(5)       
    print("Socket escuchando...") 
          
    while True:  
               
       connection, address = s.accept()       
       print('Servidor conectado a', address)
       
       hora = datetime.now()

       horaCadena = hora.strftime("%Y%m%d %H:%M:%f") 

       print('Enviamos la hora al cliente', address)
       
       connection.send(horaCadena.encode())

       connection.close() 
       print('Terminamos la conexión') 
  
  
if __name__ == '__main__': 
  
    
    prenderServer()