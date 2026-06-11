import json 
from config import ruta_json_asadas 
from models.asada import Asada

def cargar_json_local():
    """
    Se encarga de cargas el archivo json local.
    Returns:
        _type_: Retorna el archivo json local.
    """
    with open(ruta_json_asadas, "r", encoding="utf-8") as archivo:
        return json.load(archivo)
    
def obtener_lista_asadas():
    """
    Se encarga de obtener la lista de asadas.

    Returns:
        _type_: Retorna la lista de asadas.
    """
    datos = cargar_json_local()
    return datos["value"]

def obtener_metadata():
    """
    Se encarga de obtener la metadata.
    Returns:
        _type_: Retorna la metadata.
    """
    datos = cargar_json_local()
    return datos["metadata"]

def obtener_objetos_asadas():
    """
    Se encarga de crear los objetos asadas.
    Returns:
        _type_: Retorna los objetos asadas.
    """
    registros = obtener_lista_asadas()
    asadas = []
    
    for registro in registros:
        try:
            asada = Asada.from_dict(registro)
            asadas.append(asada)
        except Exception as error:
            print("Error convirtiendo registro:", error)
    
    return asadas
