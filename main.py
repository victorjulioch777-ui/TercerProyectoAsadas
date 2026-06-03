from services.api_aresep import obtener_lista_asadas, obtener_metadata, obtener_objetos_asadas
from storage.archivo_asadas import guardar_asadas, leer_asada_por_posicion

def main():
    asadas = obtener_objetos_asadas()

    print("Objetos ASADA cargados:", len(asadas))

    posiciones = guardar_asadas(asadas)

    print("Archivo binario data/asadas.dat creado correctamente.")
    print("Cantidad de posiciones guardadas:", len(posiciones))

    primera_asada = asadas[0]
    posicion_primera = posiciones[primera_asada.id_asada]

    print("\nPrimera ASADA:")
    print("ID:", primera_asada.id_asada)
    print("Posición en archivo binario:", posicion_primera)

    asada_leida = leer_asada_por_posicion(posicion_primera)

    print("\nASADA leída desde archivo binario:")
    print("ID:", asada_leida["id_asada"])
    print("Operador:", asada_leida["operador"])
    print("Provincia:", asada_leida["provincia"])
    print("Cantón:", asada_leida["canton"])
    print("Distrito:", asada_leida["distrito"])    
    
if __name__ == "__main__":
    main()