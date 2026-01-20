from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relación: Un usuario tiene muchos memoriales
    memorials = relationship("Memorial", back_populates="owner")

class Memorial(Base):
    __tablename__ = "memorials"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    
    name = Column(String, index=True)
    slug = Column(String, unique=True, index=True) # Para la URL: /view/juan-perez
    epitaph = Column(String, nullable=True) # "Amado padre..."
    bio = Column(Text, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relación inversa
    owner = relationship("User", back_populates="memorials")