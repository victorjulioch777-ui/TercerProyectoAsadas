from pathlib import Path

base_dir = Path(__file__).resolve().parent

data_dir = base_dir / "data"

# Ubicacion de los archivos.
ruta_json_asadas = data_dir / "asadas.json"
ruta_archivo_asadas = data_dir / "asadas.dat"
ruta_archivo_arbol = data_dir / "indice_arbol.dat"
ruta_archivo_geografico = data_dir / "estructura_geografica.dat"
ruta_mapa = data_dir / "mapa.html"
ruta_metadata = data_dir / "metadata.json"

data_dir.mkdir(exist_ok = True)

HOST = "127.0.0.1"
PORT = 5000

# Claves para el archivo JSON.
CLAVES_ASADAS = {
    "ID": "ID",
    "OPERADOR": "Operador",
    "PROVINCIA": "Provincia",
    "CANTON": "Cantón",
    "DISTRITO": "Distrito",
    "TELEFONO": "Teléfono",
    "CORREO": "Correo",
    "TIPO_DE_SISTEMA": "Tipo de sistema"
}

# Opciones del cliente.
OPCIONES_CLIENTE = {
    "BUSCAR_ID": "1",
    "BUSCAR_UBICACION": "2",
    "SALIR": "3"
}

# Claves para el archivo JSON.
CLAVES_JSON_ASADA = {
    "ID_ASADA": "id_Asada",
    "ID_OBJETO": "id_Objecto",
    "OPERADOR": "operador",
    "TELEFONO": "telefono",
    "FAX": "fax",
    "CORREO": "correo",
    "TIPO_SISTEMA": "tipoSistema",
    "PROVINCIA": "provincia",
    "CANTON": "canton",
    "DISTRITO": "distrito",
    "CODIGO_DTA": "codigoDTA",
    "COORDENADA_X": "coordenadaX",
    "COORDENADA_Y": "coordenadaY"
}

# Claves para el archivo de datos.
CLAVES_ASADA = {
    "ID_ASADA": "id_asada",
    "ID_OBJETO": "id_objeto",
    "OPERADOR": "operador",
    "TELEFONO": "telefono",
    "FAX": "fax",
    "CORREO": "correo",
    "TIPO_SISTEMA": "tipo_sistema",
    "PROVINCIA": "provincia",
    "CANTON": "canton",
    "DISTRITO": "distrito",
    "CODIGO_DTA": "codigo_dta",
    "COORDENADA_X": "coordenadas_x",
    "COORDENADA_Y": "coordenadas_y"
}

# Claves de los campos del JSON de respuesta.
CAMPO_ACCION = "accion"
CAMPO_ESTADO = "estado"
CAMPO_MENSAJE = "mensaje"
CAMPO_DATOS = "datos"

# Estados de la respuesta.
ESTADO_OK = "ok"
ESTADO_ERROR = "error"

# Acciones del cliente.
ACCION_BUSCAR_ID = "buscar_id"
ACCION_BUSCAR_UBICACION = "buscar_ubicacion"
ACCION_SALIR = "salir"

# Campos del JSON de respuesta.
CAMPO_ID_ASADA = "id_asada"
CAMPO_PROVINCIA = "provincia"
CAMPO_CANTON = "canton"
CAMPO_DISTRITO = "distrito"
CAMPO_POSICION_REGISTRO = "posicion_registro"

# Mensajes del servidor.
MENSAJE_CONEXION_CERRADA = "Conexión cerrada."
MENSAJE_ACCION_INVALIDA = "Acción no válida."
MENSAJE_ASADA_NO_ENCONTRADA = "No se encontró una ASADA con ese id."
MENSAJE_UBICACION_SIN_ASADAS = "No se encontraron ASADAS para esa ubicación."  

# Atributos del JSON de respuesta.
ATR_PROVINCIAS = "provincias"
ATR_CANTONES = "cantones"
ATR_DISTRITOS = "distritos"
ATR_ASADAS = "asadas"

