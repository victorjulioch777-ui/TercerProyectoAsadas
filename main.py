from services.api_aresep import obtener_lista_asadas, obtener_metadata

def main():
    metadata = obtener_metadata()
    asadas = obtener_lista_asadas()
    
    print("JSON cargado correctamente.")
    print("Fuente:", metadata.get("source"))
    print("Fecha:", metadata.get("date"))
    print("Cantidad de ASADAS:", len(asadas))
    
    print("\nPrimera ASADA encontrada:")
    print("ID:", asadas[0].get("id_Asada"))
    print("Operador:", asadas[0].get("operador"))
    print("Provincia:", asadas[0].get("provincia")) 
    print("Cantón:", asadas[0].get("canton"))
    print("Distrito:", asadas[0].get("distrito"))
    
if __name__ == "__main__":
    main()