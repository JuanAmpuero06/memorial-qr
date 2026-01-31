"""
Schemas de Memorial
"""
from pydantic import BaseModel, field_serializer
from datetime import datetime
from typing import Optional
from app.config import settings


class MemorialBase(BaseModel):
    """Schema base de memorial"""
    name: str
    epitaph: Optional[str] = None


class MemorialCreate(MemorialBase):
    """Schema para crear memorial"""
    bio: Optional[str] = None
    birth_date: Optional[str] = None
    death_date: Optional[str] = None


class MemorialUpdate(BaseModel):
    """Schema para actualizar memorial"""
    name: Optional[str] = None
    epitaph: Optional[str] = None
    bio: Optional[str] = None
    birth_date: Optional[str] = None
    death_date: Optional[str] = None


class MemorialResponse(MemorialCreate):
    """Schema de respuesta de memorial"""
    id: int
    slug: str
    owner_id: int
    created_at: datetime
    image_filename: Optional[str] = None
    
    @field_serializer('image_filename')
    def serialize_image_url(self, filename: Optional[str], _info):
        """Convierte el nombre del archivo en URL completa"""
        if filename:
            return f"{settings.BACKEND_URL}/static/{filename}"
        return None
    
    class Config:
        from_attributes = True


class PublicMemorial(BaseModel):
    """Schema para memorial público (sin datos sensibles)"""
    name: str
    epitaph: Optional[str] = None
    bio: Optional[str] = None
    image_filename: Optional[str] = None
    
    @field_serializer('image_filename')
    def serialize_image_url(self, filename: Optional[str], _info):
        """Convierte el nombre del archivo en URL completa"""
        if filename:
            return f"{settings.BACKEND_URL}/static/{filename}"
        return None
    
    class Config:
        from_attributes = True
