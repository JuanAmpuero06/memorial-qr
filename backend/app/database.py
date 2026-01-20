from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Construimos la URL de conexión usando las variables de entorno
# NOTA: El host es 'db' (el nombre del servicio en docker-compose), no 'localhost'
SQLALCHEMY_DATABASE_URL = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@db/{os.getenv('POSTGRES_DB')}"

# Creamos el motor de base de datos
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Creamos una clase "SessionLocal". Cada petición al servidor creará una instancia de esta sesión.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Esta clase "Base" será la madre de todos nuestros modelos (tablas)
Base = declarative_base()

# Dependencia para obtener la DB en cada endpoint
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()