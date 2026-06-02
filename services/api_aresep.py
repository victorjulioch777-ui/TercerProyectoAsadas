import json 
from config import ruta_json_asadas 

def cargar_json_local():
    with open(ruta_json_asadas, "r", encoding="utf-8") as archivo:
        return json.load(archivo)
    
def obtener_lista_asadas():
    datos = cargar_json_local()
    return datos["value"]

def obtener_metadata():
    datos = cargar_json_local()
    return datos["metadata"]