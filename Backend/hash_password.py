from database import SessionLocal
from models import Usuario
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

db = SessionLocal()
usuarios = db.query(Usuario).all()

for usuario in usuarios:
    password_actual = usuario.password or ""

    # Verifica si el valor ya es un hash conocido
    if pwd_context.identify(password_actual):
        print(f"Saltando (ya hasheado): {usuario.nombre_usuario}")
        continue

    print(f"Hasheando contraseña de: {usuario.nombre_usuario}")
    usuario.password = pwd_context.hash(password_actual)

db.commit()
db.close()

print("Todas las contraseñas han sido procesadas correctamente.")