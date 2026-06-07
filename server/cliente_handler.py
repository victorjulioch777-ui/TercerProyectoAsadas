from server.protocolo import recibir_mensaje, enviar_mensaje
from services.sincronizador import cargar_estructuras
from storage.archivo_asadas import leer_asada_por_posicion

def atender_cliente(socket_cliente, direccion):
    print(f"Cliente conectado: {direccion}")
    
    try:
        arbol, estructura = cargar_estructuras()
        
        while True:
            solicitud = recibir_mensaje(socket_cliente)
            
            if solicitud is None:
                break
            
            accion = solicitud.get("accion")
            
            if accion == "buscar_id":
                respuesta = procesar_busqueda_id(solicitud, arbol)
            elif accion == "buscar_ubicacion":
                respuesta = procesar_busqueda_ubicacion(solicitud, estructura)
            elif accion == "salir":
                respuesta = {
                    "estado": "ok",
                    "mensaje": "Conexión cerrada."
                }
                enviar_mensaje(socket_cliente, respuesta)
                break    
            else:
                respuesta = {
                    "estado": "error", 
                    "mensaje": "Acción no válida."
                }
                
            enviar_mensaje(socket_cliente, respuesta)
            
    except Exception as error:
        print("Error atendiendo cliente:", error)
    finally:
        socket_cliente.close()
        print(f"Cliente desconectado: {direccion}")
        
def procesar_busqueda_id(solicitud, arbol):
    id_asada = solicitud.get("id_asada")
    
    posicion = arbol.buscar(id_asada)
    
    if posicion is None:
        return {
            "estado": "error",
            "mensaje": "No se encontró una ASADA con ese id."
        }
            
    asada = leer_asada_por_posicion(posicion)
    
    return {
        "estado": "ok",
        "datos": asada
    }
    
def procesar_busqueda_ubicacion(solicitud, estrucutura):
    provincia = solicitud.get("provincia", "").strip().upper()
    canton = solicitud.get("canton", "").strip().upper()
    distrito = solicitud.get("distrito", "").strip().upper()
    
    referencias = estrucutura.obtener_asadas_por_distrito(
        provincia,
        canton,
        distrito
    )
    
    if not referencias:
        return {
            "estado": "error",
            "mensaje": "No se encontraron ASADAS para esa ubicación."
        }
        
    asadas = []
    
    for referencia in referencias:
        asada = leer_asada_por_posicion(referencia["posicion_registro"])
        asadas.append(asada)
        
    return {
        "estado": "ok", 
        "datos": asadas
    }
