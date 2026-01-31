"""
Modelo de Visitas - Tracking de escaneos QR
"""
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db import Base


class Visit(Base):
    """Modelo de visita/escaneo de memorial"""
    
    __tablename__ = "visits"

    id = Column(Integer, primary_key=True, index=True)
    memorial_id = Column(Integer, ForeignKey("memorials.id", ondelete="CASCADE"), index=True)
    ip_address = Column(String, nullable=True)
    user_agent = Column(String, nullable=True)
    referrer = Column(String, nullable=True)
    country = Column(String, nullable=True)
    city = Column(String, nullable=True)
    visited_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relaciones
    memorial = relationship("Memorial", back_populates="visits")
