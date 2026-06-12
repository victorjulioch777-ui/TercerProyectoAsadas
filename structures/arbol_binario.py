from collections import deque

from models.nodo_arbol import nodo_arbol

class arbol_binario_de_busqueda:
    def __init__(self):
        """
        Se encarga de inicializar el arbol binario de busqueda.
        """
        self.raiz = None
        self.cantidad_nodos = 0
        
    def insertar(self, id_asada, posicion_registro):
        """
        Se encarga de insertar un nodo en el arbol binario de busqueda.
        
        Args:
            id_asada (int): ID de la ASADA.
            posicion_registro (int): Posicion del registro en el archivo binario.
        """
        nuevo_nodo = nodo_arbol(id_asada, posicion_registro)
        
        if self.raiz is None:
            self.raiz = nuevo_nodo
            self.cantidad_nodos += 1
            return
    
        self._insertar_iterativo(nuevo_nodo)

    def _insertar_iterativo(self, nuevo_nodo):
        """
        Se encarga de insertar un nodo de forma iterativa.
        
        Args:
            nuevo_nodo (nodo_arbol): Nodo a insertar.
        """
        nodo_actual = self.raiz

        while True:   
            
            if nuevo_nodo.id_asada < nodo_actual.id_asada:
                
                if nodo_actual.izquierdo is None:
                    nodo_actual.izquierdo = nuevo_nodo
                    self.cantidad_nodos += 1
                    return
                
                nodo_actual = nodo_actual.izquierdo
                
            elif nuevo_nodo.id_asada > nodo_actual.id_asada:
                if nodo_actual.derecho is None:
                    nodo_actual.derecho = nuevo_nodo
                    self.cantidad_nodos += 1
                    return
                
                nodo_actual = nodo_actual.derecho
                
            else:
                nodo_actual.posicion_registro = nuevo_nodo.posicion_registro
                return
      
    def construir_balanceado(self, pares_id_posicion):
        """
        Se encarga de construir el arbol binario de busqueda de forma balanceada.
        
        Args:
            pares_id_posicion (list): Lista de tuplas con el id_asada y la posicion_registro.
        """
        pares_ordenados = sorted(pares_id_posicion, key=lambda par: par[0])
        
        self.raiz = None
        self.cantidad_nodos = 0
        
        if not pares_ordenados:
            return
        
        pila = [{
            "inicio": 0,
            "fin": len(pares_ordenados) - 1,
            "padre": None,
            "lado": None
        }]
        
        while pila:
            tarea = pila.pop()
            inicio = tarea["inicio"]
            fin = tarea["fin"]
            
            if inicio > fin:
                continue
            
            mitad = (inicio + fin) // 2
            id_asada, posicion_registro = pares_ordenados[mitad]
            
            nuevo_nodo = nodo_arbol(id_asada, posicion_registro)
            
            if tarea["padre"] is None:
                self.raiz = nuevo_nodo
            elif tarea["lado"] == "izquierdo":
                tarea["padre"].izquierdo = nuevo_nodo
            else:
                tarea["padre"].derecho = nuevo_nodo
                
            self.cantidad_nodos += 1
            
            pila.append({
                "inicio": mitad + 1,
                "fin": fin,
                "padre": nuevo_nodo,
                "lado": "derecho"
            })
            
            pila.append({
                "inicio": inicio,
                "fin": mitad - 1,
                "padre": nuevo_nodo,
                "lado": "izquierdo"
            })
              
    def buscar(self, id_asada):
        """
        Se encarga de buscar un nodo en el arbol binario de busqueda.
        
        Args:
            id_asada (int): ID de la ASADA.
            
        Returns:
            int: Posicion del registro en el archivo binario.
        """
        try:
            id_asada = int(id_asada)
        except (TypeError, ValueError):
            return None
        
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
        """
        Se encarga de recorrer el arbol inorden.
        Returns:
            _type_: Lista de tuplas con el id_asada y la posicion_registro.
        """
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

    def altura(self):
        """
        Se encarga de calcular la altura del arbol binario de busqueda.
        
        Returns:
            int: Altura del arbol binario de busqueda.
        """
        if self.raiz is None:
            return 0
        
        altura_maxima = 0
        cola = deque([(self.raiz, 1)])
        
        while cola:
            nodo_actual, altura_actual = cola.popleft()
            altura_maxima = max(altura_maxima, altura_actual)
            
            if nodo_actual.izquierdo is not None:
                cola.append((nodo_actual.izquierdo, altura_actual + 1))
                
            if nodo_actual.derecho is not None:
                cola.append((nodo_actual.derecho, altura_actual + 1))
                
        return altura_maxima
    
    def estar_balanceado(self):
        """
        Se encarga de verificar si el arbol binario de busqueda esta balanceado.
        
        Returns:
            bool: True si el arbol binario de busqueda esta balanceado, False en caso contrario.
        """
        if self.raiz is None:
            return True
        
        alturas = {}
        pila = [(self.raiz, False)]
        
        while pila:
            nodo_actual, visitado = pila.pop()
            
            if nodo_actual is None:
                continue
            
            if visitado:
                altura_izquierda = alturas.get(id(nodo_actual.izquierdo), 0)
                altura_derecha = alturas.get(id(nodo_actual.derecho), 0)
                
                if abs(altura_izquierda - altura_derecha) > 1:
                    return False
                
                alturas[id(nodo_actual)] = 1 + max(
                    altura_izquierda,
                    altura_derecha
                )
            else:
                pila.append((nodo_actual, True))
                pila.append((nodo_actual.derecho, False))
                pila.append((nodo_actual.izquierdo, False))
                
        return True
    
    def obtener_estadisticas(self):
        """
        Se encarga de obtener las estadisticas del arbol binario de busqueda.
        
        Returns:
            dict: Diccionario con las estadisticas del arbol binario de busqueda.
        """
        return {
            "cantidad_nodos": self.cantidad_nodos,
            "altura": self.altura(),
            "balanceado": self.estar_balanceado()
        }