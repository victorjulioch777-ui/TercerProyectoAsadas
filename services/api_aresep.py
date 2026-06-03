import json 
from config import ruta_json_asadas 
from models.asada import Asada

def cargar_json_local():
    with open(ruta_json_asadas, "r", encoding="utf-8") as archivo:
        return json.load(archivo)
    
def obtener_lista_asadas():
    datos = cargar_json_local()
    return datos["value"]

def obtener_metadata():
    datos = cargar_json_local()
    return datos["metadata"]

def obtener_objetos_asadas():
    registros = obtener_lista_asadas()
    asadas = []
    
    for registro in registros:
        try:
            asada = Asada.from_dict(registro)
            asadas.append(asada)
        except Exception as error:
            print("Error convirtiendo registro:", error)
    
    return asadas
