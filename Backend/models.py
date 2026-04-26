from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL, Date, Enum
from sqlalchemy.ext.declarative import declarative_base
import enum
from sqlalchemy.orm import relationship

Base = declarative_base()

# Definir el tipo ENUM en Python
class RolEnum(str, enum.Enum):
    admin = "admin"
    user = "user"
    guest = "guest"

# Modelo para Socios
class Socio(Base):
    __tablename__ = "socio"
    __table_args__ = {"schema": "sanagaton"}

    id_socio = Column(Integer, primary_key=True)
    documento = Column(String(20), unique=True, nullable=False)
    nombres = Column(String(100))
    apellidos = Column(String(100))
    direccion = Column(String(200))
    numero_telefono = Column(String(20))
    numero_control = Column(String(50))
    rif = Column(String(20), unique=True)
    fecha_nacimiento = Column(Date)

    sanciones = relationship("Sancion", back_populates="socio")

# Modelo para Sanciones
class Sancion(Base):
    __tablename__ = "sanciones"
    __table_args__ = {"schema": "sanagaton"}

    id_sancion = Column(Integer, primary_key=True)
    documento = Column(String(15), ForeignKey("sanagaton.socio.documento"), nullable=False)
    motivo_sancion = Column(String(255))
    monto = Column(DECIMAL(10,2))
    inicio_sancion = Column(Date)
    final_sancion = Column(Date)
    nombre = Column(String(100))
    apellido = Column(String(100))

   # 🔗 Relación con el socio
    socio = relationship("Socio", back_populates="sanciones")

# Modelo para Avances
class Avance(Base):
    __tablename__ = "avances"
    __table_args__ = {"schema": "sanagaton"}

    id_avance = Column(Integer, primary_key=True)
    numero_control = Column(String(50))
    nombre = Column(String(100))
    apellido = Column(String(100))
    fecha_nacimiento = Column(Date)
    documento_avance = Column(String(20), ForeignKey("sanagaton.socio.documento"), nullable=False)
    numero_telf = Column(String(20))
    rif= Column(String(20))

# Modelo para Vehículos
class Vehiculo(Base):
    __tablename__ = "vehiculos"
    __table_args__ = {"schema": "sanagaton"}

    id_vehiculo = Column(Integer, primary_key=True)
    documento = Column(String(20), ForeignKey("sanagaton.socio.documento"))
    numero_control = Column(Integer)
    marca = Column(String(20))
    modelo = Column(String(20))
    ano = Column(Integer)
    placa = Column(String(10))

# Modelo para Finanzas
class Finanzas(Base):
    __tablename__ = "finanzas"
    __table_args__ = {"schema": "sanagaton"}

    id_finanzas = Column(Integer, primary_key=True)
    documento = Column(String(20), ForeignKey("sanagaton.socio.documento"))
    pagos_mensuales = Column(DECIMAL(10,2))
    impuestos_anuales = Column(DECIMAL(10,2))
    fecha_pago = Column(Date)
    numero_contr = Column(String(3))

# Modelo para Usuarios
class Usuario(Base):
    __tablename__ = "usuarios"
    __table_args__ = {"schema": "sanagaton"}

    id_usuario = Column(Integer, primary_key=True)
    nombre_usuario = Column(String(50))
    password = Column(String(100))
    rol = Column(Enum("admin", "user", "guest", name="rol_enum", schema="sanagaton"), nullable=False)
 # Definir el tipo ENUM en la base de datos
