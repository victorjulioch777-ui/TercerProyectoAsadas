from typing import Any, Optional, Tuple

import config

from services.sincronizador import sincronizar_datos, cargar_estructuras
from storage.archivo_asadas import leer_asada_por_posicion
from services.mapa_service import generar_mapa_asada
from structures.arbol_binario import arbol_binario_de_busqueda
from structures.listas_geograficas import lista_geografica


AsadaDict = dict[str, Any]
ReferenciaAsada = dict[str, Any]
Estructuras = Tuple[arbol_binario_de_busqueda, lista_geografica]


def cargar_estructuras_seguro() -> Optional[Estructuras]:
    """ 
    Se encarga de cargar las estructuras de forma segura.
    Returns:
        Optional[Estructuras]: Arbol y lista geográfica si se cargan correctamente, None si no.
    """
    try:
        arbol, estructura = cargar_estructuras()
        return arbol, estructura

    except FileNotFoundError:
        print(config.MENSAJE_SIN_DATOS)
        return None


def pedir_id_asada(mensaje: str = config.PROMPT_ID_ASADA) -> Optional[str]:
    """
    Se encarga de pedir el id de una asada.
    Args:
        mensaje (str, optional): Mensaje que se muestra al usuario. Defaults to config.PROMPT_ID_ASADA.
    Returns:
        Optional[str]: Id de la asada.
    """
    id_asada = input(mensaje).strip()

    if not id_asada.isdigit():
        print(config.MENSAJE_ID_INVALIDO)
        return None

    return id_asada

# Función que se encarga de buscar una asada en el árbol.
def buscar_asada_en_arbol(
    arbol: arbol_binario_de_busqueda,
    id_asada: str
) -> Optional[AsadaDict]:
    
    posicion = arbol.buscar(id_asada)

    if posicion is None:
        print(config.MENSAJE_ASADA_NO_ENCONTRADA)
        return None

    return leer_asada_por_posicion(posicion)


def mostrar_asada(asada: AsadaDict) -> None:
    """
    Se encarga de mostrar la informacion de una asada.
    Args:
        asada (AsadaDict): Asada a mostrar.
    """
    print("-----------------------------------")

    for campo, etiqueta in config.ETIQUETAS_ASADA.items():
        print(f"{etiqueta}: {asada.get(campo, '')}")


def mostrar_lista(titulo: str, elementos: list[str]) -> None:
    """
    Se encarga de mostrar una lista de elementos.
    Args:
        titulo (str): Titulo de la lista.
        elementos (list[str]): Elementos de la lista.
    """
    print(f"\n{titulo}")

    for elemento in elementos:
        print("-", elemento)

# Se encarga de obtener las referencias de las asadas por ubicacion.
def obtener_referencias_por_ubicacion(
    estructura: lista_geografica,
    provincia: str,
    canton: str,
    distrito: str
) -> list[ReferenciaAsada]:
    
    return estructura.obtener_asadas_por_distrito(
        provincia,
        canton,
        distrito
    )

# Se encarga de mostrar las asadas desde las referencias.
def mostrar_asadas_desde_referencias(
    referencias: list[ReferenciaAsada]
) -> None:
    
    for referencia in referencias:
        posicion = referencia[config.CAMPO_POSICION_REGISTRO]
        asada = leer_asada_por_posicion(posicion)
        mostrar_asada(asada)

# Función que se encarga de buscar una asada por id.
def buscar_id() -> None:
    estructuras = cargar_estructuras_seguro()

    if estructuras is None:
        return

    arbol, _ = estructuras

    id_asada = pedir_id_asada()

    if id_asada is None:
        return

    asada = buscar_asada_en_arbol(arbol, id_asada)

    if asada is None:
        return

    print("\nASADA encontrada:")
    mostrar_asada(asada)


def buscar_por_ubicacion() -> None:
    """
    Se encarga de buscar una asada por ubicacion.
    """
    estructuras = cargar_estructuras_seguro()

    if estructuras is None:
        return

    _, estructura = estructuras

    provincias = estructura.obtener_provincias()
    mostrar_lista("Provincias disponibles:", provincias)

    provincia = input(f"\n{config.PROMPT_PROVINCIA}").strip().upper()

    cantones = estructura.obtener_cantones(provincia)

    if not cantones:
        print(config.MENSAJE_CANTONES_NO_ENCONTRADOS)
        return

    mostrar_lista("Cantones disponibles:", cantones)

    canton = input(f"\n{config.PROMPT_CANTON}").strip().upper()

    distritos = estructura.obtener_distritos(provincia, canton)

    if not distritos:
        print(config.MENSAJE_DISTRITOS_NO_ENCONTRADOS)
        return

    mostrar_lista("Distritos disponibles:", distritos)

    distrito = input(f"\n{config.PROMPT_DISTRITO}").strip().upper()

    referencias = obtener_referencias_por_ubicacion(
        estructura,
        provincia,
        canton,
        distrito
    )

    if not referencias:
        print(config.MENSAJE_ASADAS_NO_ENCONTRADAS_DISTRITO)
        return

    print("\nASADAS encontradas:")
    mostrar_asadas_desde_referencias(referencias)


def generar_mapa_por_id() -> None:
    """
    Se encarga de generar el mapa de una asada.
    """
    estructuras = cargar_estructuras_seguro()

    if estructuras is None:
        return

    arbol, _ = estructuras

    id_asada = pedir_id_asada(config.PROMPT_ID_ASADA_MAPA)

    if id_asada is None:
        return

    asada = buscar_asada_en_arbol(arbol, id_asada)

    if asada is None:
        return

    generar_mapa_asada(asada)


def mostrar_opciones_menu() -> None:
    print("\n==== Sistema de consulta de ASADAS ====")
    print(f"{config.OPCION_SINCRONIZAR}. Sincronizar datos")
    print(f"{config.OPCION_BUSCAR_ID}. Buscar ASADA por id_Asada")
    print(f"{config.OPCION_BUSCAR_UBICACION}. Buscar ASADAS por provincia, cantón, distrito")
    print(f"{config.OPCION_GENERAR_MAPA}. Generar mapa por id_Asada")
    print(f"{config.OPCION_SALIR}. Salir")


def procesar_opcion_menu(opcion: str) -> bool:
    acciones_menu = {
        config.OPCION_SINCRONIZAR: sincronizar_datos,
        config.OPCION_BUSCAR_ID: buscar_id,
        config.OPCION_BUSCAR_UBICACION: buscar_por_ubicacion,
        config.OPCION_GENERAR_MAPA: generar_mapa_por_id
    }

    if opcion == config.OPCION_SALIR:
        print(config.MENSAJE_SALIENDO)
        return False

    accion = acciones_menu.get(opcion)

    if accion is None:
        print(config.MENSAJE_OPCION_INVALIDA)
        return True

    accion()
    return True


def mostrar_menu_local() -> None:
    """
    Se encarga de mostrar el menu local.
    """
    continuar = True

    while continuar:
        mostrar_opciones_menu()
        opcion = input(config.PROMPT_OPCION).strip()
        continuar = procesar_opcion_menu(opcion)