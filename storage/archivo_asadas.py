import json 
import struct

from config import ruta_archivo_asadas

def guardar_asadas(lista_asadas):
    """
    Se encarga de guardar las asadas en el archivo binario.
    Args:
        lista_asadas (_type_): Lista de objetos de tipo Asada.

    Returns:
        _type_: Diccionario con las posiciones de cada asada.
    """
    posiciones = {}
    
    with open(ruta_archivo_asadas, "wb")as archivo:
        for asada in lista_asadas:
            posicion = archivo.tell()
            posiciones[asada.id_asada] = posicion
            
            datos_json = json.dumps(asada.to_dict(), ensure_ascii=False)
            datos_bytes = datos_json.encode("utf-8")
            
            archivo.write(struct.pack("I", len(datos_bytes)))
            archivo.write(datos_bytes)
            
    return posiciones

def leer_asada_por_posicion(posicion):
    """
    Se encarga de leer una asada por su posición.
    Args:
        posicion (_type_): Posición de la asada.

    Returns:
        _type_: Datos de la asada.
    """
    with open(ruta_archivo_asadas, "rb")as archivo:
        archivo.seek(posicion)
        
        longitud_bytes = archivo.read(4)
        
        if not longitud_bytes:
            return None
        
        longitud = struct.unpack("I", longitud_bytes)[0]
        datos_bytes = archivo.read(longitud)
        
        datos = json.loads(datos_bytes.decode("utf-8"))
        return datos