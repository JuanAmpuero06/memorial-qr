"""
Modelo de Condolencias - Libro de visitas digital
"""
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db import Base


class Condolence(Base):
    """Modelo de condolencia/mensaje en libro de visitas"""
    
    __tablename__ = "condolences"

    id = Column(Integer, primary_key=True, index=True)
    memorial_id = Column(Integer, ForeignKey("memorials.id", ondelete="CASCADE"), index=True)
    
    # Información del autor
    author_name = Column(String(100), nullable=False)
    author_email = Column(String(255), nullable=True)  # Opcional, para notificaciones
    author_relationship = Column(String(100), nullable=True)  # "Amigo", "Familiar", "Colega", etc.
    
    # Contenido del mensaje
    message = Column(Text, nullable=False)
    
    # Moderación
    is_approved = Column(Boolean, default=False)  # Requiere aprobación del propietario
    is_featured = Column(Boolean, default=False)  # Destacado por el propietario
    
    # Metadatos
    visitor_id = Column(String, nullable=True)  # UUID del visitante
    ip_address = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    approved_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relaciones
    memorial = relationship("Memorial", back_populates="condolences")
