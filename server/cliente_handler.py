from socket import socket
from typing import Any, Callable

import config

from server.protocolo import recibir_mensaje, enviar_mensaje
from services.sincronizador import cargar_estructuras
from storage.archivo_asadas import leer_asada_por_posicion

def crear_respuesta_ok(datos = None, mensaje = None):
    respuesta = {
        config.CAMPO_ESTADO: config.ESTADO_OK
    }
    
    if datos is not None:
        respuesta[config.CAMPO_DATOS] = datos
    
    if mensaje is not None:
        respuesta[config.CAMPO_MENSAJE] = mensaje
        
    return respuesta

def crear_respuesta_error(mensaje):
    return {
        config.CAMPO_ESTADO: config.ESTADO_ERROR,
        config.CAMPO_MENSAJE: mensaje
    }

def atender_cliente(socket_cliente, direccion):
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
    funcion_procesadora = despachador_acciones.get(accion)
    
    if funcion_procesadora is None:
        return crear_respuesta_error(config.MENSAJE_ACCION_INVALIDA)
    
    return funcion_procesadora(solicitud)   
        
def procesar_busqueda_id(solicitud, arbol):
    id_asada = solicitud.get(config.CAMPO_ID_ASADA)
    
    posicion = arbol.buscar(id_asada)
    
    if posicion is None:
        return crear_respuesta_error(config.MENSAJE_ASADA_NO_ENCONTRADA)
            
    asada = leer_asada_por_posicion(posicion)
    
    return crear_respuesta_ok(datos = asada)
    
def procesar_busqueda_ubicacion(solicitud, estructura):
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
    return solicitud.get(campo, "").strip().upper()

def obtener_asadas_desde_referencias(referencias):
    asadas = []
    
    for referencia in referencias:
        posicion = referencia[config.CAMPO_POSICION_REGISTRO]
        asada = leer_asada_por_posicion(posicion)
        asadas.append(asada)
    
    return asadas