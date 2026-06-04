from services.api_aresep import obtener_objetos_asadas
from storage.archivo_asadas import guardar_asadas
from storage.archivo_arbol import guardar_arbol, cargar_arbol
from storage.archivo_geografico import guardar_estructura_geografica, cargar_estructura_geografica
from structures.arbol_binario import arbol_binario_de_busqueda
from structures.listas_geograficas import lista_geografica

def contruir_arbol(lista_asadas, posiciones):
    arbol = arbol_binario_de_busqueda()
    
    for asada in lista_asadas:
        posicion = posiciones[asada.id_asada]
        arbol.insertar(asada.id_asada, posicion)
        
    return arbol

def construir_estructura_geografica(lista_asadas, posiciones):
    estructura = lista_geografica()
    
    for asada in lista_asadas:
        posicion = posiciones[asada.id_asada]
        estructura.insertar_asada(asada, posicion)
        
    return estructura

def sincronizar_datos():
    print("Iniciando sincronización de datos...")
    
    lista_asadas = obtener_objetos_asadas()
    print("Objetos ASADA cargados:", len(lista_asadas))
    
    posiciones = guardar_asadas(lista_asadas)
    print("Archivo binario principal creado: data/asadas.dat")
    
    arbol = contruir_arbol(lista_asadas, posiciones)
    guardar_arbol(arbol)
    print("Índice de árbol binario creado: data/indice_arbol.dat")
    
    estructura_geografica = construir_estructura_geografica(lista_asadas, posiciones)
    guardar_estructura_geografica(estructura_geografica)
    print("Estructura geográfica creada: data/estructura_geografica.dat")
    
    print("Sincronización finalizada correctamente.")
    
    return {
        "cantidad_asadas": len(lista_asadas),
        "posiciones": posiciones,
        "arbol": arbol,
        "estructura_geografica": estructura_geografica
    }
    
def cargar_estructuras():
    arbol = cargar_arbol()
    estructura_geografica = cargar_estructura_geografica()
    
    return arbol, estructura_geografica