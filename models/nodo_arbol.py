class nodo_arbol:
    """
    Se encarga de representar un nodo del arbol.
    """
    def __init__(self, id_asada, posicion_registro):
        self.id_asada = int(id_asada)
        self.posicion_registro = int(posicion_registro)
        self.izquierdo = None
        self.derecho = None
        