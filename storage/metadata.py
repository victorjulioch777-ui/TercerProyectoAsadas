import json

import config

def guardar_metadata(metadata):
    with open(config.ruta_metadata, "w", encoding="utf-8") as archivo:
        json.dump(metadata, archivo, indent=4, ensure_ascii=False)
        
def cargar_metadata():
    try:
        with open(config.ruta_metadata, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        return None
    
def obtener_fecha_metadata_local():
    metadata = cargar_metadata()
    
    if metadata is None:
        return None
    
    return metadata.get(config.CAMPO_FECHA_METADATA)
