from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session  # CAMBIO: usamos Session normal
from Backend.models import Socio, Vehiculo, Finanzas, Avance, Sancion, Usuario, RolEnum
from Backend.schema import SocioSchema, SancionSchema, AvanceSchema, VehiculoSchema, FinanzasSchema, UsuarioSchema, UsuarioLogin
from sqlalchemy import select  # CAMBIO: import normal
from Backend.database import get_db
from datetime import datetime
from Backend.jwt import create_access_token, authenticate_user, ACCESS_TOKEN_EXPIRE_MINUTES
from Backend.jwt import get_current_user
from passlib.context import CryptContext
from sqlalchemy.orm import joinedload
from datetime import datetime, timedelta  # para expiración del token
from Backend.pdf import pdf_router
from fastapi.security import OAuth2PasswordBearer
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse




app = FastAPI(title = "API TAXI SAN AGATON", version = "1.0.0",
description = "API para la Línea de TAXI SAN AGATON")

app.include_router(pdf_router)


app.mount("/landing", StaticFiles(directory="./landing", html=True), name="landing")

# Redirigir la raíz del servidor a la landing
@app.get("/", include_in_schema=False)
def redirect_to_landing():
    return RedirectResponse(url="/landing/index.html")


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

# ------------------- Rutas Públicas -------------------

@app.get("/")
def bienvenida():
    return {"message": "Bienvenido a la API de la Línea de TAXI SAN AGATON"}

@app.get("/saludos")
def saludo():
    return "Hola, como están?"

# ------------------- LOGIN -------------------
# CAMBIO: async → def, quitamos await, usamos Session

@app.post("/login")
def login(usuario: UsuarioLogin, db: Session = Depends(get_db)):
    # Autenticamos el usuario usando la función JWT
    user = authenticate_user(usuario.nombre_usuario, usuario.password, db)
    if not user:
        raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")

    # Creamos token con expiración
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.nombre_usuario, "id": user.id_usuario, "rol": user.rol},
        expires_delta=access_token_expires
    )

    return {
        "message": "Login Exitoso",
        "access_token": access_token,
        "token_type": "bearer",
        "usuario": {
            "id_usuario": user.id_usuario,
            "nombre_usuario": user.nombre_usuario,
            "rol": user.rol if user.rol else None,
        }
    }
# ------------------- USUARIOS -------------------
@app.get("/usuarios")
def obtener_usuarios(db: Session = Depends(get_db)):
    result = db.execute(select(Usuario))
    return result.scalars().all()

@app.post("/usuarios/")
def crear_usuario(usuario: UsuarioSchema, db: Session = Depends(get_db)):
    nuevo_usuario = Usuario(**usuario.model_dump())
    db.add(nuevo_usuario)
    db.commit()
    return {"message": "Usuario creado exitosamente", "usuario": usuario}

@app.put("/usuarios/{id_usuario}")
def actualizar_usuario(id_usuario: int, usuario: UsuarioSchema, db: Session = Depends(get_db)):
    result = db.execute(select(Usuario).where(Usuario.id_usuario == id_usuario))
    usuario_db = result.scalars().first()

    if not usuario_db:
        raise HTTPException(status_code=404, detail=f"No se encontró un usuario con el ID {id_usuario}.")

    for key, value in usuario.model_dump().items():
        setattr(usuario_db, key, value)

    db.commit()
    return {"message": "Usuario actualizado exitosamente", "usuario": usuario_db}

@app.delete("/usuarios/{id_usuario}")
def eliminar_usuario(id_usuario: int, db: Session = Depends(get_db)):
    result = db.execute(select(Usuario).where(Usuario.id_usuario == id_usuario))
    usuario = result.scalars().first()
    if not usuario:
        raise HTTPException(status_code=404, detail=f"No se encontró un usuario con el ID {id_usuario}.")

    db.delete(usuario)
    db.commit()
    return {"message": "Usuario eliminado exitosamente"}

# ------------------- AVANCES -------------------
@app.get("/avances")
def obtener_avances(db: Session = Depends(get_db)):
    result = db.execute(select(Avance))
    return result.scalars().all()

@app.post("/avances/")
def crear_avance(avance: AvanceSchema, db: Session = Depends(get_db)):
    nuevo_avance = Avance(**avance.model_dump())
    db.add(nuevo_avance)
    db.commit()
    db.refresh(nuevo_avance)
    return nuevo_avance # Retornamos el objeto creado

