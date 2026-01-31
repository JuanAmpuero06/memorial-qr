"""
Modelo de Línea de Tiempo - Eventos importantes de la vida
"""
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db import Base


class TimelineEvent(Base):
    """Modelo de evento en línea de tiempo"""
    
    __tablename__ = "timeline_events"

    id = Column(Integer, primary_key=True, index=True)
    memorial_id = Column(Integer, ForeignKey("memorials.id", ondelete="CASCADE"), index=True)
    
    # Información del evento
    title = Column(String(200), nullable=False)  # "Graduación universitaria"
    description = Column(Text, nullable=True)  # Descripción detallada
    event_date = Column(String, nullable=False)  # Fecha del evento (YYYY-MM-DD o YYYY)
    
    # Categoría del evento
    event_type = Column(String(50), default="general")  # birth, education, career, family, achievement, other
    
    # Multimedia opcional
    image_filename = Column(String, nullable=True)  # Foto del evento
    
    # Iconos/emoji para visualización
    icon = Column(String(10), nullable=True)  # 🎓, 💒, 🏆, etc.
    
    # Orden de visualización
    display_order = Column(Integer, default=0)
    
    # Metadatos
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relaciones
    memorial = relationship("Memorial", back_populates="timeline_events")
