"""
Modelo de Media - Galería multimedia del memorial
"""
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db import Base


class MediaItem(Base):
    """Modelo de elemento multimedia (foto/video) de galería"""
    
    __tablename__ = "media_items"

    id = Column(Integer, primary_key=True, index=True)
    memorial_id = Column(Integer, ForeignKey("memorials.id", ondelete="CASCADE"), index=True)
    
    # Información del archivo
    filename = Column(String, nullable=False)
    original_filename = Column(String, nullable=True)  # Nombre original subido
    media_type = Column(String(20), default="image")  # image, video
    mime_type = Column(String(100), nullable=True)  # image/jpeg, video/mp4
    file_size = Column(Integer, nullable=True)  # Tamaño en bytes
    
    # Metadatos de la imagen/video
    width = Column(Integer, nullable=True)
    height = Column(Integer, nullable=True)
    duration = Column(Integer, nullable=True)  # Duración en segundos (para videos)
    
    # Información descriptiva
    title = Column(String(200), nullable=True)
    caption = Column(Text, nullable=True)  # Descripción de la foto
    alt_text = Column(String(500), nullable=True)  # Texto alternativo accesibilidad
    
    # Fecha de la foto (no de subida)
    taken_at = Column(String, nullable=True)  # Fecha en que se tomó la foto
    location = Column(String(200), nullable=True)  # Lugar donde se tomó
    
    # Orden y destacados
    display_order = Column(Integer, default=0)
    is_featured = Column(Boolean, default=False)  # Foto destacada en galería
    is_cover = Column(Boolean, default=False)  # Foto de portada alternativa
    
    # Metadatos
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relaciones
    memorial = relationship("Memorial", back_populates="media_items")
