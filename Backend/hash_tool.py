import argparse
from database import SessionLocal
from models import Usuario
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_passwords():
    db = SessionLocal()
    usuarios = db.query(Usuario).all()
    for usuario in usuarios:
        current = usuario.password or ""
        # Usar identify evita doble-hasheo y detecta varios esquemas
        if pwd_context.identify(current):
            print(f"Ya hasheado: {usuario.nombre_usuario}")
            continue
        print(f"Hasheando: {usuario.nombre_usuario}")
        usuario.password = pwd_context.hash(current)
    db.commit()
    db.close()
    print("\nTodas las contraseñas han sido procesadas correctamente.")


def verify_password(nombre_usuario: str, plain_password: str):
    db = SessionLocal()
    try:
        usuario = db.query(Usuario).filter(Usuario.nombre_usuario == nombre_usuario).first()
        if not usuario:
            print(f"Usuario '{nombre_usuario}' no encontrado.")
            return

        stored = usuario.password or ""

        # Si el valor guardado no parece un hash, informamos (posible DB en texto plano)
        scheme = pwd_context.identify(stored)
        if not scheme:
            print(f"Advertencia: la contraseña almacenada para '{nombre_usuario}' no parece un hash reconocido ({stored[:30]}...).")
            # Puedes decidir verificar igualdad directa (poco seguro) o devolver error:
            # comparacion_directa = (stored == plain_password)
            # print("Comparación directa:", "Correcta" if comparacion_directa else "Incorrecta")
            return

        # Intentar verificar con passlib; manejar excepciones por seguridad
        try:
            result = pwd_context.verify(plain_password, stored)
        except Exception as e:
            print(f"Error verificando hash: {e}")
            result = False

        print(f"\nUsuario: {nombre_usuario}")
        print(f"Contraseña ingresada: {plain_password}")
        print(f"Resultado de verificación: {'Correcta' if result else 'Incorrecta'}")
    finally:
        db.close()


def list_users():
    db = SessionLocal()
    usuarios = db.query(Usuario).all()
    print("\nUsuarios en el sistema:")
    for usuario in usuarios:
        estado = "Hasheado" if pwd_context.identify(usuario.password or "") else "Sin hashear"
        print(f" - {usuario.nombre_usuario}: {estado}")
    db.close()


def main():
    parser = argparse.ArgumentParser(description="Herramienta de gestión de contraseñas (hash y verificación).")
    parser.add_argument("--hash", action="store_true", help="Hashea todas las contraseñas sin hashear.")
    # Usar metavar sin caracteres especiales para evitar problemas en algunas consolas
    parser.add_argument("--verify", help="Verifica una contraseña | uso: --verify NOMBRE CONTRASEÑA", nargs=2, metavar=("NOMBRE", "CONTRASEÑA"))
    parser.add_argument("--list", action="store_true", help="Lista los usuarios y su estado de hash.")
    args = parser.parse_args()

    if args.hash:
        hash_passwords()
    elif args.verify:
        nombre, password = args.verify
        verify_password(nombre, password)
    elif args.list:
        list_users()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()