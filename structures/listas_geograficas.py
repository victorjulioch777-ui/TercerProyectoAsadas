import config

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
        provincia = self._buscar_provincia(asada.provincia)

        if provincia is None:
            provincia = self._crear_provincia(asada.provincia)
            self._insertar_provincia(provincia)
            
        canton = self._buscar_canton(provincia, asada.canton)
         
        if canton is None:
            canton = self._crear_canton(asada.canton)
            self._insertar_canton(provincia, canton)
        
        distrito = self._buscar_distrito(canton, asada.distrito)
         
        if distrito is None:
            distrito = self._crear_distrito(asada.distrito)
            self._insertar_distrito(canton, distrito)
            
        self._insertar_asada_ordenada(
            distrito,
            asada.id_asada,
            posicion_registro
        )
        
    def _crear_provincia(self, nombre):
        return nodo_provincia(self._normalizar_nombre(nombre))
    
    def _crear_canton(self, nombre):
        return nodo_canton(self._normalizar_nombre(nombre)) 
    
    def _crear_distrito(self, nombre):
        return nodo_distrito(self._normalizar_nombre(nombre))
    
    def _crear_referencia_asada(self, nodo_asada):
        return{
            config.CAMPO_ID_ASADA: nodo_asada.id_asada,
            config.CAMPO_POSICION_REGISTRO: nodo_asada.posicion_registro
        }
        
    def _insertar_provincia(self, provincia):
        self.provincias = self.insertar_nodo_al_final(
            self.provincias,
            provincia
        )    
    
    def _insertar_canton(self, provincia, canton):
        provincia.cantones = self.insertar_nodo_al_final(
            provincia.cantones,
            canton
        )
        
    def _insertar_distrito(self, canton, distrito):
        canton.distritos = self.insertar_nodo_al_final(
            canton.distritos,
            distrito
        )
        
    def insertar_nodo_al_final(self, cabeza, nuevo_nodo):
        if cabeza is None:
            return nuevo_nodo
        
        ultimo = self._obtener_ultimo_nodo(cabeza)
        ultimo.siguiente = nuevo_nodo
        
        return cabeza
    
    def _obtener_ultimo_nodo(self, cabeza):
        ultimo = None
        
        for nodo in self._recorrer_lista(cabeza):
            ultimo = nodo
            
        return ultimo
    
    def _insertar_asada_ordenada(self, distrito, id_asada, posicion_registro):
        nueva_asada = nodo_asada_geografica(id_asada, posicion_registro)
        
        if self._debe_insertar_asada_al_inicio(distrito, id_asada):
            self._insertar_asada_al_inicio(distrito, nueva_asada)
            return 
        
        nodo_anterior = self._buscar_nodo_anterior_asada(
            distrito.asadas,
            id_asada
        )
        
        self._insertar_asada_despues_de(nodo_anterior, nueva_asada)
        
    def _insertar_asada_al_inicio(self, distrito, nueva_asada):
        nueva_asada.siguiente = distrito.asadas
        distrito.asadas = nueva_asada

    def _debe_insertar_asada_al_inicio(self, distrito, id_asada):
        return distrito.asadas is None or id_asada < distrito.asadas.id_asada
        
    def _buscar_nodo_anterior_asada(self, cabeza, id_asada):
        actual = cabeza
        
        while (
            actual.siguiente is not None
            and actual.siguiente.id_asada < id_asada
        ):
            actual = actual.siguiente
            
        return actual
    
    def _insertar_asada_despues_de(self, nodo_anterior, nueva_asada):
        nueva_asada.siguiente = nodo_anterior.siguiente
        nodo_anterior.siguiente = nueva_asada
        
    def obtener_provincias(self):
        return self._obtener_nombres_desde_lista(self.provincias)
    
    def obtener_cantones(self, nombre_provincia):
        provincia = self._buscar_provincia(nombre_provincia)
        
        if provincia is None:
            return []
        
        return self._obtener_nombres_desde_lista(provincia.cantones)
    
    def obtener_distritos(self, nombre_provincia, nombre_canton):
        provincia = self._buscar_provincia(nombre_provincia)
        
        if provincia is None:
            return []
        
        canton = self._buscar_canton(provincia, nombre_canton)
        
        if canton is None:
            return []
        
        return self._obtener_nombres_desde_lista(canton.distritos)
    
    def obtener_asadas_por_distrito(
        self,
        nombre_provincia,
        nombre_canton,
        nombre_distrito
    ):
    
        provincia = self._buscar_provincia(nombre_provincia)
        
        if provincia is None:
            return []
        
        canton = self._buscar_canton(provincia, nombre_canton)
        
        if canton is None:
            return []
        
        distrito = self._buscar_distrito(canton, nombre_distrito)

        if distrito is None:
            return []

        return self._obtener_referencias_asadas(distrito.asadas)

    def _buscar_provincia(self, nombre):
        return self._buscar_nodo_por_nombre(self.provincias, nombre)

    def _buscar_canton(self, provincia, nombre):
        return self._buscar_nodo_por_nombre(provincia.cantones, nombre)

    def _buscar_distrito(self, canton, nombre):
        return self._buscar_nodo_por_nombre(canton.distritos, nombre)
    
    def _buscar_nodo_por_nombre(self, cabeza, nombre):
        nombre_normalizado = self._normalizar_nombre(nombre)
        
        for nodo in self._recorrer_lista(cabeza):
            if nodo.nombre == nombre_normalizado:
                return nodo
            
        return None
    
    def _obtener_nombres_desde_lista(self, cabeza):
        nombres = []
        
        for nodo in self._recorrer_lista(cabeza):
            nombres.append(nodo.nombre)
            
        return nombres
    
    def _obtener_referencias_asadas(self, cabeza):
        referencias = []
        
        for nodo_asada in self._recorrer_lista(cabeza):
            referencia = self._crear_referencia_asada(nodo_asada)
            referencias.append(referencia)
            
        return referencias
    
    def _recorrer_lista(self, cabeza):
        actual = cabeza
        
        while actual is not None:
            yield actual
            actual = actual.siguiente
            
    def _normalizar_nombre(self, nombre):
        if nombre is None:
            return ""
        
        return str(nombre).strip().upper()
