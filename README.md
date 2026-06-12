# 🚰 Sistema Distribuido de ASADAS

Un sistema completo y distribuido para la gestión y visualización de información sobre las ASADAS (Asociaciones Administradoras de Sistemas de Acueductos y Alcantarillados) de Costa Rica.

## 📋 Descripción

Este proyecto integra múltiples módulos para:
- **Descargar datos** de ASADAS desde servicios web externos
- **Procesar y almacenar** información geográfica y estructural
- **Visualizar datos** en mapas interactivos (por ID o completos)
- **Operar en modo local o distribuido** (cliente-servidor)

## 🎯 Características

✅ Descarga automática de datos en formato JSON desde servicios web públicos  
✅ Generación de mapas interactivos en HTML (por ID de ASADA o completos)  
✅ Almacenamiento eficiente de datos con estructuras personalizadas  
✅ Sistema cliente-servidor para consultas distribuidas  
✅ Interfaz de menú interactiva  
✅ Soporte para búsquedas por ID de ASADA  

## 📁 Estructura del Proyecto

```
TercerProyectoAsadas/
├── main.py                      # Punto de entrada principal
├── config.py                    # Configuración centralizada
├── requirements.txt             # Dependencias del proyecto
├── descarga_del_json.py        # Script para descargar datos
├── genera_mapa_html.py         # Generación de mapas interactivos (por ID)
├── data/                        # Almacenamiento de datos
│   ├── asadas.json             # Datos en formato JSON
│   ├── asadas.dat              # Datos procesados
│   ├── indice_arbol.dat        # Índice en estructura de árbol
│   ├── estructura_geografica.dat# Índice geográfico
│   └── mapa.html               # Mapa interactivo generado
├── ui/                          # Módulo de interfaz de usuario
│   └── menu_local.py           # Menú interactivo local
├── server/                      # Módulo servidor
│   └── server.py               # Lógica del servidor
├── client/                      # Módulo cliente
│   └── cliente.py              # Lógica del cliente
├── services/                    # Servicios auxiliares
├── models/                      # Modelos de datos
├── structures/                  # Estructuras de datos personalizadas
└── storage/                     # Gestión de almacenamiento
```

## 🚀 Instalación

### Requisitos previos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Pasos de instalación

1. **Clonar el repositorio**
```bash
git clone https://github.com/victorjulioch777-ui/TercerProyectoAsadas.git
cd TercerProyectoAsadas
```

2. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

## 📦 Dependencias

- **folium** - Generación de mapas interactivos
- **pyproj** - Transformación de proyecciones geográficas

## 💻 Uso

### Ejecución del programa principal
```bash
python main.py
python3 main.py
```

### Menú interactivo
El programa presenta un menú con las siguientes opciones:

```
==== SISTEMA DISTRIBUIDO DE ASADAS ===
1. Sistema local     - Operar en modo local
2. Iniciar servidor  - Iniciar el servidor distribuido
3. Iniciar cliente   - Conectarse como cliente
4. Salir             - Cerrar la aplicación
```

### Descargar datos de ASADAS
```bash
python descarga_del_json.py
```
Esto descargará los datos más recientes desde el servicio web de datos abiertos de ARESEP y los guardará en `data/asadas.json`

### Generar mapa interactivo
```bash
python genera_mapa_html.py
```
Genera un archivo `mapa.html` con la visualización interactiva de una ASADA específica por ID. El flujo principal del sistema utiliza esta funcionalidad para generar mapas según la consulta del usuario.

## ⚙️ Configuración

El archivo `config.py` contiene la configuración centralizada del proyecto:

| Variable | Valor | Descripción |
|----------|-------|-------------|
| `HOST` | 127.0.0.1 | Dirección IP del servidor |
| `PORT` | 5000 | Puerto de escucha del servidor |
| `data_dir` | `./data` | Directorio de almacenamiento de datos |
| `ruta_json_asadas` | `./data/asadas.json` | Ubicación del JSON de ASADAS |

## 📊 Datos

Los datos se obtienen del servicio web público de ARESEP:
- **URL:** `https://datos.aresep.go.cr/ws.datosabiertos/Services/IA/Asadas.svc/ObtenerInformacionUbicacionAsadas`
- **Formato:** JSON
- **Información incluida:** ID, Operador, Ubicación geográfica y más

## 🗺️ Visualización

El proyecto genera mapas interactivos usando **Folium**, permitiendo visualizar:
- Ubicación de ASADAS específicas por ID
- Información contextual de cada ASADA
- Capas geográficas

## 🔄 Arquitectura Distribuida

El sistema soporta una arquitectura cliente-servidor:

### Servidor
- Escucha conexiones en `127.0.0.1:5000`
- Procesa consultas de clientes
- Accede a la base de datos centralizada

### Cliente
- Se conecta al servidor
- Realiza consultas (búsqueda por ID, etc.)
- Recibe respuestas del servidor

## 📝 Documentación Externa

Consulta `Doc_externa.docx` para documentación adicional sobre el proyecto.

## 🛠️ Desarrollo

### Estructura de módulos
- **ui/** - Interfaz de usuario
- **server/** - Lógica del servidor
- **client/** - Lógica del cliente
- **services/** - Servicios reutilizables
- **models/** - Definición de modelos de datos
- **structures/** - Estructuras de datos especializadas
- **storage/** - Capas de almacenamiento

### Próximas mejoras
- [ ] Implementar más opciones de búsqueda avanzada
- [ ] Agregar autenticación en el sistema cliente-servidor
- [ ] Mejorar interfaz gráfica (GUI)
- [ ] Agregar tests unitarios
- [ ] Documentación de API

## 📄 Licencia

Este proyecto no cuenta con una licencia especificada. Consulta con el autor para obtener más información.

## 👤 Autor

**victorjulioch777-ui**

## 📞 Contacto

Para preguntas, sugerencias o reportes de bugs, abre un [issue](https://github.com/victorjulioch777-ui/TercerProyectoAsadas/issues) en el repositorio.

---

⭐ Si este proyecto te fue útil, considera darle una estrella en GitHub
