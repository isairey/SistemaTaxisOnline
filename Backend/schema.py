from pydantic import BaseModel
from datetime import date
from Backend.models import RolEnum

class UsuarioLogin(BaseModel):
    nombre_usuario: str
    password: str


class SocioSchema(BaseModel):
    documento: str
    nombres: str
    apellidos: str
    direccion: str
    numero_telefono: str
    numero_control: str
    rif: str
    fecha_nacimiento: date

# Para crear (sin id_socio)
class SocioCreate(SocioSchema):
    pass

class SocioResponse(SocioSchema):
    id_socio: int

    class Config:
        from_attributes = True

class SancionSchema(BaseModel):
    documento: str
    motivo_sancion: str
    monto: float
    inicio_sancion: date
    final_sancion: date
    nombre: str
    apellido: str

class SancionCreate(SancionSchema):
    pass

class SancionResponse(SancionSchema):
    id_sancion: int

    class Config:
        from_attributes = True



class AvanceSchema(BaseModel):
    numero_control: str
    nombre: str
    apellido: str
    fecha_nacimiento: date
    rif: str
    documento_avance: str
    numero_telf: str

class AvanceCreate(AvanceSchema):
    pass

class AvanceResponse(AvanceSchema):
    id_avance: int

    class Config:
        from_attributes = True

class VehiculoSchema(BaseModel):
    documento: str
    numero_control: int
    marca: str
    modelo: str
    ano: int
    placa: str

class VehiculoCreate(VehiculoSchema):
    pass


class VehiculoResponse(VehiculoSchema):
    id_vehiculo: int
    
    class Config:
        from_attributes = True

#Schema finanzas
class FinanzasSchema(BaseModel):
    documento: str
    pagos_mensuales: float
    impuestos_anuales: float
    fecha_pago: date
    numero_contr: str

class FinanzasCreate(FinanzasSchema):
    pass

class FinanzasResponse(FinanzasSchema):
    id_finanzas: int

    class Config:
        from_attributes = True

class UsuarioSchema(BaseModel):
    id_usuario: int
    nombre_usuario: str
    password: str
    rol: RolEnum
