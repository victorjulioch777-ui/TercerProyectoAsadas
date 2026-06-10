import config

from services.api_aresep import obtener_metadata, obtener_objetos_asadas
from storage.archivo_asadas import guardar_asadas
from storage.archivo_arbol import guardar_arbol, cargar_arbol
from storage.archivo_geografico import guardar_estructura_geografica, cargar_estructura_geografica
from storage.metadata import guardar_metadata, obtener_fecha_metadata_local
from structures.arbol_binario import arbol_binario_de_busqueda
from structures.listas_geograficas import lista_geografica

def mostrar_fechas_metadata(fecha_actual, fecha_local):
    print("Fecha actual", fecha_actual)
    print("Fecha local", fecha_local)

def reconstruir_estructuras():
    lista_asadas = obtener_objetos_asadas()
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
    
    for asada in lista_asadas:
        posicion = posiciones[asada.id_asada]
        arbol.insertar(asada.id_asada, posicion)
        
    return arbol

def construir_estructura_geografica(lista_asadas, posiciones):
    estructura = lista_geografica()
    
    for asada in lista_asadas:
        posicion = posiciones[asada.id_asada]
        estructura.insertar_asada(asada, posicion)
        
    return estructura

def sincronizar_datos(forzar = False):
    print(config.MENSAJE_VERIFICANDO_ACTUALIZACION)
    
    metadata_actual = obtener_metadata()
    fecha_actual = metadata_actual.get(config.CAMPO_FECHA_METADATA)
    fecha_local = obtener_fecha_metadata_local()
    
    mostrar_fechas_metadata(fecha_actual, fecha_local)
    
    if fecha_local is None:
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

    resultado = reconstruir_estructuras()

    guardar_metadata(metadata_actual)
    print(config.MENSAJE_METADATA_GUARDADA)

    print("Sincronización finalizada correctamente.")

    return {
        "actualizado": True,
        "fecha": fecha_actual,
        "cantidad_asadas": resultado["cantidad_asadas"]
    }
    
def cargar_estructuras():
    arbol = cargar_arbol()
    estructura_geografica = cargar_estructura_geografica()
    
    return arbol, estructura_geografica
