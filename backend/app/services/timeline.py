"""
Servicio de Línea de Tiempo
"""
import os
import uuid
from typing import List
from sqlalchemy.orm import Session
from fastapi import HTTPException, UploadFile, status
from app.models import TimelineEvent
from app.repositories import TimelineRepository, MemorialRepository
from app.schemas import TimelineEventCreate, TimelineEventUpdate, TimelineResponse, TimelineEventResponse
from app.config import settings


class TimelineService:
    """Servicio de gestión de línea de tiempo"""
    
    @staticmethod
    def create_event(
        db: Session, 
        memorial_id: int, 
        user_id: int,
        event: TimelineEventCreate
    ) -> TimelineEvent:
        """
        Crear nuevo evento en línea de tiempo
        
        Args:
            db: Sesión de base de datos
            memorial_id: ID del memorial
            user_id: ID del usuario
            event: Datos del evento
            
        Returns:
            Evento creado
        """
        memorial = MemorialRepository.get_by_id(db, memorial_id)
        if not memorial:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Memorial no encontrado"
            )
        
        if memorial.owner_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permiso para modificar este memorial"
            )
        
        return TimelineRepository.create(db, memorial_id, event)
    
    @staticmethod
    def get_timeline(db: Session, slug: str) -> TimelineResponse:
        """
        Obtener línea de tiempo de un memorial
        
        Args:
            db: Sesión de base de datos
            slug: Slug del memorial
            
        Returns:
            Línea de tiempo con eventos
        """
        memorial = MemorialRepository.get_by_slug(db, slug)
        if not memorial:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Memorial no encontrado"
            )
        
        events = TimelineRepository.get_by_memorial(db, memorial.id)
        
        return TimelineResponse(
            memorial_id=memorial.id,
            events=[TimelineEventResponse.model_validate(e) for e in events]
        )
    
    @staticmethod
    def update_event(
        db: Session, 
        event_id: int, 
        user_id: int,
        update_data: TimelineEventUpdate
    ) -> TimelineEvent:
        """
        Actualizar evento de línea de tiempo
        
        Args:
            db: Sesión de base de datos
            event_id: ID del evento
            user_id: ID del usuario
            update_data: Datos de actualización
            
        Returns:
            Evento actualizado
        """
        event = TimelineRepository.get_by_id(db, event_id)
        if not event:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Evento no encontrado"
            )
        
        if event.memorial.owner_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permiso para modificar este evento"
            )
        
        return TimelineRepository.update(db, event_id, update_data)
    
    @staticmethod
    def delete_event(db: Session, event_id: int, user_id: int) -> bool:
        """
        Eliminar evento de línea de tiempo
        
        Args:
            db: Sesión de base de datos
            event_id: ID del evento
            user_id: ID del usuario
            
        Returns:
            True si se eliminó correctamente
        """
        event = TimelineRepository.get_by_id(db, event_id)
        if not event:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Evento no encontrado"
            )
        
        if event.memorial.owner_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permiso para eliminar este evento"
            )
        
        return TimelineRepository.delete(db, event_id)
    
    @staticmethod
    async def upload_event_image(
        db: Session,
        event_id: int,
        file: UploadFile,
        user_id: int
    ) -> TimelineEvent:
        """
        Subir imagen a un evento de timeline
        
        Args:
            db: Sesión de base de datos
            event_id: ID del evento
            file: Archivo subido
            user_id: ID del usuario
            
        Returns:
            Evento actualizado
        """
        event = TimelineRepository.get_by_id(db, event_id)
        if not event:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Evento no encontrado"
            )
        
        if event.memorial.owner_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permiso para modificar este evento"
            )
        
        # Validar tipo de archivo
        allowed_types = ["image/jpeg", "image/png", "image/webp", "image/gif"]
        if file.content_type not in allowed_types:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Tipo de archivo no permitido"
            )
        
        # Generar nombre único
        ext = file.filename.split(".")[-1] if "." in file.filename else "jpg"
        filename = f"timeline_{event_id}_{uuid.uuid4().hex[:8]}.{ext}"
        file_path = os.path.join(settings.UPLOAD_DIR, filename)
        
        # Guardar archivo
        os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # Actualizar evento
        return TimelineRepository.update_image(db, event_id, filename)
