from services.api_aresep import obtener_objetos_asadas
from storage.archivo_asadas import guardar_asadas, leer_asada_por_posicion
from structures.arbol_binario import arbol_binario_de_busqueda
from storage.archivo_arbol import guardar_arbol, cargar_arbol

def construir_arbol(lista_asadas, posiciones):
    arbol = arbol_binario_de_busqueda()
    
    for asada in lista_asadas:
        posicion = posiciones[asada.id_asada]
        arbol.insertar(asada.id_asada, posicion)
    
    return arbol
 
def main():
    asadas = obtener_objetos_asadas()

    print("Objetos ASADA cargados:", len(asadas))

    posiciones = guardar_asadas(asadas)
    print("Archivo binario data/asadas.dat creado correctamente.")

    arbol = construir_arbol(asadas, posiciones)
    guardar_arbol(arbol)
    
    print("Árbol binario guardado en data/indice_arbol.dat")
    
    arbol_cargado = cargar_arbol()
    
    id_buscado = input("\nDigite el id_Asada que desea buscar: ").strip()

    if not id_buscado.isdigit():
        print("El id_Asada debe ser un número.")
        return
    
    posicion = arbol_cargado.buscar(id_buscado)
    
    if posicion is None:
        print("No se encontró una ASADA con ese id.")
    else:
        asada_encontrada = leer_asada_por_posicion(posicion)

        print("\nASADA leída desde archivo binario:")
        print("ID:", asada_encontrada["id_asada"])
        print("Operador:", asada_encontrada["operador"])
        print("Provincia:", asada_encontrada["provincia"])
        print("Cantón:", asada_encontrada["canton"])
        print("Distrito:", asada_encontrada["distrito"])    
    
if __name__ == "__main__":
    main()
