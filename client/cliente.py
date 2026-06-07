import socket
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from config import HOST, PORT
from server.protocolo import enviar_mensaje, recibir_mensaje

def iniciar_cliente():
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        cliente.connect((HOST, PORT))
        mostrar_menu_cliente(cliente)    
    except ConnectionRefusedError:
        print("No se pudo conectar con el servidor. Verfique que este encendido.")
    finally:
        cliente.close()
        
def mostrar_menu_cliente(cliente):
    while True:
        print("\n====CONSULTA DE CLIENTES====")
        print("1. Buscar ASADA por id")
        print("2. Buscar ASADAS por provincia, cantón y distrito")
        print("3. Salir")
        
        opcion = input("Seleccione una opcion: ").strip()
        
        if opcion == "1":
            buscar_por_id(cliente)
        elif opcion == "2":
            buscar_por_ubicacion(cliente)
        elif opcion == "3":
            enviar_mensaje(cliente, {"accion": "salir"})
            respuesta = recibir_mensaje(cliente)
            print(respuesta.get("mensaje"))
            return
        else:
            print("Opción inválida.")
        
def buscar_por_id(cliente):
    id_asada = input("Digite el id_Asada: ").strip()
    
    solicitud = {
        "accion": "buscar_id",
        "id_asada": id_asada
    }
    
    enviar_mensaje(cliente, solicitud)
    respuesta = recibir_mensaje(cliente)
    
    mostrar_respuesta(respuesta)
    
def buscar_por_ubicacion(cliente):
    provincia = input("Digite la provincia: ").strip().upper()
    canton = input("Digite el canton: ").strip().upper()
    distrito = input("Digite el distrito: ").strip().upper()
    
    solicitud = {
        "accion": "buscar_ubicacion",
        "provincia": provincia,
        "canton": canton,
        "distrito": distrito
    }
    
    enviar_mensaje(cliente, solicitud)
    respuesta = recibir_mensaje(cliente)
    
    mostrar_respuesta(respuesta)
    
def mostrar_respuesta(respuesta):
    if respuesta is None:
        print("No se recibio respuestas del servidor.")
        return
    
    if respuesta.get("estado") == "error":
        print("Error:", respuesta.get("mensaje"))
        return 
    
    datos = respuesta.get("datos")
    
    if isinstance(datos, list):
        for asada in datos:
            mostrar_asada(asada)
    else:
        mostrar_asada(datos)
        
def mostrar_asada(asada):
    print("-----------------------------------")
    print("ID:", asada["id_asada"])
    print("Operador:", asada["operador"])
    print("Provincia:", asada["provincia"])
    print("Cantón:", asada["canton"])
    print("Distrito:", asada["distrito"])
    print("Teléfono:", asada["telefono"])
    print("Correo:", asada["correo"])
    print("Tipo de sistema:", asada["tipo_sistema"])

if __name__ == "__main__":
    iniciar_cliente()
