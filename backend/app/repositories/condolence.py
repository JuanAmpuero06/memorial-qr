"""
Repositorio de Condolencias
"""
from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models import Condolence
from app.schemas import CondolenceCreate, CondolenceUpdate


class CondolenceRepository:
    """Repositorio para operaciones de base de datos de condolencias"""
    
    @staticmethod
    def create(
        db: Session, 
        memorial_id: int, 
        condolence: CondolenceCreate,
        ip_address: Optional[str] = None
    ) -> Condolence:
        """Crear nueva condolencia"""
        db_condolence = Condolence(
            memorial_id=memorial_id,
            author_name=condolence.author_name,
            author_email=condolence.author_email,
            author_relationship=condolence.author_relationship,
            message=condolence.message,
            visitor_id=condolence.visitor_id,
            ip_address=ip_address,
            is_approved=False,  # Requiere aprobación
            is_featured=False
        )
        db.add(db_condolence)
        db.commit()
        db.refresh(db_condolence)
        return db_condolence
    
    @staticmethod
    def get_by_id(db: Session, condolence_id: int) -> Optional[Condolence]:
        """Obtener condolencia por ID"""
        return db.query(Condolence).filter(Condolence.id == condolence_id).first()
    
    @staticmethod
    def get_by_memorial(
        db: Session, 
        memorial_id: int, 
        approved_only: bool = True,
        limit: int = 50,
        offset: int = 0
    ) -> Tuple[List[Condolence], int]:
        """Obtener condolencias de un memorial"""
        query = db.query(Condolence).filter(Condolence.memorial_id == memorial_id)
        
        if approved_only:
            query = query.filter(Condolence.is_approved == True)
        
        total = query.count()
        
        condolences = query.order_by(
            Condolence.is_featured.desc(),
            Condolence.created_at.desc()
        ).offset(offset).limit(limit).all()
        
        return condolences, total
    
    @staticmethod
    def get_pending_count(db: Session, memorial_id: int) -> int:
        """Obtener cantidad de condolencias pendientes"""
        return db.query(Condolence).filter(
            Condolence.memorial_id == memorial_id,
            Condolence.is_approved == False
        ).count()
    
    @staticmethod
    def update(
        db: Session, 
        condolence_id: int, 
        update_data: CondolenceUpdate
    ) -> Optional[Condolence]:
        """Actualizar condolencia (moderación)"""
        condolence = db.query(Condolence).filter(Condolence.id == condolence_id).first()
        if not condolence:
            return None
        
        update_dict = update_data.model_dump(exclude_unset=True)
        
        # Si se aprueba, agregar fecha de aprobación
        if update_dict.get('is_approved') == True and not condolence.is_approved:
            from datetime import datetime, timezone
            condolence.approved_at = datetime.now(timezone.utc)
        
        for key, value in update_dict.items():
            setattr(condolence, key, value)
        
        db.commit()
        db.refresh(condolence)
        return condolence
    
    @staticmethod
    def delete(db: Session, condolence_id: int) -> bool:
        """Eliminar condolencia"""
        condolence = db.query(Condolence).filter(Condolence.id == condolence_id).first()
        if not condolence:
            return False
        
        db.delete(condolence)
        db.commit()
        return True
    
    @staticmethod
    def get_total_by_memorial(db: Session, memorial_id: int) -> int:
        """Obtener total de condolencias aprobadas"""
        return db.query(Condolence).filter(
            Condolence.memorial_id == memorial_id,
            Condolence.is_approved == True
        ).count()
