from services.sincronizador import sincronizar_datos, cargar_estructuras
from storage.archivo_asadas import leer_asada_por_posicion

def probar_busqueda_por_id(arbol):
    id_asada = input("\nDigite el id_Asada que desea buscar: ")
    
    posicion = arbol.buscar(id_asada)
    
    if posicion is None:
        print("No se encontró una ASADA con ese id.")
        return
    
    asada = leer_asada_por_posicion(posicion)
     
    print("\nASADAS encontradas:")
    print("ID:", asada["id_asada"])
    print("Operador:", asada["operador"])
    print("Provincia:", asada["provincia"])
    print("Cantón:", asada["canton"])
    print("Distrito:", asada["distrito"])

def probar_busqueda_geografica(estructura):
    print("\nProvincias disponibles:")
    for provincia in estructura.obtener_provincias():
        print("-", provincia)
        
    provincia = input("\nDigite provincia: ").strip().upper()
    
    cantones = estructura.obtener_cantones(provincia)
    
    if not cantones:
        print("No se encontraron cantones para esa provincia.")
        return
    
    print("\nCantones disponibles:")
    for canton in cantones:
        print("-", canton)
        
    canton = input("\nDigite el cantón: ").strip().upper()
    
    distritos = estructura.obtener_distritos(provincia, canton)
    
    if not distritos:
        print("No se encontraron distritos para ese cantón.")
        return
    
    print("\nDistritos disponibles:")
    for distrito in distritos:
        print("-", distrito)
        
    distrito = input("\nDigite el distrito: ").strip().upper()
    
    referencias = estructura.obtener_asadas_por_distrito(
        provincia,
        canton,
        distrito
    )   
    
    if not referencias:
        print("No se encontraron ASADAS para ese distrito.")
        return 
    
    print("\nASADAS encontradas:")
    
    for referencia in referencias:
        asada = leer_asada_por_posicion(referencia["posicion_registro"])
        
        print("----------------------------------------------------")
        print("ID:", asada["id_asada"])
        print("Operador:", asada["operador"])
        print("Provincia:", asada["provincia"])
        print("Cantón:", asada["canton"])
        print("Distrito:", asada["distrito"])
        
def main():
    sincronizar_datos()
    
    arbol, estructura = cargar_estructuras()
    
    while True:
        print("\n==== Sistema de consulta de ASADAS ====")
        print("1. Buscar ASADA por id")
        print("2. Buscar ASADAS por provincia, canton y distrito")
        print("3. Salir")
        
        opcion = input("Selecciones una opción: ")
        
        if opcion == "1":
            probar_busqueda_por_id(arbol)
        elif opcion == "2":
            probar_busqueda_geografica(estructura)
        elif opcion == "3":
            print("Saliendo del sistema...")
            break
        else:
            print("Opción inválida.")
            
if __name__ == "__main__":
    main()
