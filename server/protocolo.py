import json

def enviar_mensaje(socket_conexion, mensaje):
    datos_json = json.dumps(mensaje, ensure_ascii=False)
    datos_bytes = datos_json.encode("utf-8")
    socket_conexion.sendall(datos_bytes + b"\n")
    
def recibir_mensaje(socket_conexion):
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