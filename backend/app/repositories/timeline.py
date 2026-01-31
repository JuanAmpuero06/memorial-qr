"""
Repositorio de Línea de Tiempo
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models import TimelineEvent
from app.schemas import TimelineEventCreate, TimelineEventUpdate


class TimelineRepository:
    """Repositorio para operaciones de base de datos de eventos de timeline"""
    
    @staticmethod
    def create(db: Session, memorial_id: int, event: TimelineEventCreate) -> TimelineEvent:
        """Crear nuevo evento de timeline"""
        db_event = TimelineEvent(
            memorial_id=memorial_id,
            title=event.title,
            description=event.description,
            event_date=event.event_date,
            event_type=event.event_type,
            icon=event.icon,
            display_order=event.display_order or 0
        )
        db.add(db_event)
        db.commit()
        db.refresh(db_event)
        return db_event
    
    @staticmethod
    def get_by_id(db: Session, event_id: int) -> Optional[TimelineEvent]:
        """Obtener evento por ID"""
        return db.query(TimelineEvent).filter(TimelineEvent.id == event_id).first()
    
    @staticmethod
    def get_by_memorial(db: Session, memorial_id: int) -> List[TimelineEvent]:
        """Obtener todos los eventos de un memorial"""
        return db.query(TimelineEvent).filter(
            TimelineEvent.memorial_id == memorial_id
        ).order_by(
            TimelineEvent.event_date.asc(),
            TimelineEvent.display_order.asc()
        ).all()
    
    @staticmethod
    def update(
        db: Session, 
        event_id: int, 
        update_data: TimelineEventUpdate
    ) -> Optional[TimelineEvent]:
        """Actualizar evento de timeline"""
        event = db.query(TimelineEvent).filter(TimelineEvent.id == event_id).first()
        if not event:
            return None
        
        update_dict = update_data.model_dump(exclude_unset=True)
        for key, value in update_dict.items():
            setattr(event, key, value)
        
        db.commit()
        db.refresh(event)
        return event
    
    @staticmethod
    def delete(db: Session, event_id: int) -> bool:
        """Eliminar evento de timeline"""
        event = db.query(TimelineEvent).filter(TimelineEvent.id == event_id).first()
        if not event:
            return False
        
        db.delete(event)
        db.commit()
        return True
    
    @staticmethod
    def update_image(db: Session, event_id: int, filename: str) -> Optional[TimelineEvent]:
        """Actualizar imagen de un evento"""
        event = db.query(TimelineEvent).filter(TimelineEvent.id == event_id).first()
        if not event:
            return None
        
        event.image_filename = filename
        db.commit()
        db.refresh(event)
        return event
    
    @staticmethod
    def reorder(db: Session, memorial_id: int, event_ids: List[int]) -> bool:
        """Reordenar eventos de timeline"""
        for order, event_id in enumerate(event_ids):
            event = db.query(TimelineEvent).filter(
                TimelineEvent.id == event_id,
                TimelineEvent.memorial_id == memorial_id
            ).first()
            if event:
                event.display_order = order
        
        db.commit()
        return True
