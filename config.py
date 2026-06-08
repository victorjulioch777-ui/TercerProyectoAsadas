from pathlib import Path

base_dir = Path(__file__).resolve().parent

data_dir = base_dir / "data"

ruta_json_asadas = data_dir / "asadas.json"
ruta_archivo_asadas = data_dir / "asadas.dat"
ruta_archivo_arbol = data_dir / "indice_arbol.dat"
ruta_archivo_geografico = data_dir / "estructura_geografica.dat"
ruta_mapa = data_dir / "mapa.html"

data_dir.mkdir(exist_ok = True)

HOST = "127.0.0.1"
PORT = 5000

#Agregar mas constantes para que no hayan strings quemados y usarlas en todos los lados posibles
#Crear mas diccionarios si es lo considera necesario
CLAVES_ASADAS = {
    "ID": "ID",
    "OPERADOR": "Operador",
}

OPCIONES_CLIENTE = {
    "BUSCAR_ID": "1",
    
}