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
        print("No se pudo conectar con el servidor. Verifique que esté encendido.")
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
            enviar_mensaje(cliente, {config.CAMPO_ACCION: config.ACCION_SALIR})
            respuesta = recibir_mensaje(cliente)
            print(respuesta.get(config.CAMPO_MENSAJE))
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
        config.CAMPO_ACCION: accion,
        **datos
    }
    
    enviar_mensaje(cliente, solicitud)
    respuesta = recibir_mensaje(cliente)
    mostrar_respuesta(respuesta)

def procesar(cliente, accion, **datos):
    """
    Se encarga de enviar la solicitud al servidor y mostrar la respuesta.
    Args:
        cliente (_type_): Socket del cliente
        accion (_type_): String que indica la accion a realizar
    """
    enviar_solicitud(
        cliente,
        accion,
        **datos
    )

def enviar_busqueda_por_id(cliente, id_asada):
    """
    Se encarga de enviar la solicitud de busqueda por id al servidor.
    Args:
        cliente (_type_): Socket del cliente
        id_asada (_type_): String que indica el id de la ASADA
    """
    procesar(
        cliente,
        config.ACCION_BUSCAR_ID,
        id_asada=id_asada
    )
    
def enviar_busqueda_por_ubicacion(cliente, provincia, canton, distrito):
    """
    Se encarga de enviar la solicitud de busqueda por ubicacion al servidor.
    Args:
        cliente (_type_): Socket del cliente
        provincia (_type_): String que indica la provincia
        canton (_type_): String que indica el canton
        distrito (_type_): String que indica el distrito
    """
    procesar(
        cliente,
        config.ACCION_BUSCAR_UBICACION,
        provincia=provincia,
        canton=canton,
        distrito=distrito
    )
       
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
    
    enviar_busqueda_por_id(cliente, id_asada)

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
        print("Debe completar provincia, cantón y distrito.")
        return
    
    enviar_busqueda_por_ubicacion(
        cliente,
        provincia,
        canton,
        distrito
    )
    
def mostrar_respuesta(respuesta):
    """
    Se encarga de mostrar la respuesta del servidor.
    Args:
        respuesta (_type_): Diccionario con la respuesta del servidor
    """
    if respuesta is None:
        print("No se recibió respuesta del servidor.")
        return
    
    if respuesta.get(config.CAMPO_ESTADO) == config.ESTADO_ERROR:
        print("Error:", respuesta.get(config.CAMPO_MENSAJE))
        return 
    
    datos = respuesta.get(config.CAMPO_DATOS)
    
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
    if not asada:
        print("No hay datos para mostrar.")
        return

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
