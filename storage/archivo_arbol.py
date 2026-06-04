import pickle

from config import ruta_archivo_arbol

def guardar_arbol(arbol):
    with open(ruta_archivo_arbol, "wb")as archivo:
        pickle.dump(arbol, archivo)
        
def cargar_arbol():
    with open(ruta_archivo_arbol, "rb")as archivo:
        return pickle.load(archivo)