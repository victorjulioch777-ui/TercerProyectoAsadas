import unicodedata

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
            
        canton = self._buscar_canton(provincia, asada.canton)
         
        if canton is None:
            canton = self._crear_canton(provincia, asada.canton)
        
        distrito = self._buscar_distrito(canton, asada.distrito)
         
        if distrito is None:
            distrito = self._crear_distrito(canton, asada.distrito)
            
        self._insertar_asada_ordenada(
            distrito,
            asada.id_asada,
            posicion_registro
        )

    def obtener_provincias(self):
        """
        Se encarga de obtener todas las provincias.

        Returns:
            _type_: Lista con los nombres de las provincias.
        """
        return self._obtener_nombres_desde_lista(self.provincias)
    
    def obtener_cantones(self, nombre_provincia):
        """
        Se encarga de obtener todos los cantones.
        
        Args:
            nombre_provincia (_type_): Nombre de la provincia.

        Returns:
            _type_: Lista con los nombres de los cantones.
        """
        provincia = self._buscar_provincia(nombre_provincia)
        
        if provincia is None:
            return []
        
        return self._obtener_nombres_desde_lista(provincia.cantones)
    
    def obtener_distritos(self, nombre_provincia, nombre_canton):
        """
        Se encarga de obtener todos los distritos.
        Args:
            nombre_provincia (_type_): Nombre de la provincia.
            nombre_canton (_type_): Nombre del cantón.

        Returns:
            _type_: Lista con los nombres de los distritos.
        """
        provincia = self._buscar_provincia(nombre_provincia)
        
        if provincia is None:
            return []
        
        canton = self._buscar_canton(provincia, nombre_canton)
        
        if canton is None:
            return []
        
        return self._obtener_nombres_desde_lista(canton.distritos)
    
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
        
        return self._obtener_referencias_asadas(distrito.asadas)
        
    def obtener_estadisticas(self):
        cantidad_provincias = 0
        cantidad_cantones = 0
        cantidad_distritos = 0
        cantidad_asadas = 0
        mayor_cantidad_asadas = -1
        distrito_con_mas_asadas = None
        
        for provincia in self._recorrer_lista(self.provincias):
            cantidad_provincias += 1
            
            for canton in self._recorrer_lista(provincia.cantones):
                cantidad_cantones += 1
                
                for distrito in self._recorrer_lista(canton.distritos):
                    cantidad_distritos += 1
                    cantidad_asadas_distrito = self._contar_lista(distrito.asadas)
                    cantidad_asadas += cantidad_asadas_distrito
                    
                    if cantidad_asadas_distrito > mayor_cantidad_asadas:
                        mayor_cantidad_asadas = cantidad_asadas_distrito
                        distrito_con_mas_asadas = (
                            f"{provincia.nombre} / {canton.nombre} / {distrito.nombre}"
                        )
        
        return {
            "cantidad_provincias": cantidad_provincias,
            "cantidad_cantones": cantidad_cantones,
            "cantidad_distritos": cantidad_distritos,
            "cantidad_asadas": cantidad_asadas,
            "distrito_con_mas_asadas": distrito_con_mas_asadas,
            "mayor_cantidad_asadas": mayor_cantidad_asadas
        }
                        
    def _crear_provincia(self, nombre):
        provincia = nodo_provincia(self._normalizar_nombre(nombre))
        self.provincias = self._insertar_nodo_ordenado(self.provincias, provincia)
        return provincia
    
    def _crear_canton(self, provincia, nombre):
        canton = nodo_canton(self._normalizar_nombre(nombre))
        provincia.cantones = self._insertar_nodo_ordenado(provincia.cantones, canton)
        return canton 
    
    def _crear_distrito(self, canton, nombre):
        distrito = nodo_distrito(self._normalizar_nombre(nombre))
        canton.distritos = self._insertar_nodo_ordenado(canton.distritos, distrito)
        return distrito   
     
    def _buscar_provincia(self, nombre):
        """
        Se encarga de buscar una provincia por nombre.
        
        Args:
            nombre (_type_): Nombre de la provincia.

        Returns:
            _type_: Provincia buscada.
        """
        return self._buscar_nodo_por_nombre(self.provincias, nombre)

    def _buscar_canton(self, provincia, nombre):
        """
        Se encarga de buscar un cantón por nombre.

        Args:
            provincia (_type_): Provincia donde se buscará.
            nombre (_type_): Nombre del cantón.

        Returns:
            _type_: Cantón buscado.
        """
        return self._buscar_nodo_por_nombre(provincia.cantones, nombre)

    def _buscar_distrito(self, canton, nombre):
        """
        Se encarga de buscar un distrito por nombre.        
        Args:
            canton (_type_): Cantón donde se buscará.
            nombre (_type_): Nombre del distrito.

        Returns:
            _type_: Retorna el distrito buscado.
        """
        return self._buscar_nodo_por_nombre(canton.distritos, nombre)
    
    def _buscar_nodo_por_nombre(self, cabeza, nombre):
        clave_buscada = self._clave_busqueda(nombre)
        
        for nodo in self._recorrer_lista(cabeza):
            if self._clave_busqueda(nodo.nombre) == clave_buscada:
                return nodo
            
        return None
    
    def _insertar_nodo_ordenado(self, cabeza, nuevo_nodo):
        if cabeza is None:
            return nuevo_nodo
        
        clave_nuevo = self._clave_busqueda(nuevo_nodo.nombre)
        clave_cabeza = self._clave_busqueda(cabeza.nombre)
        
        if clave_nuevo < clave_cabeza:
            nuevo_nodo.siguiente = cabeza
            return nuevo_nodo
        
        actual = cabeza
        
        while actual.siguiente is not None:
            clave_siguiente = self._clave_busqueda(actual.siguiente.nombre)
            
            if clave_nuevo <  clave_siguiente:
                break
            
            actual = actual.siguiente
            
        nuevo_nodo.siguiente = actual.siguiente
        actual.siguiente = nuevo_nodo
        
        return cabeza 
    
    def _insertar_asada_ordenada(self, distrito, id_asada, posicion_registro):
        id_asada = int(id_asada)

        if distrito.asadas is None:
            distrito.asadas = nodo_asada_geografica(id_asada, posicion_registro)
            return

        if id_asada < distrito.asadas.id_asada:
            nueva_asada = nodo_asada_geografica(id_asada, posicion_registro)
            nueva_asada.siguiente = distrito.asadas
            distrito.asadas = nueva_asada
            return

        if id_asada == distrito.asadas.id_asada:
            distrito.asadas.posicion_registro = posicion_registro
            return

        actual = distrito.asadas

        while (
            actual.siguiente is not None
            and actual.siguiente.id_asada < id_asada
        ):
            actual = actual.siguiente

        if (
            actual.siguiente is not None
            and actual.siguiente.id_asada == id_asada
        ):
            actual.siguiente.posicion_registro = posicion_registro
            return

        nueva_asada = nodo_asada_geografica(id_asada, posicion_registro)
        nueva_asada.siguiente = actual.siguiente
        actual.siguiente = nueva_asada
        
    def _obtener_nombres_desde_lista(self, cabeza):
        nombres = []

        for nodo in self._recorrer_lista(cabeza):
            nombres.append(nodo.nombre)

        return nombres

    def _obtener_referencias_asadas(self, cabeza):
        referencias = []

        for nodo_asada in self._recorrer_lista(cabeza):
            referencias.append(self._crear_referencia_asada(nodo_asada))

        return referencias

    def _crear_referencia_asada(self, nodo_asada):
        return {
            config.CAMPO_ID_ASADA: nodo_asada.id_asada,
            config.CAMPO_POSICION_REGISTRO: nodo_asada.posicion_registro
        }

    def _recorrer_lista(self, cabeza):
        actual = cabeza

        while actual is not None:
            yield actual
            actual = actual.siguiente

    def _contar_lista(self, cabeza):
        cantidad = 0

        for _ in self._recorrer_lista(cabeza):
            cantidad += 1

        return cantidad
    
    def _normalizar_nombre(self, nombre):
        if nombre is None:
            return "SIN DATO"

        texto = str(nombre).strip().upper()

        if texto == "":
            return "SIN DATO"

        return texto

    def _clave_busqueda(self, nombre):
        texto = self._normalizar_nombre(nombre)
        texto_normalizado = unicodedata.normalize("NFD", texto)

        return "".join(
            caracter
            for caracter in texto_normalizado
            if unicodedata.category(caracter) != "Mn"
        )