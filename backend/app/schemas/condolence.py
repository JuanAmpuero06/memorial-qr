"""
Schemas de Condolencias - Libro de visitas digital
"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List


class CondolenceBase(BaseModel):
    """Schema base de condolencia"""
    author_name: str = Field(..., min_length=2, max_length=100)
    author_relationship: Optional[str] = Field(None, max_length=100)
    message: str = Field(..., min_length=10, max_length=2000)


class CondolenceCreate(CondolenceBase):
    """Schema para crear condolencia"""
    author_email: Optional[str] = None
    visitor_id: Optional[str] = None


class CondolenceUpdate(BaseModel):
    """Schema para actualizar condolencia (moderación)"""
    is_approved: Optional[bool] = None
    is_featured: Optional[bool] = None


class CondolenceResponse(CondolenceBase):
    """Schema de respuesta de condolencia"""
    id: int
    memorial_id: int
    is_approved: bool
    is_featured: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class CondolencePublic(BaseModel):
    """Schema público de condolencia (para visitantes)"""
    id: int
    author_name: str
    author_relationship: Optional[str] = None
    message: str
    is_featured: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class CondolenceListResponse(BaseModel):
    """Lista paginada de condolencias"""
    items: List[CondolencePublic]
    total: int
    pending_count: int = 0  # Solo para propietarios
