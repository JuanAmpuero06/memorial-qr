"""
Schemas de Línea de Tiempo
"""
from pydantic import BaseModel, Field, field_serializer
from datetime import datetime
from typing import Optional, List
from app.config import settings


class TimelineEventBase(BaseModel):
    """Schema base de evento de línea de tiempo"""
    title: str = Field(..., min_length=2, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    event_date: str = Field(..., description="Fecha del evento (YYYY-MM-DD o YYYY)")
    event_type: str = Field(default="general")
    icon: Optional[str] = Field(None, max_length=10)


class TimelineEventCreate(TimelineEventBase):
    """Schema para crear evento"""
    display_order: Optional[int] = 0


class TimelineEventUpdate(BaseModel):
    """Schema para actualizar evento"""
    title: Optional[str] = None
    description: Optional[str] = None
    event_date: Optional[str] = None
    event_type: Optional[str] = None
    icon: Optional[str] = None
    display_order: Optional[int] = None


class TimelineEventResponse(TimelineEventBase):
    """Schema de respuesta de evento"""
    id: int
    memorial_id: int
    display_order: int
    image_filename: Optional[str] = None
    created_at: datetime
    
    @field_serializer('image_filename')
    def serialize_image_url(self, filename: Optional[str], _info):
        """Convierte el nombre del archivo en URL completa"""
        if filename:
            return f"{settings.BACKEND_URL}/static/{filename}"
        return None
    
    class Config:
        from_attributes = True


class TimelineResponse(BaseModel):
    """Lista de eventos de línea de tiempo"""
    memorial_id: int
    events: List[TimelineEventResponse]


# Tipos de eventos predefinidos
EVENT_TYPES = {
    "birth": {"icon": "👶", "label": "Nacimiento"},
    "education": {"icon": "🎓", "label": "Educación"},
    "career": {"icon": "💼", "label": "Carrera"},
    "family": {"icon": "💒", "label": "Familia"},
    "achievement": {"icon": "🏆", "label": "Logro"},
    "travel": {"icon": "✈️", "label": "Viaje"},
    "hobby": {"icon": "🎨", "label": "Hobby"},
    "general": {"icon": "📌", "label": "General"},
    "other": {"icon": "✨", "label": "Otro"},
}
