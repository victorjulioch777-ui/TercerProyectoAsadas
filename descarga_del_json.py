# Este script descarga datos en formato JSON desde un servicio web y los convierte en formato diccionario de python y los guarda en un archivo local.

import requests
import json

# URL del servicio web que proporciona los datos en formato JSON
url = "https://datos.aresep.go.cr/ws.datosabiertos/Services/IA/Asadas.svc/ObtenerInformacionUbicacionAsadas"

# Realizar la solicitud GET al servicio web
respuesta = requests.get(url)

# Convertir JSON a diccionario/lista de Python
datos = respuesta.json()

# Guardar los datos en un archivo JSON
with open("asadas.json", "w", encoding="utf-8") as archivo:
    json.dump(datos, archivo, indent=4, ensure_ascii=False)

print("Archivo guardado correctamente")
print(datos)