@app.put("/avances/{id_avance}")
def actualizar_avance(id_avance: int, avance: AvanceSchema, db: Session = Depends(get_db)):
    result = db.execute(select(Avance).where(Avance.id_avance == id_avance))
    avance_db = result.scalars().first()

    if not avance_db:
        raise HTTPException(status_code=404, detail=f"No se encontró un avance con el ID {id_avance}.")

    for key, value in avance.model_dump().items():
        setattr(avance_db, key, value)

    db.commit()
    return {"message": "Avance actualizado exitosamente", "avance": avance_db}

@app.delete("/avances/{id_avance}")
def eliminar_avance(id_avance: int, db: Session = Depends(get_db)):
    result = db.execute(select(Avance).where(Avance.id_avance == id_avance))
    avance = result.scalars().first()

    if not avance:
        raise HTTPException(status_code=404, detail=f"No se encontró un avance con el ID {id_avance}.")

    db.delete(avance)
    db.commit()

# ------------------- SOCIOS -------------------
@app.get("/socios")
def obtener_socios(db: Session = Depends(get_db)):
    result = db.execute(select(Socio))
    return result.scalars().all()

@app.post("/socios/")
def crear_socio(socio: SocioSchema, db: Session = Depends(get_db)):
    nuevo_socio = Socio(**socio.model_dump())
    db.add(nuevo_socio)
    db.commit()
    db.refresh(nuevo_socio)
    return nuevo_socio # Retornamos el objeto creado      

@app.delete("/socios/{id_socio}")
def eliminar_socio(id_socio: int, db: Session = Depends(get_db)):
    result = db.execute(select(Socio).where(Socio.id_socio == id_socio))
    socio = result.scalars().first()

    if not socio:

        raise HTTPException(status_code=404, detail=f"No se encontró un socio con el ID {id_socio}.")

    db.delete(socio)
    db.commit()

@app.put("/socios/{id_socio}")
def actualizar_socio(id_socio: int, socio: SocioSchema, db: Session = Depends(get_db)):
    result = db.execute(select(Socio).where(Socio.id_socio == id_socio))
    socio_db = result.scalars().first()

    if not socio_db:
        raise HTTPException(status_code=404, detail=f"No se encontró un socio con el ID {id_socio}.")
    
    socio_data = socio.model_dump()
    if isinstance(socio_data.get('fecha_nacimiento'), str):
        socio_data['fecha_nacimiento'] = datetime.strptime(socio_data['fecha_nacimiento'], '%Y-%m-%d').date()


    for key, value in socio_data.items():
        setattr(socio_db, key, value)

    db.commit()
    return {"message": "Socio actualizado exitosamente", "socio": socio_db}

# ------------------- VEHICULOS -------------------
@app.post("/vehiculos/", response_model=VehiculoSchema)
def crear_vehiculo(vehiculo: VehiculoSchema, db: Session = Depends(get_db)):
    nuevo_vehiculo = Vehiculo(**vehiculo.model_dump())
    db.add(nuevo_vehiculo)
    db.commit()
    db.refresh(nuevo_vehiculo)
    return nuevo_vehiculo

@app.get("/vehiculos")
def obtener_vehiculos(db: Session = Depends(get_db)):
    result = db.execute(select(Vehiculo))
    return result.scalars().all()

@app.put("/vehiculos/{id_vehiculo}")
def actualizar_vehiculo(id_vehiculo: int, vehiculo: VehiculoSchema, db: Session = Depends(get_db)):
    result = db.execute(select(Vehiculo).where(Vehiculo.id_vehiculo == id_vehiculo))
    vehiculo_db = result.scalars().first()

    if not vehiculo_db:
        raise HTTPException(status_code=404, detail=f"No se encontró un vehiculo con el ID {id_vehiculo}.")
    
    vehiculo_data = vehiculo.model_dump()
    if isinstance(vehiculo_data.get('ano'), str):
        vehiculo_data['ano'] = int(vehiculo_data['ano'])

    for key, value in vehiculo_data.items():
        setattr(vehiculo_db, key, value)

    db.commit()
    db.refresh(vehiculo_db)  # para devolverlo actualizado

    return {"message": "Vehículo actualizado exitosamente", "vehículo": vehiculo_db}

