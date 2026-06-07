import socket
import sys
import threading
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from config import HOST, PORT
from server.cliente_handler import atender_cliente

def iniciar_servidor():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    servidor.bind((HOST, PORT))
    servidor.listen()
    
    print(f"Servidor iniciado en {HOST}:{PORT}")
    print("Esperando cliente...")
    
    try:
        while True:
            socket_cliente, direccion = servidor.accept()
            
            hilo = threading.Thread(
                target = atender_cliente,
                args = (socket_cliente, direccion)
            )
            
            hilo.daemon = True
            hilo.start()
    except KeyboardInterrupt:
        print("\nServidor detenido manualmente.")
    finally:
        servidor.close()        

if __name__ == "__main__":
    iniciar_servidor()
    
