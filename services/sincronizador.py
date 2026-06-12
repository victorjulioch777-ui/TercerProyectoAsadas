import json 

import config

from services.api_aresep import (
    obtener_datos_aresep,
    obtener_metadata,
    obtener_objetos_asadas, 
    error_datos_aresep, 
    cargar_json_local_seguro
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
    
def obtener_datos_locales_previos():
    try:
        return cargar_json_local_seguro()
    except (FileNotFoundError, json.JSONDecodeError, error_datos_aresep):
        return None


def existen_archivos_estructuras():
    rutas = [
        config.ruta_archivo_asadas,
        config.ruta_archivo_arbol,
        config.ruta_archivo_geografico
    ]

    return all(ruta.exists() for ruta in rutas)


def obtener_id_registro(registro):
    clave_id = config.CLAVES_JSON_ASADA["ID_ASADA"]
    id_asada = registro.get(clave_id)

    if id_asada is None:
        return None

    try:
        return int(id_asada)
    except (TypeError, ValueError):
        return None


def indexar_registros_por_id(datos_aresep):
    indice = {}

    for registro in datos_aresep.get("value", []):
        id_asada = obtener_id_registro(registro)

        if id_asada is not None:
            indice[id_asada] = registro

    return indice


def crear_firma_registro(registro):
    return json.dumps(
        registro,
        sort_keys=True,
        ensure_ascii=False,
        default=str
    )


def calcular_cambios_incrementales(datos_anteriores, datos_actuales):
    registros_actuales = indexar_registros_por_id(datos_actuales)

    if datos_anteriores is None:
        return {
            "agregadas": sorted(registros_actuales.keys()),
            "actualizadas": [],
            "eliminadas": [],
            "sin_cambios": [],
            "total_anterior": 0,
            "total_actual": len(registros_actuales),
            "hubo_cambios": True
        }

    registros_anteriores = indexar_registros_por_id(datos_anteriores)

    ids_anteriores = set(registros_anteriores.keys())
    ids_actuales = set(registros_actuales.keys())

    agregadas = sorted(ids_actuales - ids_anteriores)
    eliminadas = sorted(ids_anteriores - ids_actuales)

    ids_comunes = ids_anteriores & ids_actuales
    actualizadas = []
    sin_cambios = []

    for id_asada in sorted(ids_comunes):
        firma_anterior = crear_firma_registro(registros_anteriores[id_asada])
        firma_actual = crear_firma_registro(registros_actuales[id_asada])

        if firma_anterior != firma_actual:
            actualizadas.append(id_asada)
        else:
            sin_cambios.append(id_asada)

    hubo_cambios = bool(agregadas or actualizadas or eliminadas)

    return {
        "agregadas": agregadas,
        "actualizadas": actualizadas,
        "eliminadas": eliminadas,
        "sin_cambios": sin_cambios,
        "total_anterior": len(registros_anteriores),
        "total_actual": len(registros_actuales),
        "hubo_cambios": hubo_cambios
    }


def mostrar_resumen_incremental(cambios):
    print("Resumen de actualización incremental:")
    print("ASADAS anteriores:", cambios["total_anterior"])
    print("ASADAS actuales:", cambios["total_actual"])
    print("ASADAS agregadas:", len(cambios["agregadas"]))
    print("ASADAS actualizadas:", len(cambios["actualizadas"]))
    print("ASADAS eliminadas:", len(cambios["eliminadas"]))
    print("ASADAS sin cambios:", len(cambios["sin_cambios"]))

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
    arbol = arbol_binario_de_busqueda()
    pares_id_posicion = []
    
    for asada in lista_asadas:
        posicion = posiciones[asada.id_asada]
        pares_id_posicion.append((asada.id_asada, posicion))
        
    arbol.construir_balanceado(pares_id_posicion)
    
    estadisticas = arbol.obtener_estadisticas()
    
    print("Árbol binario construido.")
    print("Cantidad de nodos:", estadisticas["cantidad_nodos"])
    print("Altura de árbol:", estadisticas["balanceado"])
        
    return arbol

def construir_estructura_geografica(lista_asadas, posiciones):   
    estructura = lista_geografica()
    
    for asada in lista_asadas:
        posicion = posiciones[asada.id_asada]
        estructura.insertar_asada(asada, posicion)
    
    estadisticas = estructura.obtener_estadisticas()

    print("Estructura geográfica jerárquica construida.")
    print("Cantidad de provincias:", estadisticas["cantidad_provincias"])
    print("Cantidad de cantones:", estadisticas["cantidad_cantones"])
    print("Cantidad de distritos:", estadisticas["cantidad_distritos"])
    print("Cantidad de ASADAS ubicadas:", estadisticas["cantidad_asadas"])
    print("Distrito con más ASADAS:", estadisticas["distrito_con_mas_asadas"])
    print("ASADAS en ese distrito:", estadisticas["mayor_cantidad_asadas"])
    
    return estructura

def sincronizar_datos(forzar = False):
    print(config.MENSAJE_VERIFICANDO_ACTUALIZACION)
    
    datos_anteriores = obtener_datos_locales_previos()
    
    resultado_descarga = obtener_datos_aresep()
    datos_aresep = resultado_descarga["datos"]
    origen_datos = resultado_descarga["origen"]

    metadata_actual = obtener_metadata(datos_aresep)
    fecha_actual = metadata_actual.get(config.CAMPO_FECHA_METADATA)
    fecha_local = obtener_fecha_metadata_local()
    
    mostrar_fechas_metadata(fecha_actual, fecha_local)
    
    reconstruir = debo_reconstruir(
        forzar,
        fecha_actual,
        fecha_local, 
        origen_datos
    )
    
    if not reconstruir:
        return {
            "actualizado": False,
            "fecha": fecha_actual,
            "origen": origen_datos
        }
    
    cambios = calcular_cambios_incrementales(datos_anteriores, datos_aresep)
    mostrar_resumen_incremental(cambios)
    
    if (not cambios["hubo_cambios"] and not forzar and existen_archivos_estructuras()):
        guardar_metadata(metadata_actual)
        print("La metadata cambió, pero los registros de ASADAS no cambiaron.")
        print(config.MENSAJE_METADATA_GUARDADA)
        
        return {
            "actualizado": False,
            "fecha": fecha_actual,
            "origen": origen_datos,
            "cambios": cambios
        }
    
    print(config.MENSAJE_RECONSTRUYENDO)
    
    resultado = reconstruir_estructuras(datos_aresep)
    
    guardar_metadata(metadata_actual)
    print(config.MENSAJE_METADATA_GUARDADA)
    
    print("Sincronización finalizada correctamente.")
    
    return {
        "actualizado": True,
        "fecha": fecha_actual,
        "origen": origen_datos,
        "cantidad_asadas": resultado["cantidad_asadas"],
        "cambios": cambios
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
    
    if not existen_archivos_estructuras():
        print("Faltan arhivos binarios locales. Se reconstruirán las estructuras.")
        return True
    
    if origen_datos == "local":
        print(config.MENSAJE_ACTUALIZACION_NO_VERIFICADA)
        return False
    
    if fecha_actual is None:
        print(config.MENSAJE_METADATA_NO_EXISTE)
        return True
    
    if fecha_local is None:
        print(config.MENSAJE_METADATA_NO_EXISTE)
        return True
    
    if fecha_local != fecha_actual:
        print(config.MENSAJE_METADATA_CAMBIO)
        return True
    
    print(config.MENSAJE_DATOS_ACTUALIZADOS)
    return False
