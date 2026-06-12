import pickle

from config import ruta_archivo_geografico

def guardar_estructura_geografica(estructura_geografica):
    """
    Se encarga de guardar la estructura geografica.
    Args:
        estructura_geografica (_type_): Diccionario con la estructura geografica.
    """
    ruta_archivo_geografico.parent.mkdir(parents=True, exist_ok=True)
    
    with open(ruta_archivo_geografico, "wb")as archivo:
        pickle.dump(estructura_geografica, archivo, protocol=pickle.HIGHEST_PROTOCOL)
        
def cargar_estructura_geografica():
    """
    Se encarga de cargar la estructura geografica del archivo binario.
    Returns:
        _type_: Datos de la estructura geografica.
    """
    with open(ruta_archivo_geografico, "rb")as archivo:
        return pickle.load(archivo)