from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from Backend.database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import select
from Backend.models import Usuario
from passlib.context import CryptContext
from datetime import timezone

# -------------------- CONFIGURACIÓN --------------------
SECRET_KEY = "12345678"  # Cambia esto por una clave segura en producción
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Inicializamos bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 para FastAPI
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# -------------------- FUNCIONES --------------------

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Crea un JWT con los datos del usuario y tiempo de expiración.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_password(plain_password, hashed_password):
    """Verifica que la contraseña ingresada coincida con el hash."""
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(username: str, password: str, db: Session):
    """Verifica usuario y contraseña, devuelve el usuario si es correcto."""
    result = db.execute(select(Usuario).where(Usuario.nombre_usuario == username))
    user = result.scalars().first()
    
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Obtiene el usuario actual desde el token JWT.
    Levanta HTTPException si el token no es válido o usuario no existe.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # Obtenemos el usuario de la DB
    result = db.execute(select(Usuario).where(Usuario.nombre_usuario == username))
    user = result.scalars().first()
    if user is None:
        raise credentials_exception
    return user

def get_current_active_user(current_user: Usuario = Depends(get_current_user)):
    """Opcional: si quieres manejar usuarios activos/inactivos"""
    return current_user


def decode_access_token(token: str):
    """
    Decodifica un token JWT y devuelve su contenido (payload).
    Lanza una excepción si el token es inválido o ha expirado.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        ) from e