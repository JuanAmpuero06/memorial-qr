from sqlalchemy.orm import Session
from passlib.context import CryptContext
from . import models, schemas
from slugify import slugify # <--- NUEVO
import uuid # <--- NUEVO

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

def create_memorial(db: Session, memorial: schemas.MemorialCreate, user_id: int):
    # 1. Generar un slug único
    # Ejemplo: "Juan Perez" -> "juan-perez-a1b2" (para evitar duplicados)
    base_slug = slugify(memorial.name)
    unique_suffix = str(uuid.uuid4())[:8] # Tomamos 8 caracteres aleatorios
    final_slug = f"{base_slug}-{unique_suffix}"
    
    # 2. Crear el objeto DB
    db_memorial = models.Memorial(
        name=memorial.name,
        epitaph=memorial.epitaph,
        bio=memorial.bio,
        slug=final_slug,
        owner_id=user_id # ¡Aquí vinculamos al difunto con el usuario logueado!
    )
    
    # 3. Guardar
    db.add(db_memorial)
    db.commit()
    db.refresh(db_memorial)
    
    return db_memorial

def get_memorials_by_user(db: Session, user_id: int):
    return db.query(models.Memorial).filter(models.Memorial.owner_id == user_id).all()

def get_memorial_by_slug(db: Session, slug: str):
    # Buscamos el primero que coincida con el slug
    return db.query(models.Memorial).filter(models.Memorial.slug == slug).first()