@app.delete("/vehiculos/{id_vehiculo}")
def eliminar_vehiculo(id_vehiculo: int, db: Session = Depends(get_db)):
    result = db.execute(select(Vehiculo).where(Vehiculo.id_vehiculo == id_vehiculo))
    vehiculo = result.scalars().first()

    if not vehiculo:
        raise HTTPException(status_code=404, detail=f"No se encontró un vehículo con el ID {id_vehiculo}.")

    db.delete(vehiculo)
    db.commit()

# ------------------- SANCIONES -------------------
@app.get("/sanciones")
def obtener_sanciones(db: Session = Depends(get_db)):
    sanciones = db.execute(
        select(Sancion).options(joinedload(Sancion.socio))
    ).scalars().all()

    resultado = []
    for s in sanciones:
        resultado.append({
            "id_sancion": s.id_sancion,
            "inicio_sancion": s.inicio_sancion,
            "final_sancion": s.final_sancion,
            "motivo_sancion": s.motivo_sancion,
            "monto": s.monto,
            "documento": s.socio.documento if s.socio else s.documento,
            "nombre": s.socio.nombres if s.socio else s.nombre,
            "apellido": s.socio.apellidos if s.socio else s.apellido,
        })
    return resultado

@app.post("/sanciones/")
def crear_sancion(sancion: SancionSchema, db: Session = Depends(get_db)):
    nueva_sancion = Sancion(**sancion.model_dump())
    db.add(nueva_sancion)
    db.commit()
    db.refresh(nueva_sancion)
    return nueva_sancion # Retornamos el objeto creado

@app.put("/sanciones/{id_sancion}")
def actualizar_sancion(id_sancion: int, sancion: SancionSchema, db: Session = Depends(get_db)):
    result = db.execute(select(Sancion).where(Sancion.id_sancion == id_sancion))
    sancion_db = result.scalars().first()

    if not sancion_db:
        raise HTTPException(status_code=404, detail=f"No se encontró una sanción con el ID {id_sancion}.")

    for key, value in sancion.model_dump().items():
        setattr(sancion_db, key, value)

    db.commit()
    return {"message": "Sanción actualizada exitosamente", "sancion": sancion_db}

@app.delete("/sanciones/{id_sancion}")
def eliminar_sancion(id_sancion: int, db: Session = Depends(get_db)):
    result = db.execute(select(Sancion).where(Sancion.id_sancion == id_sancion))
    sancion = result.scalars().first()

    if not sancion:
        raise HTTPException(status_code=404, detail=f"No se encontró una sanción con el ID {id_sancion}.")

    db.delete(sancion)
    db.commit()

# ------------------- FINANZAS -------------------
@app.get("/finanzas")
def obtener_finanzas(db: Session = Depends(get_db)):
    result = db.execute(select(Finanzas))
    return result.scalars().all()

@app.post("/finanzas/")
def crear_finanza(finanza: FinanzasSchema, db: Session = Depends(get_db)):
    nueva_finanza = Finanzas(**finanza.model_dump())
    db.add(nueva_finanza)
    db.commit()
    db.refresh(nueva_finanza)
    return nueva_finanza # Retornamos el objeto creado

@app.put("/finanzas/{id_finanzas}")
def actualizar_finanza(id_finanzas: int, finanza: FinanzasSchema, db: Session = Depends(get_db)):
    result = db.execute(select(Finanzas).where(Finanzas.id_finanzas == id_finanzas))
    finanza_db = result.scalars().first()

    if not finanza_db:
        raise HTTPException(status_code=404, detail=f"No se encontró una finanza con el ID {id_finanzas}.")

    for key, value in finanza.model_dump().items():
        setattr(finanza_db, key, value)

    db.commit()
    return {"message": "Finanza actualizada exitosamente", "finanza": finanza_db}

@app.delete("/finanzas/{id_finanzas}")
def eliminar_finanza(id_finanzas: int, db: Session = Depends(get_db)):
    result = db.execute(select(Finanzas).where(Finanzas.id_finanzas == id_finanzas))
    finanza = result.scalars().first()

    if not finanza:
        raise HTTPException(status_code=404, detail=f"No se encontró una finanza con el ID {id_finanzas}.")

    db.delete(finanza)
    db.commit()