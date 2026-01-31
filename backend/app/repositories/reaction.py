"""
Repositorio de Reacciones - Capa de acceso a datos
"""
from typing import List, Optional, Dict
from sqlalchemy.orm import Session
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from app.models import Reaction


class ReactionRepository:
    """Repositorio para operaciones de base de datos de reacciones"""
    
    @staticmethod
    def create(db: Session, memorial_id: int, reaction_type: str, visitor_id: str) -> Optional[Reaction]:
        """Crear nueva reacción"""
        try:
            db_reaction = Reaction(
                memorial_id=memorial_id,
                reaction_type=reaction_type,
                visitor_id=visitor_id
            )
            db.add(db_reaction)
            db.commit()
            db.refresh(db_reaction)
            return db_reaction
        except IntegrityError:
            db.rollback()
            return None
    
    @staticmethod
    def delete(db: Session, memorial_id: int, reaction_type: str, visitor_id: str) -> bool:
        """Eliminar una reacción"""
        reaction = db.query(Reaction).filter(
            Reaction.memorial_id == memorial_id,
            Reaction.reaction_type == reaction_type,
            Reaction.visitor_id == visitor_id
        ).first()
        
        if reaction:
            db.delete(reaction)
            db.commit()
            return True
        return False
    
    @staticmethod
    def get_counts_by_memorial(db: Session, memorial_id: int) -> Dict[str, int]:
        """Obtener conteo de reacciones por tipo para un memorial"""
        results = db.query(
            Reaction.reaction_type,
            func.count(Reaction.id).label('count')
        ).filter(
            Reaction.memorial_id == memorial_id
        ).group_by(
            Reaction.reaction_type
        ).all()
        
        counts = {
            'candle': 0,
            'flower': 0,
            'heart': 0,
            'pray': 0,
            'dove': 0
        }
        
        for r in results:
            if r.reaction_type in counts:
                counts[r.reaction_type] = r.count
        
        return counts
    
    @staticmethod
    def get_user_reactions(db: Session, memorial_id: int, visitor_id: str) -> List[str]:
        """Obtener las reacciones de un visitante específico"""
        reactions = db.query(Reaction.reaction_type).filter(
            Reaction.memorial_id == memorial_id,
            Reaction.visitor_id == visitor_id
        ).all()
        
        return [r.reaction_type for r in reactions]
    
    @staticmethod
    def get_total_for_memorial(db: Session, memorial_id: int) -> int:
        """Obtener total de reacciones de un memorial"""
        return db.query(Reaction).filter(Reaction.memorial_id == memorial_id).count()
    
    @staticmethod
    def get_total_reactions_for_user(db: Session, memorial_ids: List[int]) -> int:
        """Obtener total de reacciones para múltiples memoriales"""
        if not memorial_ids:
            return 0
        return db.query(Reaction).filter(Reaction.memorial_id.in_(memorial_ids)).count()
    
    @staticmethod
    def toggle_reaction(db: Session, memorial_id: int, reaction_type: str, visitor_id: str) -> dict:
        """Toggle de reacción (agregar si no existe, eliminar si existe)"""
        existing = db.query(Reaction).filter(
            Reaction.memorial_id == memorial_id,
            Reaction.reaction_type == reaction_type,
            Reaction.visitor_id == visitor_id
        ).first()
        
        if existing:
            db.delete(existing)
            db.commit()
            return {"action": "removed", "reaction_type": reaction_type}
        else:
            new_reaction = Reaction(
                memorial_id=memorial_id,
                reaction_type=reaction_type,
                visitor_id=visitor_id
            )
            db.add(new_reaction)
            db.commit()
            return {"action": "added", "reaction_type": reaction_type}
