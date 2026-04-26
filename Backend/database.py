from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

# CAMBIO: Driver async → Driver sync (psycopg2)
DATABASE_URL = "postgresql+psycopg2://postgres:root@localhost:5432/taxi"

# CAMBIO: create_async_engine → create_engine
engine = create_engine(DATABASE_URL, echo=True)

# CAMBIO: class_=AsyncSession ya no es necesario
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)

# Dependencia para obtener la sesión
# CAMBIO: async def → def y quitamos "async with"
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()