import config

from services.api_aresep import (
    obtener_datos_aresep,
    obtener_metadata,
    obtener_objetos_asadas
)
from storage.archivo_asadas import guardar_asadas
from storage.archivo_arbol import guardar_arbol, cargar_arbol
from storage.archivo_geografico import guardar_estructura_geografica, cargar_estructura_geografica
from storage.metadata import guardar_metadata, obtener_fecha_metadata_local
from structures.arbol_binario import arbol_binario_de_busqueda
from structures.listas_geograficas import lista_geografica

def mostrar_fechas_metadata(fecha_actual, fecha_local):
    """
    Se encarga de mostrar las fechas de metadata.
    
    Args:
        fecha_actual (str): Fecha actual obtenida de la API.
        fecha_local (str): Fecha local obtenida del archivo de metadata.
    """
    print("Fecha actual", fecha_actual)
    print("Fecha local", fecha_local)

def reconstruir_estructuras(datos_aresep):
    """
    Se encarga de reconstruir las estructuras de datos.
    
    Returns:
        dict: Diccionario con la cantidad de ASADAS, el árbol y la estructura geográfica.
    """
    lista_asadas = obtener_objetos_asadas(datos_aresep)
    print("Objetos ASADA cargados:", len(lista_asadas))
    
    posiciones = guardar_asadas(lista_asadas)
    print("Archivo binario principal creado.")
    
    arbol = construir_arbol(lista_asadas, posiciones)
    guardar_arbol(arbol)
    print("Índice de árbol binario creado.")
    
    estructura_geografica = construir_estructura_geografica(
        lista_asadas,
        posiciones
    )
    guardar_estructura_geografica(estructura_geografica)
    print("Estructura geográfica creada.")
    
    return {
        "cantidad_asadas": len(lista_asadas),
        "arbol": arbol,
        "estructura_geografica": estructura_geografica
    }

def construir_arbol(lista_asadas, posiciones):
    """
    Se encarga de construir el árbol binario de búsqueda.
    
    Args:
        lista_asadas (list): Lista de objetos ASADA.
        posiciones (dict): Diccionario de posiciones de las ASADAS.

    Returns:
        arbol_binario_de_busqueda: Árbol binario de búsqueda.
    """
    arbol = arbol_binario_de_busqueda()
    
    for asada in lista_asadas:
        posicion = posiciones[asada.id_asada]
        arbol.insertar(asada.id_asada, posicion)
        
    return arbol

def construir_estructura_geografica(lista_asadas, posiciones):
    """
    Se encarga de construir la estructura geográfica.
    
    Args:
        lista_asadas (list): Lista de objetos ASADA.
        posiciones (dict): Diccionario de posiciones de las ASADAS.

    Returns:
        lista_geografica: Estructura geográfica.
    """
    estructura = lista_geografica()
    
    for asada in lista_asadas:
        posicion = posiciones[asada.id_asada]
        estructura.insertar_asada(asada, posicion)
        
    return estructura

def sincronizar_datos(forzar = False):
    """
    Se encarga de sincronizar los datos con la API.
    
    Args:
        forzar (bool, optional): Si es True, se sincronizan los datos sin verificar la fecha.
            Defaults to False.

    Returns:
        dict: Diccionario con la información de la sincronización.    
    """
    print(config.MENSAJE_VERIFICANDO_ACTUALIZACION)
    
    resultado_descarga = obtener_datos_aresep()
    datos_aresep = resultado_descarga["datos"]
    origen_datos = resultado_descarga["origen"]

    metadata_actual = obtener_metadata(datos_aresep)
    fecha_actual = metadata_actual.get(config.CAMPO_FECHA_METADATA)
    fecha_local = obtener_fecha_metadata_local()
    
    mostrar_fechas_metadata(fecha_actual, fecha_local)

    if origen_datos == "local" and fecha_local is not None and not forzar:
        print(config.MENSAJE_ACTUALIZACION_NO_VERIFICADA)
        return {
            "actualizado": False,
            "fecha": fecha_actual,
            "origen": origen_datos
        }

    if forzar:
        print(config.MENSAJE_SINCRONIZACION_FORZADA)
    
    elif fecha_local is None:
        print(config.MENSAJE_METADATA_NO_EXISTE)
    
    elif not forzar and fecha_local == fecha_actual:
        print(config.MENSAJE_DATOS_ACTUALIZADOS)
        return {
            "actualizado": False,
            "fecha": fecha_actual
        }
    
    else:
        print(config.MENSAJE_METADATA_CAMBIO)

    print(config.MENSAJE_RECONSTRUYENDO)

    resultado = reconstruir_estructuras(datos_aresep)

    guardar_metadata(metadata_actual)
    print(config.MENSAJE_METADATA_GUARDADA)

    print("Sincronización finalizada correctamente.")

    return {
        "actualizado": True,
        "fecha": fecha_actual,
        "cantidad_asadas": resultado["cantidad_asadas"]
    }
    
def cargar_estructuras():
    """
    Se encarga de cargar las estructuras desde los archivos.
    Returns:
        _type_: Tupla con el árbol y la estructura geográfica.
    """
    arbol = cargar_arbol()
    estructura_geografica = cargar_estructura_geografica()
    
    return arbol, estructura_geografica

def debo_reconstruir(forzar, fecha_actual, fecha_local, origen_datos):
    if forzar:
        print(config.MENSAJE_SINCRONIZACION_FORZADA)
        return True
    
    if origen_datos == "local":
        print(config.MENSAJE_ACTUALIZACION_NO_VERIFICADA)
        return False
    
    if fecha_actual is None:
        print(config.MENSAJE_METADATA_NO_EXISTE)
        return True
    
    if fecha_local != fecha_actual:
        print(config.MENSAJE_METADATA_CAMBIO)
        return True
    
    print(config.MENSAJE_DATOS_ACTUALIZADOS)
    return False
