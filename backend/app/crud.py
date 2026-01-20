from sqlalchemy.orm import Session
from passlib.context import CryptContext
from . import models, schemas

# Configuración del Hashing (algoritmo bcrypt)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# --- FUNCIONES DE USUARIO ---

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    # 1. Encriptamos la contraseña
    hashed_password = get_password_hash(user.password)
    
    # 2. Creamos el objeto Usuario de SQLAlchemy
    db_user = models.User(
        email=user.email, 
        hashed_password=hashed_password
    )
    
    # 3. Guardamos en BD
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user