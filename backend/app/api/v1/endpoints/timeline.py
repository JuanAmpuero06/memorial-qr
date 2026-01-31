"""
Endpoints de Línea de Tiempo
"""
from typing import List
from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import User
from app.schemas import (
    TimelineEventCreate, TimelineEventUpdate, 
    TimelineEventResponse, TimelineResponse, EVENT_TYPES
)
from app.services import TimelineService
from app.api.deps import get_current_user


router = APIRouter()


# ============ ENDPOINTS PÚBLICOS ============

@router.get("/public/{slug}", response_model=TimelineResponse)
async def get_public_timeline(
    slug: str,
    db: Session = Depends(get_db)
):
    """
    Obtener línea de tiempo de un memorial (público)
    
    Args:
        slug: Slug del memorial
        
    Returns:
        Línea de tiempo con eventos
    """
    return TimelineService.get_timeline(db, slug)


@router.get("/event-types")
async def get_event_types():
    """
    Obtener tipos de eventos disponibles con iconos
    
    Returns:
        Diccionario de tipos de eventos
    """
    return EVENT_TYPES


# ============ ENDPOINTS AUTENTICADOS ============

@router.post("/{memorial_id}", response_model=TimelineEventResponse, status_code=201)
async def create_event(
    memorial_id: int,
    event: TimelineEventCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Crear nuevo evento en línea de tiempo
    
    Args:
        memorial_id: ID del memorial
        event: Datos del evento
        
    Returns:
        Evento creado
    """
    return TimelineService.create_event(db, memorial_id, current_user.id, event)


@router.put("/{event_id}", response_model=TimelineEventResponse)
async def update_event(
    event_id: int,
    update_data: TimelineEventUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Actualizar evento de línea de tiempo
    
    Args:
        event_id: ID del evento
        update_data: Datos de actualización
        
    Returns:
        Evento actualizado
    """
    return TimelineService.update_event(db, event_id, current_user.id, update_data)


@router.delete("/{event_id}")
async def delete_event(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Eliminar evento de línea de tiempo
    
    Args:
        event_id: ID del evento
        
    Returns:
        Confirmación de eliminación
    """
    TimelineService.delete_event(db, event_id, current_user.id)
    return {"message": "Evento eliminado"}


@router.post("/{event_id}/image", response_model=TimelineEventResponse)
async def upload_event_image(
    event_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Subir imagen a un evento de timeline
    
    Args:
        event_id: ID del evento
        file: Imagen a subir
        
    Returns:
        Evento actualizado
    """
    return await TimelineService.upload_event_image(
        db, event_id, file, current_user.id
    )
