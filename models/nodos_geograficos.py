class nodo_asada_geografica:
    def __init__(self, id_asada, posicion_registro):
        self.id_asada = int(id_asada)
        self.posicion_registro = posicion_registro
        self.siguiente = None


class nodo_geografico:
    def __init__(self, nombre):
        self.nombre = nombre
        self.siguiente = None


class nodo_provincia(nodo_geografico):
    def __init__(self, nombre):
        super().__init__(nombre)
        self.cantones = None


class nodo_canton(nodo_geografico):
    def __init__(self, nombre):
        super().__init__(nombre)
        self.distritos = None


class nodo_distrito(nodo_geografico):
    def __init__(self, nombre):
        super().__init__(nombre)
        self.asadas = None