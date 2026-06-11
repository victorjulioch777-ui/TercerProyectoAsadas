import json

def enviar_mensaje(socket_conexion, mensaje):
    """
    Se encarga de enviar un mensaje al cliente.
    
    Args:
        socket_conexion (_type_): Socket de conexion.
        mensaje (_type_): Mensaje a enviar.
    """
    datos_json = json.dumps(mensaje, ensure_ascii=False)
    datos_bytes = datos_json.encode("utf-8")
    socket_conexion.sendall(datos_bytes + b"\n")
    
def recibir_mensaje(socket_conexion):
    """
    Se encarga de recibir los mensajes del cliente.
    
    Args:
        socket_conexion (_type_): Socket de conexion.

    Returns:
        _type_: Retorna el mensaje recibido.
    """
    datos = b""
    
    while True:
        parte = socket_conexion.recv(4096)
        
        if not parte:
            return None
        
        datos += parte
        
        if b"\n" in datos:
            break
        
    mensaje_json = datos.decode("utf-8").strip()
    return json.loads(mensaje_json)