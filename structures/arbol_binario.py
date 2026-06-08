from models.nodo_arbol import nodo_arbol

class arbol_binario_de_busqueda:
    def __init__(self):
        self.raiz = None
        
    def insertar(self, id_asada, posicion_registro):
        nuevo_nodo = nodo_arbol(id_asada, posicion_registro)
        
        if self.raiz is None:
            self.raiz = nuevo_nodo
        else:
            self._insertar_iterativo(nuevo_nodo)

    def _insertar_iterativo(self, nuevo_nodo):
        nodo_actual = self.raiz

        while True:   
            
            if nuevo_nodo.id_asada < nodo_actual.id_asada:
                
                if nodo_actual.izquierdo is None:
                    nodo_actual.izquierdo = nuevo_nodo
                    return
                nodo_actual = nodo_actual.izquierdo
                
            elif nuevo_nodo.id_asada > nodo_actual.id_asada:
                if nodo_actual.derecho is None:
                    nodo_actual.derecho = nuevo_nodo
                    return
                nodo_actual = nodo_actual.derecho
                
            else:
                nodo_actual.posicion_registro = nuevo_nodo.posicion_registro
                return
                
    def buscar(self, id_asada):
        id_asada = int(id_asada)
        nodo_actual = self.raiz

        while nodo_actual is not None:
            if id_asada == nodo_actual.id_asada:
                return nodo_actual.posicion_registro

            if id_asada < nodo_actual.id_asada:
                nodo_actual = nodo_actual.izquierdo
            else:
                nodo_actual = nodo_actual.derecho
        
        return None
    
    def recorrido_inorden(self):
        resultado = []
        pila = []
        nodo_actual = self.raiz

        while pila or nodo_actual is not None:
            while nodo_actual is not None:
                pila.append(nodo_actual)
                nodo_actual = nodo_actual.izquierdo

            nodo_actual = pila.pop()
            resultado.append((nodo_actual.id_asada, nodo_actual.posicion_registro))
            nodo_actual = nodo_actual.derecho

        return resultado
