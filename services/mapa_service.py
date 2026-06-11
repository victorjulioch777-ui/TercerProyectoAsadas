import webbrowser
from pathlib import Path
from config import ruta_mapa

def convertir_crtm05_a_wgs84(coordenadas_x, coordenadas_y):
    """
    Se encarga de convertir las coordenadas de CRTM05 a WGS84.
    """
    from pyproj import Transformer

    x_crtm05 = float(str(coordenadas_x).strip())
    y_crtm05 = float(str(coordenadas_y).strip())
    
    transformer = Transformer.from_crs(
        "EPSG:5367",
        "EPSG:4326",
        always_xy=True
    )
    
    longitud, latitud = transformer.transform(x_crtm05, y_crtm05)
    
    return latitud, longitud

def generar_mapa_asada(asada):
    """
    Se encarga de generar un mapa interactivo con la ubicación de la ASADA.
    """
    try:
        import folium
        import pyproj
    except ModuleNotFoundError as error:
        print(f"No se puede generar el mapa porque falta instalar la librería {error.name}.")
        print("Ejecute: pip install -r requirements.txt")
        return

    latitud, longitud = convertir_crtm05_a_wgs84(
        asada["coordenadas_x"],
        asada["coordenadas_y"]
    )
    
    mapa = folium.Map(
        location=[latitud, longitud],
        zoom_start=15
    )
    
    popup = f"""
    <b>ID ASADA:</b> {asada["id_asada"]}<br>
    <b>Operador:</b> {asada["operador"]}<br>
    <b>Provincia:</b> {asada["provincia"]}<br>
    <b>Cantón:</b> {asada["canton"]}<br>
    <b>Distrito:</b> {asada["distrito"]}<br>
    <b>Teléfono:</b> {asada["telefono"]}<br>
    <b>Correo:</b> {asada["correo"]}<br>
    <b>Tipo de sistema:</b> {asada["tipo_sistema"]}<br>
    """
    
    folium.Marker(
        [latitud, longitud],
        popup = folium.Popup(popup, max_width=350),
        tooltip = f"ASADA {asada['id_asada']}"
    ).add_to(mapa)
    
    mapa.save(str(ruta_mapa))
    
    ruta_absoluta = Path(ruta_mapa).resolve()
    webbrowser.open(f"file://{ruta_absoluta}")
    
    print("Mapa generado correctamente:", ruta_absoluta)
