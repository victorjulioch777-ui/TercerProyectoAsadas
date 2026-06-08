from models.nodos_geograficos import (
    nodo_provincia,
    nodo_canton,
    nodo_distrito,
    nodo_asada_geografica
)

class lista_geografica:
    def __init__(self):
        self.provincias = None
        
    def insertar_asada(self, asada, posicion_registro):
        provincia = self._obtener_o_crear_provincia(asada.provincia)
        canton = self._obtener_o_crear_canton(provincia, asada.canton)
        distrito = self._obtener_o_crear_distrito(canton, asada.distrito)
        
        self._insertar_asada_ordenada(
            distrito,
            asada.id_asada,
            posicion_registro
        )
        
    #Separar esto en funciones que solo tengan 1 responsabilidad
    #1 para obtener, otra para crear, otra para insertar 
    def _obtener_o_crear_provincia(self, nombre):
        actual = self.provincias
        anterior = None
        
        while actual is not None:
            if actual.nombre == nombre:
                return actual
            anterior = actual
            actual = actual.siguiente
            
        nuevo = nodo_provincia(nombre)
        
        if anterior is None:
            self.provincias = nuevo
        else:
            anterior.siguiente = nuevo
        
        return nuevo 
    
    #Mismo que lo de arriba
    def _obtener_o_crear_canton(self, provincia, nombre):
        actual = provincia.cantones
        anterior = None
        
        while actual is not None:
            if actual.nombre == nombre:
                return actual
            anterior = actual
            actual = actual.siguiente
            
        nuevo = nodo_canton(nombre)    
            
        if anterior is None:
            provincia.cantones = nuevo
        else:
            anterior.siguiente = nuevo
            
        return nuevo
    
    #Mismo que lo de arriba
    def _obtener_o_crear_distrito(self, canton, nombre):
        actual = canton.distritos
        anterior = None
        
        while actual is not None:
            if actual.nombre == nombre:
                return actual 
            anterior = actual 
            actual = actual.siguiente
            
        nuevo = nodo_distrito(nombre)
        
        if anterior is None:
            canton.distritos = nuevo
        else:
            anterior.siguiente = nuevo
            
        return nuevo
    
    def _insertar_asada_ordenada(self, distrito, id_asada, posicion_registro):
        nuevo = nodo_asada_geografica(id_asada, posicion_registro)
        
        if distrito.asadas is None or id_asada < distrito.asadas.id_asada:
            nuevo.siguiente = distrito.asadas
            distrito.asadas = nuevo
            return
        
        actual = distrito.asadas
        
        while actual.siguiente is not None and actual.siguiente.id_asada < id_asada:
            actual = actual.siguiente
            
        nuevo.siguiente = actual.siguiente
        actual.siguiente = nuevo
        
    def obtener_provincias(self):
        resultado = []
        actual = self.provincias
        
        while actual is not None:
            resultado.append(actual.nombre) 
            #Esta logica del while se repetire varias veces en este archivo, se puede abstraer a una función aparte que reciba el nodo inicial y una función para extraer el dato que se quiere guardar en el resultado
            actual = actual.siguiente
            
        return resultado
    
    def obtener_cantones(self, nombre_provincia):
        provincia = self._buscar_provincia(nombre_provincia)
        
        if provincia is None:
            return []
        
        resultado = []
        actual = provincia.cantones
        
        while actual is not None:
            resultado.append(actual.nombre)
            actual = actual.siguiente
            
        return resultado
    
    def obtener_distritos(self, nombre_provincia, nombre_canton):
        provincia = self._buscar_provincia(nombre_provincia)
        
        if provincia is None:
            return []
        
        canton = self._buscar_canton(provincia, nombre_canton)
        
        if canton is None:
            return []
        
        resultado = []
        actual = canton.distritos
        
        while actual is not None:
            resultado.append(actual.nombre)
            actual = actual.siguiente
            
        return resultado 
    
    def obtener_asadas_por_distrito(self, nombre_provincia, nombre_canton, nombre_distrito):
        provincia = self._buscar_provincia(nombre_provincia)
        
        if provincia is None:
            return []
        
        canton = self._buscar_canton(provincia, nombre_canton)
        
        if canton is None:
            return []
        
        distrito = self._buscar_distrito(canton, nombre_distrito)
        
        if distrito is None:
            return []
        
        resultado = []
        actual = distrito.asadas
        
        while actual is not None:
            resultado.append({
                "id_asada": actual.id_asada, 
                "posicion_registro": actual.posicion_registro
            })
            actual = actual.siguiente
            
        return resultado
    
    def _buscar_provincia(self, nombre):
        actual = self.provincias
        
        while actual is not None: #Este while se repite varias veces, se puede abstraer a una función aparte que reciba el nodo inicial y una función para comparar el nombre con el nodo actual
            if actual.nombre == nombre:
                return actual
            actual = actual.siguiente
            
        return None
    
    def _buscar_canton(self, provincia, nombre):
        actual = provincia.cantones
        
        while actual is not None:
            if actual.nombre == nombre:
                return actual
            actual = actual.siguiente
            
        return None
    
    def _buscar_distrito(self, canton, nombre):
        actual = canton.distritos
        
        while actual is not None:
            if actual.nombre == nombre:
                return actual
            actual = actual.siguiente
            
        return None
