"""
Schemas de Galería Multimedia
"""
from pydantic import BaseModel, Field, field_serializer
from datetime import datetime
from typing import Optional, List
from app.config import settings


class MediaItemBase(BaseModel):
    """Schema base de elemento multimedia"""
    title: Optional[str] = Field(None, max_length=200)
    caption: Optional[str] = Field(None, max_length=1000)
    alt_text: Optional[str] = Field(None, max_length=500)
    taken_at: Optional[str] = None
    location: Optional[str] = Field(None, max_length=200)


class MediaItemCreate(MediaItemBase):
    """Schema para crear elemento multimedia (metadata)"""
    display_order: Optional[int] = 0
    is_featured: Optional[bool] = False


class MediaItemUpdate(BaseModel):
    """Schema para actualizar elemento multimedia"""
    title: Optional[str] = None
    caption: Optional[str] = None
    alt_text: Optional[str] = None
    taken_at: Optional[str] = None
    location: Optional[str] = None
    display_order: Optional[int] = None
    is_featured: Optional[bool] = None
    is_cover: Optional[bool] = None


class MediaItemResponse(MediaItemBase):
    """Schema de respuesta de elemento multimedia"""
    id: int
    memorial_id: int
    filename: str
    original_filename: Optional[str] = None
    media_type: str
    mime_type: Optional[str] = None
    file_size: Optional[int] = None
    width: Optional[int] = None
    height: Optional[int] = None
    display_order: int
    is_featured: bool
    is_cover: bool
    created_at: datetime
    
    @field_serializer('filename')
    def serialize_file_url(self, filename: str, _info):
        """Convierte el nombre del archivo en URL completa"""
        if filename:
            return f"{settings.BACKEND_URL}/static/{filename}"
        return None
    
    class Config:
        from_attributes = True


class GalleryResponse(BaseModel):
    """Respuesta de galería completa"""
    memorial_id: int
    items: List[MediaItemResponse]
    total: int


class MediaUploadResponse(BaseModel):
    """Respuesta al subir archivo"""
    message: str
    item: MediaItemResponse
