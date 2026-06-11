import json 
import config
import requests
from models.asada import Asada

def validar_datos_aresep(datos):
    if not isinstance(datos, dict):
        raise ValueError("La respuesta de ARESEP no tiene formato de diccionario.")
    
    if "metadata" not in datos:
        raise ValueError("La respuesta de ARESEP no contiene metadata.")
    
    if "value" not in datos:
        raise ValueError("La respuesta de ARESEP no contiene la lista de ASADAS.")
    
    if not isinstance(datos["value"], list):
        raise ValueError("El campo value de ARESEP no es una lista.")

def descargar_datos_aresep():
    print(config.MENSAJE_DESCARGANDO_DATOS)

    ultimo_error = None

    for intento in range(1, config.INTENTOS_DESCARGA_API + 1):
        try:
            respuesta = requests.get(
                config.URL_ARESEP_ASADAS,
                timeout=(
                    config.TIEMPO_CONEXION_API,
                    config.TIEMPO_LECTURA_API
                )
            )

            respuesta.raise_for_status()

            datos = respuesta.json()
            validar_datos_aresep(datos)

            return datos
        except requests.RequestException as error:
            ultimo_error = error
            print(f"{config.MENSAJE_ERROR_DESCARGA} Intento {intento}/{config.INTENTOS_DESCARGA_API}.")

            if intento < config.INTENTOS_DESCARGA_API:
                print(config.MENSAJE_REINTENTO_DESCARGA)

    raise ultimo_error


def guardar_json_local(datos):
    with open(config.ruta_json_asadas, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=4, ensure_ascii=False)
        
    print(config.MENSAJE_JSON_LOCAL_ACTUALIZADO)

def cargar_json_local():
    with open(config.ruta_json_asadas, "r", encoding="utf-8")as archivo:
        return json.load(archivo)

def obtener_datos_aresep():
    try:
        datos = descargar_datos_aresep()
        guardar_json_local(datos)
        return datos
    except requests.RequestException:
        print(config.MENSAJE_USANDO_JSON_LOCAL)
        datos = cargar_json_local()
        validar_datos_aresep(datos)
        return datos
    
def obtener_lista_asadas(datos=None):
    if datos is None:
        datos = cargar_json_local()
        
    return datos["value"]

def obtener_metadata(datos=None):
    if datos is None:
        datos = cargar_json_local()
        
    return datos["metadata"]

def obtener_objetos_asadas(datos=None):
    """
    Se encarga de crear los objetos asadas.
    Returns:
        _type_: Retorna los objetos asadas.
    """
    registros = obtener_lista_asadas(datos)
    asadas = []
    
    for registro in registros:
        try:
            asada = Asada.from_dict(registro)
            asadas.append(asada)
        except Exception as error:
            print("Error convirtiendo registro:", error)
    
    return asadas
