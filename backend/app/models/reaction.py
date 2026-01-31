"""
Modelo de Reacciones - Interacciones de usuarios con memoriales
"""
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db import Base


class Reaction(Base):
    """Modelo de reacción a un memorial"""
    
    __tablename__ = "reactions"

    id = Column(Integer, primary_key=True, index=True)
    memorial_id = Column(Integer, ForeignKey("memorials.id", ondelete="CASCADE"), index=True)
    reaction_type = Column(String, index=True)  # 'candle', 'flower', 'heart', 'pray', 'dove'
    visitor_id = Column(String, index=True)  # UUID generado en el cliente para identificar visitantes únicos
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relaciones
    memorial = relationship("Memorial", back_populates="reactions")
    
    # Constraint único para evitar múltiples reacciones del mismo tipo por visitante
    __table_args__ = (
        UniqueConstraint('memorial_id', 'reaction_type', 'visitor_id', name='unique_reaction_per_visitor'),
    )
