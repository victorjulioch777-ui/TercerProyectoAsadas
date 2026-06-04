from services.api_aresep import obtener_objetos_asadas
from storage.archivo_asadas import guardar_asadas, leer_asada_por_posicion
from structures.arbol_binario import arbol_binario_de_busqueda
from storage.archivo_arbol import guardar_arbol
from structures.listas_geograficas import lista_geografica
from storage.archivo_geografico import (
    guardar_estructura_geografica,
    cargar_estructura_geografica
)

def construir_arbol(lista_asadas, posiciones):
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
 
def main():
    asadas = obtener_objetos_asadas()

    print("Objetos ASADA cargados:", len(asadas))

    posiciones = guardar_asadas(asadas)
    print("Archivo binario data/asadas.dat creado correctamente.")

    arbol = construir_arbol(asadas, posiciones)
    guardar_arbol(arbol)
    print("Árbol binario guardado en data/indice_arbol.dat")
    
    estructura_geografica = construir_estructura_geografica(asadas, posiciones)
    guardar_estructura_geografica(estructura_geografica)
    print("Estructura geográfica guardada en data/estructura_geografica.dat")
    
    estructura = cargar_estructura_geografica()
    
    print("\nProvincias disponibles:")
    provincias = estructura.obtener_provincias()
    
    for provincia in provincias:
        print("-", provincia)
        
    provincia = input("\nDigite la provincia: ").strip().upper()
    cantones = estructura.obtener_cantones(provincia)
    
    if not cantones:
        print("No se encontraron cantones para esa provincia.")
        return
    
    print("\nCantones disponibles:")
    for canton in cantones:
        print("-", canton)
        
    canton = input("Digite el cantón: ").strip().upper()
    distritos = estructura.obtener_distritos(provincia, canton)
    
    if not distritos:
        print("No se encontraron distritos para ese cantón.")
        return 
    
    print("\nDistritos disponibles:")
    for distrito in distritos:
        print("-", distrito)
        
    distrito = input("\nDigite el distrito: ").strip().upper()
    asadas_distrito = estructura.obtener_asadas_por_distrito(
        provincia,
        canton,
        distrito
    )
    
    if not asadas_distrito:
        print("No se encontraron ASADAS para ese distrito.")
        return
    
    print("\nASADAS encontradas:")
    for referencia in asadas_distrito:
        asada = leer_asada_por_posicion(referencia["posicion_registro"])
        print("-------------------------------------------")
        print("ID:", asada["id_asada"])
        print("Operador:", asada["operador"])
        print("Provincia:", asada["provincia"])
        print("Cantón:", asada["canton"])
        print("Distrito:", asada["distrito"])    
    
if __name__ == "__main__":
    main()
