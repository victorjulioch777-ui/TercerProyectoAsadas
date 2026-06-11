import socket
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import config
from config import HOST, PORT
from server.protocolo import enviar_mensaje, recibir_mensaje

def iniciar_cliente():
    """
    Se encarga de iniciar el cliente y conectar con el servidor.
    Si la conexion es exitosa, se muestra el menu de opciones.
    Si la conexion falla, se muestra un mensaje de error.
    """
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        cliente.connect((HOST, PORT))
        mostrar_menu_cliente(cliente)    
    except ConnectionRefusedError:
        print("No se pudo conectar con el servidor. Verfique que este encendido.")
    finally:
        cliente.close()
        
def mostrar_menu_cliente(cliente):
    """
    Se encarga de mostrar el menu de opciones al cliente.
    Y de manejar la interaccion con el servidor.
    Args:
        cliente (_type_): Socket del cliente
    """
    while True:
        print("\n====CONSULTA DE CLIENTES====")
        print(f"{config.OPCIONES_CLIENTE['BUSCAR_ID']}. Buscar ASADA por id")
        print(f"{config.OPCIONES_CLIENTE['BUSCAR_UBICACION']}. Buscar ASADAS por provincia, cantón y distrito")
        print(f"{config.OPCIONES_CLIENTE['SALIR']}. Salir")
        
        opcion = input("Seleccione una opcion: ").strip()
        
        if opcion == config.OPCIONES_CLIENTE["BUSCAR_ID"]:
            buscar_por_id(cliente)
        elif opcion == config.OPCIONES_CLIENTE["BUSCAR_UBICACION"]:
            buscar_por_ubicacion(cliente)
        elif opcion == config.OPCIONES_CLIENTE["SALIR"]:
            enviar_mensaje(cliente, {"accion": "salir"})
            respuesta = recibir_mensaje(cliente)
            print(respuesta.get("mensaje"))
            return
        else:
            print("Opción inválida.")

def enviar_solicitud(cliente, accion, **datos):
    """
    Se encarga de enviar la solicitud al servidor y de recibir la respuesta.
    Args:
        cliente (_type_): Socket del cliente
        accion (_type_): String que indica la accion a realizar
    """
    solicitud = {
        "accion": accion,
        **datos
    }
    
    enviar_mensaje(cliente, solicitud)
    respuesta = recibir_mensaje(cliente)
    mostrar_respuesta(respuesta)
       
def buscar_por_id(cliente):
    """
    Se encarga de buscar una ASADA por id.
    Args:
        cliente (_type_): Socket del cliente
    """
    id_asada = input("Digite el id_Asada: ").strip()
    
    if not id_asada.isdigit():
        print("El id_asada debe ser un número.")
        return
    
    enviar_solicitud(
        cliente,
        "buscar_id",
        id_asada = id_asada
    )

def buscar_por_ubicacion(cliente):
    """
    Se encarga de buscar las ASADAS por provincia, canton y distrito.
    Args:
        cliente (_type_): Socket del cliente
    """
    provincia = input("Digite la provincia: ").strip().upper()
    canton = input("Digite el canton: ").strip().upper()
    distrito = input("Digite el distrito: ").strip().upper()
    
    if not provincia or not canton or not distrito:
        print("Debe completar pronvincia, canton y distrito.")
        return
    
    enviar_solicitud(
        cliente,
        "buscar_ubicacion",
        provincia = provincia,
        canton = canton,
        distrito = distrito
    )
    
def mostrar_respuesta(respuesta):
    """
    Se encarga de mostrar la respuesta del servidor.
    Args:
        respuesta (_type_): Diccionario con la respuesta del servidor
    """
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
    """
    Se encarga de mostrar una ASADA.
    Args:
        asada (_type_): Diccionario con la informacion de la ASADA
    """
    print("-----------------------------------")
    print(f"{config.CLAVES_ASADAS['ID']}:", asada[config.CAMPO_ID_ASADA])
    print(f"{config.CLAVES_ASADAS['OPERADOR']}:", asada[config.CAMPO_OPERADOR])
    print(f"{config.CLAVES_ASADAS['PROVINCIA']}:", asada[config.CAMPO_PROVINCIA])
    print(f"{config.CLAVES_ASADAS['CANTON']}:", asada[config.CAMPO_CANTON])
    print(f"{config.CLAVES_ASADAS['DISTRITO']}:", asada[config.CAMPO_DISTRITO])
    print(f"{config.CLAVES_ASADAS['TELEFONO']}:", asada[config.CAMPO_TELEFONO])
    print(f"{config.CLAVES_ASADAS['CORREO']}:", asada[config.CAMPO_CORREO])
    print(f"{config.CLAVES_ASADAS['TIPO_DE_SISTEMA']}:", asada[config.CAMPO_TIPO_DE_SISTEMA])

if __name__ == "__main__":
    iniciar_cliente()
