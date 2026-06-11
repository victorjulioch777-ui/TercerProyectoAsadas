import config

class Asada:
    """
    Clase que representa una ASADA.
    """
    def __init__(
        self,
        id_asada,
        id_objeto,
        operador,
        telefono,
        fax,
        correo,
        tipo_sistema,
        provincia,
        canton,
        distrito,
        codigo_dta,
        coordenadas_x,
        coordenadas_y
    ):
        self.id_asada = int(id_asada)
        self.id_Asada = self.id_asada
        self.id_objeto = int(id_objeto)
        self.operador = operador
        self.telefono = telefono
        self.fax = fax
        self.correo = correo
        self.tipo_sistema = tipo_sistema
        self.provincia = provincia
        self.canton = canton
        self.distrito = distrito
        self.codigo_dta = int(codigo_dta)
        self.coordenadas_x = float(str(coordenadas_x).strip())
        self.coordenadas_y = float(str(coordenadas_y).strip())
        
    @classmethod
    def from_dict(cls, data):
        """
        Convierte un diccionario en un objeto Asada.
        Args:
            data (_type_): Diccionario con la informacion de la ASADA
        Returns:
            _type_: Objeto Asada
        """
        claves = config.CLAVES_JSON_ASADA
        
        return cls(
            id_asada=data.get(claves["ID_ASADA"]),
            id_objeto=data.get(claves["ID_OBJETO"]),
            operador=data.get(claves["OPERADOR"]),
            telefono=data.get(claves["TELEFONO"]),
            fax=data.get(claves["FAX"]),
            correo=data.get(claves["CORREO"]),
            tipo_sistema=data.get(claves["TIPO_SISTEMA"]),
            provincia=data.get(claves["PROVINCIA"]),
            canton=data.get(claves["CANTON"]),
            distrito=data.get(claves["DISTRITO"]),
            codigo_dta=data.get(claves["CODIGO_DTA"]),
            coordenadas_x=data.get(claves["COORDENADA_X"]),
            coordenadas_y=data.get(claves["COORDENADA_Y"])
        )
    
    def to_dict(self):
        """
        Se encarga de convertir un objeto Asada en un diccionario.
        Returns:
            _type_: Diccionario con la informacion de la ASADA
        """
        claves = config.CLAVES_ASADA
    
        return {
            claves["ID_ASADA"]: self.id_asada,
            claves["ID_OBJETO"]: self.id_objeto,
            claves["OPERADOR"]: self.operador,
            claves["TELEFONO"]: self.telefono,
            claves["FAX"]: self.fax,
            claves["CORREO"]: self.correo,
            claves["TIPO_SISTEMA"]: self.tipo_sistema,
            claves["PROVINCIA"]: self.provincia,
            claves["CANTON"]: self.canton,
            claves["DISTRITO"]: self.distrito,
            claves["CODIGO_DTA"]: self.codigo_dta,
            claves["COORDENADA_X"]: self.coordenadas_x,
            claves["COORDENADA_Y"]: self.coordenadas_y
        }

    def to_dic(self):
        """
        Se encarga de llamar al metodo to_dict().
        Returns:
            _type_: Diccionario con la informacion de la ASADA
        """
        return self.to_dict()
    
    def __str__(self):
        """
        Se encarga de representar un objeto Asada en formato string.
        """
        return(
            f"{config.ETIQUETAS_ASADA[config.CAMPO_ID_ASADA]}: {self.id_asada}\n"
            f"{config.ETIQUETAS_ASADA[config.CAMPO_OPERADOR]}: {self.operador}\n"
            f"{config.ETIQUETAS_ASADA[config.CAMPO_PROVINCIA]}: {self.provincia}\n"
            f"{config.ETIQUETAS_ASADA[config.CAMPO_CANTON]}: {self.canton}\n"
            f"{config.ETIQUETAS_ASADA[config.CAMPO_DISTRITO]}: {self.distrito}\n"
            f"{config.ETIQUETAS_ASADA[config.CAMPO_TELEFONO]}: {self.telefono}\n"
            f"{config.ETIQUETAS_ASADA[config.CAMPO_CORREO]}: {self.correo}\n"
            f"{config.ETIQUETAS_ASADA[config.CAMPO_TIPO_DE_SISTEMA]}: {self.tipo_sistema}"
        )
