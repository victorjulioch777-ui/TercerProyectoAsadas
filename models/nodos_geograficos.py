class nodo_asada_geografica:
    def __init__(self, id_asada, posicion_registro):
        self.id_asada = int(id_asada)
        self.posicion_registro = posicion_registro
        self.siguiente = None
        
class nodo_distrito:
    def __init__(self, nombre):
        self.nombre = nombre
        self.asadas = None
        self.siguiente = None
        
class nodo_canton:
    def __init__(self, nombre):
        self.nombre = nombre
        self.distritos = None
        self.siguiente = None
        
class nodo_provincia:
    def __init__(self, nombre):
        self.nombre = nombre
        self.cantones = None
        self.siguiente = None