import pickle

from config import ruta_archivo_geografico

def guardar_estructura_geografica(estructura_geografica):
    with open(ruta_archivo_geografico, "wb")as archivo:
        pickle.dump(estructura_geografica, archivo)
        
def cargar_estructura_geografica():
    with open(ruta_archivo_geografico, "rb")as archivo:
        return pickle.load(archivo)