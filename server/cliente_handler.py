from socket import socket
from typing import Any, Callable

import config

from server.protocolo import recibir_mensaje, enviar_mensaje
from services.sincronizador import cargar_estructuras
from storage.archivo_asadas import leer_asada_por_posicion

def crear_respuesta_ok(datos = None, mensaje = None):
    """
    Se encarga de crear una respuesta exitosa.

    Args:
        datos (_type_, optional): Datos a incluir en la respuesta.
        mensaje (_type_, optional): Mensaje a incluir en la respuesta.

    Returns:
        _type_: Respuesta exitosa
    """
    respuesta = {
        config.CAMPO_ESTADO: config.ESTADO_OK
    }
    
    if datos is not None:
        respuesta[config.CAMPO_DATOS] = datos
    
    if mensaje is not None:
        respuesta[config.CAMPO_MENSAJE] = mensaje
        
    return respuesta

def crear_respuesta_error(mensaje):
    """
    Se encarga de crear una respuesta de error.

    Args:
        mensaje (str): Mensaje a incluir en la respuesta

    Returns:
        _type_: Respuesta de error
    """
    return {
        config.CAMPO_ESTADO: config.ESTADO_ERROR,
        config.CAMPO_MENSAJE: mensaje
    }

def atender_cliente(socket_cliente, direccion):
    """
    Se encarga de atender a un cliente.

    Args:
        socket_cliente (_type_): Socket del cliente.
        direccion (_type_): Direccion del cliente.
    """
    print(f"Cliente conectado desde: {direccion}")
        
    try:
        arbol, estructura = cargar_estructuras()
        
        despachador_acciones = crear_despachador(arbol, estructura)
        
        while True:
            solicitud = recibir_mensaje(socket_cliente)
            
            if solicitud is None:
                break
            
            accion = solicitud.get(config.CAMPO_ACCION)
            
            respuesta = procesar_solicitud(
                accion,
                solicitud,
                despachador_acciones
            )
            
            enviar_mensaje(socket_cliente, respuesta)
            
            if accion == config.ACCION_SALIR:
                break
    except Exception as error:
        print("Error atendiendo al cliente:", error)
        
    finally:
        socket_cliente.close()
        print(f"Cliente desconectado: {direccion}")

def crear_despachador(arbol, estructura):
    """
    Se encarga de crear un despachador de acciones.
    
    Args:
        arbol (_type_): Arbol de asadas.
        estructura (_type_): Estructura de asadas.

    Returns:
        _type_: Diccionario con las acciones a realizar.
    """
    return {
        config.ACCION_BUSCAR_ID: lambda solicitud: procesar_busqueda_id(
            solicitud, 
            arbol
        ),
        config.ACCION_BUSCAR_UBICACION: lambda solicitud: procesar_busqueda_ubicacion(
            solicitud,
            estructura
        ),
        config.ACCION_SALIR: lambda solicitud: crear_respuesta_ok(
            mensaje = config.MENSAJE_CONEXION_CERRADA
        )
    }        
    
def procesar_solicitud(accion, solicitud, despachador_acciones):
    """
    Se encarga de procesar una solicitud.

    Args:
        accion (_type_): Accion a realizar.
        solicitud (_type_): Solicitud a procesar.
        despachador_acciones (_type_): Diccionario con las acciones a realizar.

    Returns:
        _type_: Respuesta a la solicitud.
    """
    funcion_procesadora = despachador_acciones.get(accion)
    
    if funcion_procesadora is None:
        return crear_respuesta_error(config.MENSAJE_ACCION_INVALIDA)
    
    return funcion_procesadora(solicitud)   
        
def procesar_busqueda_id(solicitud, arbol):
    """
    Se encarga de procesar una busqueda por ID.
    Args:
        solicitud (_type_): Solicitud a procesar.
        arbol (_type_): Arbol de asadas.

    Returns:
        _type_: Respuesta a la solicitud.
    """
    id_asada = solicitud.get(config.CAMPO_ID_ASADA)
    
    posicion = arbol.buscar(id_asada)
    
    if posicion is None:
        return crear_respuesta_error(config.MENSAJE_ASADA_NO_ENCONTRADA)
            
    asada = leer_asada_por_posicion(posicion)
    
    return crear_respuesta_ok(datos = asada)
    
def procesar_busqueda_ubicacion(solicitud, estructura):
    """
    Se encarga de procesar una busqueda por ubicacion.
    Args:
        solicitud (_type_): Solicitud a procesar.
        estructura (_type_): Estructura de asadas.

    Returns:
        _type_: Retorna una respuesta con las asadas encontradas.
    """
    provincia = obtener_campo_texto(solicitud, config.CAMPO_PROVINCIA)
    canton = obtener_campo_texto(solicitud, config.CAMPO_CANTON)
    distrito = obtener_campo_texto(solicitud, config.CAMPO_DISTRITO)
    
    referencias = estructura.obtener_asadas_por_distrito(
        provincia,
        canton,
        distrito
    )
    
    if not referencias:
        return crear_respuesta_error(config.MENSAJE_UBICACION_SIN_ASADAS)
        
    asadas = obtener_asadas_desde_referencias(referencias)
    
    return crear_respuesta_ok(datos = asadas)

def obtener_campo_texto(solicitud, campo):
    """
    Se encarga de obtener un campo de texto de la solicitud.
    Args:
        solicitud (_type_): Solicitud a procesar.
        campo (_type_): Campo a obtener.

    Returns:
        _type_: Retorna el valor del campo de texto.
    """
    return solicitud.get(campo, "").strip().upper()

def obtener_asadas_desde_referencias(referencias):
    """
    Se encarga de obtener las asadas desde las referencias.
    Args:
        referencias (_type_): Referencias a obtener.

    Returns:
        _type_: Retorna una lista con las asadas.
    """
    asadas = []
    
    for referencia in referencias:
        posicion = referencia[config.CAMPO_POSICION_REGISTRO]
        asada = leer_asada_por_posicion(posicion)
        asadas.append(asada)
    
    return asadas