# Atributos del JSON de respuesta.
CAMPO_OPERADOR = "operador"
CAMPO_TELEFONO = "telefono"
CAMPO_CORREO = "correo"
CAMPO_TIPO_DE_SISTEMA = "tipo_sistema"
CAMPO_POSICION_REGISTRO = "posicion_registro"

# Etiquetas de las asadas.
ETIQUETAS_ASADA = {
    CAMPO_ID_ASADA: "ID",
    CAMPO_OPERADOR: "Operador",
    CAMPO_PROVINCIA: "Provincia",
    CAMPO_CANTON: "Cantón",
    CAMPO_DISTRITO: "Distrito",
    CAMPO_TELEFONO: "Teléfono",
    CAMPO_CORREO: "Correo",
    CAMPO_TIPO_DE_SISTEMA: "Tipo de sistema"
}

# Opciones del cliente.
OPCION_SINCRONIZAR = "1"
OPCION_BUSCAR_ID = "2"
OPCION_BUSCAR_UBICACION = "3"
OPCION_GENERAR_MAPA = "4"
OPCION_SALIR = "5"

# Mensajes del cliente.
MENSAJE_SIN_DATOS = "Primero debe sincronizar los datos."
MENSAJE_ID_INVALIDO = "El id_Asada debe ser un número."
MENSAJE_CANTONES_NO_ENCONTRADOS = "No se encontraron cantones para esa provincia."
MENSAJE_DISTRITOS_NO_ENCONTRADOS = "No se encontraron distritos para ese cantón."
MENSAJE_ASADAS_NO_ENCONTRADAS_DISTRITO = "No se encontraron asadas para ese distrito."
MENSAJE_SALIENDO = "Saliendo del sistema..."
MENSAJE_OPCION_INVALIDA = "Opción invalida."

# Prompts del cliente.
PROMPT_OPCION = "Seleccione una opción: "
PROMPT_ID_ASADA = "Digite el id_Asada: "
PROMPT_ID_ASADA_MAPA = "Digite el id_Asada para generar el mapa: "
PROMPT_PROVINCIA = "Digite la provincia: "
PROMPT_CANTON = "Digite el cantón: "
PROMPT_DISTRITO = "Digite el distrito: "

# Claves para la metadata.
CAMPO_METADATA = "metadata"
CAMPO_FECHA_METADATA = "date"

# Mensajes de la metadata.
MENSAJE_VERIFICANDO_ACTUALIZACION = "Verificando actualización de datos..."
MENSAJE_DATOS_ACTUALIZADOS = "Los datos ya estan actualizados. No se reconstruyeron los archivos."
MENSAJE_METADATA_NO_EXISTE = "No existe metadata local. Se reconstruirán los archivos."
MENSAJE_METADATA_CAMBIO = "Se detectó una actualización en la metadata."
MENSAJE_RECONSTRUYENDO = "Reconstruyendo archivos y estructuras..."
MENSAJE_METADATA_GUARDADA = "METADATA LOCAL ACTUALIZADA CORRECTAMENTE."

URL_ARESEP_ASADAS = (
    "https://datos.aresep.go.cr/ws.datosabiertos/Services/IA/Asadas.svc/"
    "ObtenerInformacionUbicacionAsadas"
)

TIEMPO_CONEXION_API = 10
TIEMPO_LECTURA_API = 60
INTENTOS_DESCARGA_API = 3

MENSAJE_DESCARGANDO_DATOS = "Descargando datos desde ARESEP..."
MENSAJE_JSON_LOCAL_ACTUALIZADO = "JSON local actualizado correctamente."
MENSAJE_ERROR_DESCARGA = "No se pudieron descargar los datos desde ARESEP."
MENSAJE_REINTENTO_DESCARGA = "Reintentando descarga desde ARESEP..."
MENSAJE_USANDO_JSON_LOCAL = "Se usará el JSON local como respaldo."
