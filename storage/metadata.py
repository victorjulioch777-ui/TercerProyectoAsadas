import json

import config

def guardar_metadata(metadata):
    """
    Se encarga de guardar la metadata en el archivo JSON.
    Args:
        metadata (_type_): Diccionario con la metadata.
    """
    with open(config.ruta_metadata, "w", encoding="utf-8") as archivo:
        json.dump(metadata, archivo, indent=4, ensure_ascii=False)
        
def cargar_metadata():
    """ 
    Se encarga de cargar la metadata del archivo JSON.
    Returns:
        _type_: Datos de la metadata.
    """
    try:
        with open(config.ruta_metadata, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        return None
    
def obtener_fecha_metadata_local():
    """
    Se encarga de obtener la fecha de la metadata local.
    Returns:
        _type_: Fecha de la metadata local.
    """
    metadata = cargar_metadata()
    
    if metadata is None:
        return None
    
    return metadata.get(config.CAMPO_FECHA_METADATA)
