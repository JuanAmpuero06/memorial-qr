from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True) # Identificador único del usuario
    email = Column(String, unique=True, index=True, nullable=False) # Correo electrónico del usuario
    hashed_password = Column(String, nullable=False) # Contraseña hasheada del usuario
    is_active = Column(Boolean, default=True) # Estado activo del usuario
    created_at = Column(DateTime(timezone=True), server_default=func.now()) # Fecha de creación del usuario

    # Relación: Un usuario tiene muchos memoriales
    memorials = relationship("Memorial", back_populates="owner")

class Memorial(Base):
    __tablename__ = "memorials"

    id = Column(Integer, primary_key=True, index=True) # Identificador único del memorial
    slug = Column(String, unique=True, index=True) # Slug único para URL amigable
    name = Column(String, index=True) # Nombre del difunto
    epitaph = Column(String, nullable=True) # Epitafio del memorial
    bio = Column(String, nullable=True) # Biografía del difunto
    image_filename = Column(String, nullable=True) # Nombre del archivo de la imagen asociada
    
    # Relación: Muchos memoriales pertenecen a un usuario
    owner_id = Column(Integer, ForeignKey("users.id")) 
    owner = relationship("User", back_populates="memorials") 
    created_at = Column(DateTime(timezone=True), server_default=func.now()) 