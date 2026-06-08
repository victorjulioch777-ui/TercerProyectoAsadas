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
            
            #Investigar como usar el patron de diseño reducer para evitar este if else gigante, o al menos abstraer cada caso a una función aparte para que sea mas legible
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
        #Sale blanco el close por que no esta typado
        socket_cliente.close()
        print(f"Cliente desconectado: {direccion}")
        
def procesar_busqueda_id(solicitud, arbol):
    id_asada = solicitud.get("id_asada")
    
    posicion = arbol.buscar(id_asada)
    
    if posicion is None:
        #Strings quemados
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
    #strings quemados, se pueden abstraer a constantes o a un archivo de configuración
    provincia = solicitud.get("provincia", "").strip().upper()
    canton = solicitud.get("canton", "").strip().upper()
    distrito = solicitud.get("distrito", "").strip().upper()
    
    
    #estructura no esta typada
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
