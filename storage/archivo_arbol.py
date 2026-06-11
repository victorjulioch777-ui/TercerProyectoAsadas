import pickle

from config import ruta_archivo_arbol

def guardar_arbol(arbol):
    """
    Se encarga de guardar el árbol binario de búsqueda en un archivo.
    
    Args:
        arbol (_type_): El árbol binario de búsqueda a guardar.
    """
    with open(ruta_archivo_arbol, "wb")as archivo:
        pickle.dump(arbol, archivo, protocol=pickle.HIGHEST_PROTOCOL)
        
def cargar_arbol():
    """
    Se encarga de cargar el árbol binario de búsqueda desde un archivo.
    
    Returns:
        _type_: El árbol binario de búsqueda cargado.
    """
    with open(ruta_archivo_arbol, "rb")as archivo:
        return pickle.load(archivo)