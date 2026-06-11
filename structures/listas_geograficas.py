import config

from models.nodos_geograficos import (
    nodo_provincia,
    nodo_canton,
    nodo_distrito,
    nodo_asada_geografica
)

class lista_geografica:
    """
    Se encarga de implementar una lista geografica.
    """
    def __init__(self):
        self.provincias = None
        
    def insertar_asada(self, asada, posicion_registro):
        """
        Se encarga de insertar una asada en la lista geografica.
        Args:
            asada (_type_): Asada a insertar.
            posicion_registro (_type_): Posición del registro en el archivo.
        """
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
        """
        Se encarga de crear una provincia.
        Args:
            nombre (_type_): Nombre de la provincia.

        Returns:
            _type_: Nodo con el nombre de la provincia.
        """
        return nodo_provincia(self._normalizar_nombre(nombre))
    
    def _crear_canton(self, nombre):
        """
        Se encarga de crear un cantón.
        Args:
            nombre (_type_): Nombre del cantón.

        Returns:
            _type_: Nodo con el nombre del cantón.
        """
        return nodo_canton(self._normalizar_nombre(nombre)) 
    
    def _crear_distrito(self, nombre):
        """
        Se encarga de crear un distrito.
        Args:
            nombre (_type_): Nombre del distrito.

        Returns:
            _type_: Nodo con el nombre del distrito.
        """
        return nodo_distrito(self._normalizar_nombre(nombre))
    
    def _crear_referencia_asada(self, nodo_asada):
        """
        Se encarga de crear una referencia a una asada.
        Args:
            nodo_asada (_type_): Nodo con la información de la asada.

        Returns:
            _type_: Diccionario con la información de la asada.
        """
        return{
            config.CAMPO_ID_ASADA: nodo_asada.id_asada,
            config.CAMPO_POSICION_REGISTRO: nodo_asada.posicion_registro
        }
        
    def _insertar_provincia(self, provincia):
        """
        Se encarga de insertar una provincia en la lista de provincias.
        Args:
            provincia (_type_): Provincia a insertar.
        """
        self.provincias = self.insertar_nodo_al_final(
            self.provincias,
            provincia
        )    
    
    def _insertar_canton(self, provincia, canton):
        """
        Se encarga de insertar un cantón en la lista de cantones.
        Args:
            provincia (_type_): Provincia a la que se le insertará el cantón.
            canton (_type_): Cantón a insertar.
        """
        provincia.cantones = self.insertar_nodo_al_final(
            provincia.cantones,
            canton
        )
        
    def _insertar_distrito(self, canton, distrito):
        """
        Se encarga de insertar un distrito en la lista de distritos.
        Args:
            canton (_type_): Cantón al que se le insertará el distrito.
            distrito (_type_): Distrito a insertar.
        """
        canton.distritos = self.insertar_nodo_al_final(
            canton.distritos,
            distrito
        )
        
    def insertar_nodo_al_final(self, cabeza, nuevo_nodo):
        """
        Se encarga de insertar un nodo al final de una lista enlazada.
        Args:
            cabeza (_type_): Cabeza de la lista enlazada.
            nuevo_nodo (_type_): Nodo a insertar.

        Returns:
            _type_: Cabeza de la lista enlazada con el nuevo nodo insertado.
        """
        if cabeza is None:
            return nuevo_nodo
        
        ultimo = self._obtener_ultimo_nodo(cabeza)
        ultimo.siguiente = nuevo_nodo
        
        return cabeza
    
    def _obtener_ultimo_nodo(self, cabeza):
        """
        Se encarga de obtener el último nodo de una lista enlazada.
        Args:
            cabeza (_type_): Cabeza de la lista enlazada.

        Returns:
            _type_: Último nodo de la lista enlazada.
        """
        ultimo = None
        
        for nodo in self._recorrer_lista(cabeza):
            ultimo = nodo
            
        return ultimo
    
    def _insertar_asada_ordenada(self, distrito, id_asada, posicion_registro):
        """
        Se encarga de insertar una asada en la lista de asadas de un distrito.
        Args:
            distrito (_type_): Distrito al que se le insetará la asada.
            id_asada (_type_): ID de la asada a insertar.
            posicion_registro (_type_): Posición del registro de la asada.
        """
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
        """
        Se encarga de insertar una asada al inicio de la lista de asadas.
        Args:
            distrito (_type_): Distrito al que se le insertará la asada.
            nueva_asada (_type_): Asada a insertar.
        """
        nueva_asada.siguiente = distrito.asadas
        distrito.asadas = nueva_asada

    def _debe_insertar_asada_al_inicio(self, distrito, id_asada):
        """
        Se encarga de verificar si se debe insertar una asada al inicio de la lista de asadas.
        Args:
            distrito (_type_): Distrito al que se le insertará la asada.
            id_asada (_type_): ID de la asada a insertar.

        Returns:
            bool: True si se debe insertar una asada al inicio, False en caso contrario.
        """
        return distrito.asadas is None or id_asada < distrito.asadas.id_asada
        
    def _buscar_nodo_anterior_asada(self, cabeza, id_asada):
        """
        Se encarga de buscar el nodo anterior a la asada que se debe insertar.
        Args:
            cabeza (_type_): Cabeza de la lista de asadas.
            id_asada (_type_): ID de la asada a insertar.

        Returns:
            _type_: Nodo anterior a la asada que se debe insertar.
        """
        actual = cabeza
        
        while (
            actual.siguiente is not None
            and actual.siguiente.id_asada < id_asada
        ):
            actual = actual.siguiente
            
        return actual
    
    def _insertar_asada_despues_de(self, nodo_anterior, nueva_asada):
        """
        Se encarga de insertar una asada despues de un nodo anterior.
        Args:
            nodo_anterior (_type_): Nodo anterior a la asada que se debe insertar.
            nueva_asada (_type_): Asada a insertar.
        """
        nueva_asada.siguiente = nodo_anterior.siguiente
        nodo_anterior.siguiente = nueva_asada
        
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
        """
        Se encarga de buscar un nodo por nombre dentro de una lista.

        Args:
            cabeza (_type_): Cabeza de la lista.
            nombre (_type_): Nombre del nodo a buscar.

        Returns:
            _type_: Nodo buscado.
        """
        nombre_normalizado = self._normalizar_nombre(nombre)
        
        for nodo in self._recorrer_lista(cabeza):
            if nodo.nombre == nombre_normalizado:
                return nodo
            
        return None
    
    def _obtener_nombres_desde_lista(self, cabeza):
        """
        Se encarga de obtener los nombres de una lista.

        Args:
            cabeza (_type_): Cabeza de la lista.

        Returns:
            _type_: Lista de nombres.
        """
        nombres = []
        
        for nodo in self._recorrer_lista(cabeza):
            nombres.append(nodo.nombre)
            
        return nombres
    
    def _obtener_referencias_asadas(self, cabeza):
        """
        Se encarga de obtener las referencias de las asadas.

        Args:
            cabeza (_type_): Cabeza de la lista.

        Returns:
            _type_: Lista de referencias.
        """
        referencias = []
        
        for nodo_asada in self._recorrer_lista(cabeza):
            referencia = self._crear_referencia_asada(nodo_asada)
            referencias.append(referencia)
            
        return referencias
    
    def _recorrer_lista(self, cabeza):
        """
        Se encarga de recorrer la lista de forma eficiente.

        Args:
            cabeza (_type_): Cabeza de la lista.

        Yields:
            _type_: Nodos de la lista.
        """
        actual = cabeza
        
        while actual is not None:
            yield actual
            actual = actual.siguiente
            
    def _normalizar_nombre(self, nombre):
        """
        Se encarga de normalizar el nombre.
        Args:
            nombre (_type_): Nombre a normalizar.

        Returns:
            _type_: Nombre normalizado.
        """
        if nombre is None:
            return ""
        
        return str(nombre).strip().upper()
