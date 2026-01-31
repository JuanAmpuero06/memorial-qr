"""
Modelo de Memorial
"""
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db import Base


class Memorial(Base):
    """Modelo de memorial"""
    
    __tablename__ = "memorials"

    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String, unique=True, index=True)
    name = Column(String, index=True)
    epitaph = Column(String, nullable=True)
    bio = Column(String, nullable=True)
    birth_date = Column(String, nullable=True)
    death_date = Column(String, nullable=True)
    image_filename = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relaciones
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    owner = relationship("User", back_populates="memorials")
    visits = relationship("Visit", back_populates="memorial", cascade="all, delete-orphan")
    reactions = relationship("Reaction", back_populates="memorial", cascade="all, delete-orphan")
    condolences = relationship("Condolence", back_populates="memorial", cascade="all, delete-orphan")
    timeline_events = relationship("TimelineEvent", back_populates="memorial", cascade="all, delete-orphan")
    media_items = relationship("MediaItem", back_populates="memorial", cascade="all, delete-orphan")
