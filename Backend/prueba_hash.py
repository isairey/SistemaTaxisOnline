from passlib.context import CryptContext

# Creamos el contexto de cifrado (bcrypt es el algoritmo usado)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# La contraseña original
password_original = "admin123"

# Generamos el hash
hash_generado = pwd_context.hash(password_original)

# Mostramos los resultados
print("Contraseña original:", password_original)
print("Hash generado:", hash_generado)

# Verificamos si la contraseña coincide con el hash
es_valido = pwd_context.verify(password_original, hash_generado)
print("¿La contraseña es válida?:", es_valido)