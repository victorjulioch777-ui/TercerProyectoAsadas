class Asada:
    def __init__(
        self,
        id_Asada,
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
        self.id_asada = int(id_Asada)
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
        
    @staticmethod
    def from_dict(data):
        return Asada(
            id_Asada=data.get("id_Asada"),
            id_objeto=data.get("id_Objecto"),
            operador=data.get("operador"),
            telefono=data.get("telefono"),
            fax=data.get("fax"),
            correo=data.get("correo"),
            tipo_sistema=data.get("tipoSistema"),
            provincia=data.get("provincia"),
            canton=data.get("canton"),
            distrito=data.get("distrito"),
            codigo_dta=data.get("codigoDTA"),
            coordenadas_x=data.get("coordenadaX"),
            coordenadas_y=data.get("coordenadaY")
        )
    
    def to_dict(self):
        return {
            "id_asada": self.id_asada,
            "id_objeto": self.id_objeto,
            "operador": self.operador,
            "telefono": self.telefono,
            "fax": self.fax,
            "correo": self.correo,
            "tipo_sistema": self.tipo_sistema,
            "provincia": self.provincia,
            "canton": self.canton,
            "distrito": self.distrito,
            "codigo_dta": self.codigo_dta,
            "coordenadas_x": self.coordenadas_x,
            "coordenadas_y": self.coordenadas_y
        }

    def to_dic(self):
        return self.to_dict()
    
    def __str__(self):
        return(
            f"ID Asada: {self.id_asada}\n"
            f"Operador: {self.operador}\n"
            f"Provincia: {self.provincia}\n"
            f"Cantón: {self.canton}\n"
            f"Distrito: {self.distrito}\n"
            f"Teléfono: {self.telefono}\n"
            f"Correo: {self.correo}\n"
            f"Tipo de sistema: {self.tipo_sistema}"
        )
