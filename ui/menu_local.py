from services.sincronizador import sincronizar_datos, cargar_estructuras
from storage.archivo_asadas import leer_asada_por_posicion
from services.mapa_service import generar_mapa_asada

def mostrar_asada(asada):
    print("-----------------------------------")
    #Strings quemados
    print("ID:", asada["id_asada"])
    print("Operador:", asada["operador"])
    print("Provincia:", asada["provincia"])
    print("Cantón:", asada["canton"])
    print("Distrito:", asada["distrito"])
    print("Teléfono:", asada["telefono"])
    print("Correo:", asada["correo"])
    print("Tipo de sistema:", asada["tipo_sistema"])
    
def buscar_id():
    try:
        arbol, estructura = cargar_estructuras()
    except FileNotFoundError:
        print("Primero debe sincronizar los datos.")
        return 
    
    id_asada = input("Digite el id_Asada: ").strip()
    
    if not id_asada.isdigit():
        print("El id_Asada debe ser un número.")
        return 
    
    #Typar estos para que no salga en blanco todo feo
    posicion = arbol.buscar(id_asada)

    if posicion is None:
        print("No se encontró una ASADA con ese id.")
        return

    asada = leer_asada_por_posicion(posicion)
    
    print("\nASADA encontrada:")
    mostrar_asada(asada)
    
def buscar_por_ubicacion():
    try:
        arbol, estructura = cargar_estructuras()
    except FileNotFoundError:
        print("Primero debe sincronizar los datos.")
        return
    
    print("\nProvincias disponibles:")
    for provincia in estructura.obtener_provincias():
        print("-", provincia)
        
    provincia = input("\nDigite la provincia: ").strip().upper()
    
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
        print("No se encontraron distrios para ese cantón.")
        return
    
    print("\nDistritos disponibles:")
    for distrito in distritos:
        print("-", distrito)
        
    distrito = input("\nDigite distrito: ").strip().upper()
    
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
        mostrar_asada(asada)

def generar_mapa_por_id():
    try:
        arbol, estructura = cargar_estructuras()
    except FileNotFoundError:
        print("Primero debe sincronizar los datos.")
        return

    id_asada = input("Digite el id_Asada para generar el mapa: ").strip()

    if not id_asada.isdigit():
        print("El id_Asada debe ser un número.")
        return
    
    #Typar estos para que no salga en blanco todo feo
    posicion = arbol.buscar(id_asada)

    if posicion is None:
        print("No se encontró una ASADA con ese id.")
        return

    asada = leer_asada_por_posicion(posicion)
    generar_mapa_asada(asada)
        
def mostrar_menu_local():
    while True:
        print("\n====Sistema de consulta de ASADAS====")
        print("1. Sincronizar datos")
        print("2. Buscar ASADA por id_Asada")
        print("3. Buscar ASADAS por provincia, cantón, distrito")
        print("4. Generar mapa por id_Asada")
        print("5. Salir")
        
        opcion = input("Seleccion una opción: ").strip()
        
        #Magic number
        if opcion == "1":
            sincronizar_datos()
        elif opcion == "2":
            buscar_id()
        elif opcion == "3":
            buscar_por_ubicacion()
        elif opcion == "4":
            generar_mapa_por_id()
        elif opcion == "5":
            print("Saliendo del sistema...")
            break
        else:
            print("Opción inválida.")
