import json 
import config
import requests
from models.asada import Asada

class error_datos_aresep(Exception):
    """
    Se encarga de representar un error en los datos de ARESEP.
    """
    pass

def validar_datos_aresep(datos):
    """
    Se encarga de validar los datos de ARESEP.
    """
    if not isinstance(datos, dict):
        raise error_datos_aresep("La respuesta de ARESEP no tiene formato de diccionario.")
    
    if "metadata" not in datos:
        raise error_datos_aresep("La respuesta de ARESEP no contiene metadata.")
    
    if "value" not in datos:
        raise error_datos_aresep("La respuesta de ARESEP no contiene la lista de ASADAS.")
    
    if not isinstance(datos["value"], list):
        raise error_datos_aresep("El campo value de ARESEP no es una lista.")

def descargar_datos_aresep():
    """
    Se encarga de descargar los datos de ARESEP.
    """
    print(config.MENSAJE_DESCARGANDO_DATOS)

    respuesta = requests.get(
        config.URL_ARESEP_ASADAS,
        timeout = config.TIEMPO_ESPERA_API
    )

    respuesta.raise_for_status()
    
    datos = respuesta.json()
    validar_datos_aresep(datos)
    
    return datos

def guardar_json_local(datos):
    """
    Se encarga de guardar los datos de ARESEP en un archivo JSON local.
    """
    with open(config.ruta_json_asadas, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=4, ensure_ascii=False)
        
    print(config.MENSAJE_JSON_LOCAL_ACTUALIZADO)

def cargar_json_local():
    """
    Se encarga de cargar los datos de ARESEP desde un archivo JSON local.
    """
    with open(config.ruta_json_asadas, "r", encoding="utf-8")as archivo:
        return json.load(archivo)

def cargar_json_local_seguro():
    """
    Se encarga de cargar los datos de ARESEP desde un archivo JSON local de manera segura.
    """
    try:
        datos = cargar_json_local()
        validar_datos_aresep(datos)
        return datos
    except FileNotFoundError:
        print(config.MENSAJE_JSON_LOCAL_NO_DISPONIBLES)
        raise
    
    except json.JSONDecodeError:
        print(config.MENSAJE_JSON_LOCAL_INVALIDO)
        raise
    
    except error_datos_aresep:
        print(config.MENSAJE_JSON_LOCAL_INVALIDO)
        raise

def obtener_datos_aresep():
    """
    Se encarga de obtener los datos de ARESEP.
    """
    try:
        datos = descargar_datos_aresep()
        guardar_json_local(datos)
        
        return {
            "datos": datos,
            "origen": "remoto"
        }
        
    except (requests.RequestException, error_datos_aresep):
        print(config.MENSAJE_ERROR_DESCARGA)
        print(config.MENSAJE_USANDO_JSON_LOCAL)
        
        datos = cargar_json_local_seguro()
        
        return {
            "datos": datos,
            "origen": "local"
        }
    
def obtener_lista_asadas(datos=None):
    """
    Se encarga de obtener la lista de ASADAS.
    """
    if datos is None:
        datos = cargar_json_local()
        
    return datos["value"]

def obtener_metadata(datos=None):
    """
    Se encarga de obtener la metadata.
    """
    if datos is None:
        datos = cargar_json_local()
        
    return datos["metadata"]

def obtener_objetos_asadas(datos=None):
    """
    Se encarga de obtener los objetos ASADA desde los datos de ARESEP.
    """
    registros = obtener_lista_asadas(datos)
    asadas = []
    errores = []
    
    for indice, registro in enumerate(registros):
        try:
            asada = Asada.from_dict(registro)
            asadas.append(asada)
            
        except (ValueError, TypeError, KeyError) as error:
            id_asada = registro.get("id_asada", "SIN_ID")
            
            errores.append({
                "indice": indice,
                "id_asada": id_asada,
                "error": str(error)                
            })
            
            print(
                f"Error conviertiendo registro {indice}"
                f"(id_Asada={id_asada}): {error}"
            )
            
    if not asadas:
        raise error_datos_aresep("No se pudo convertir ninguna ASADA.")
    
    if errores:
        print(f"Registros con error al convertir: {len(errores)}")
        
    return asadas
