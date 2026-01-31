"""
Repositorio de Visitas - Capa de acceso a datos
"""
from typing import List, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func, cast, Date
from app.models import Visit


class VisitRepository:
    """Repositorio para operaciones de base de datos de visitas"""
    
    @staticmethod
    def create(db: Session, memorial_id: int, ip_address: str = None, 
               user_agent: str = None, referrer: str = None) -> Visit:
        """Crear nueva visita"""
        db_visit = Visit(
            memorial_id=memorial_id,
            ip_address=ip_address,
            user_agent=user_agent,
            referrer=referrer
        )
        db.add(db_visit)
        db.commit()
        db.refresh(db_visit)
        return db_visit
    
    @staticmethod
    def get_by_memorial(db: Session, memorial_id: int) -> List[Visit]:
        """Obtener todas las visitas de un memorial"""
        return db.query(Visit).filter(Visit.memorial_id == memorial_id).all()
    
    @staticmethod
    def get_total_count(db: Session, memorial_id: int) -> int:
        """Obtener total de visitas de un memorial"""
        return db.query(Visit).filter(Visit.memorial_id == memorial_id).count()
    
    @staticmethod
    def get_today_count(db: Session, memorial_id: int) -> int:
        """Obtener visitas de hoy de un memorial"""
        today = datetime.utcnow().date()
        return db.query(Visit).filter(
            Visit.memorial_id == memorial_id,
            cast(Visit.visited_at, Date) == today
        ).count()
    
    @staticmethod
    def get_week_count(db: Session, memorial_id: int) -> int:
        """Obtener visitas de la última semana de un memorial"""
        week_ago = datetime.utcnow() - timedelta(days=7)
        return db.query(Visit).filter(
            Visit.memorial_id == memorial_id,
            Visit.visited_at >= week_ago
        ).count()
    
    @staticmethod
    def get_month_count(db: Session, memorial_id: int) -> int:
        """Obtener visitas del último mes de un memorial"""
        month_ago = datetime.utcnow() - timedelta(days=30)
        return db.query(Visit).filter(
            Visit.memorial_id == memorial_id,
            Visit.visited_at >= month_ago
        ).count()
    
    @staticmethod
    def get_daily_stats(db: Session, memorial_id: int, days: int = 30) -> List[dict]:
        """Obtener estadísticas diarias de visitas"""
        start_date = datetime.utcnow() - timedelta(days=days)
        
        results = db.query(
            cast(Visit.visited_at, Date).label('date'),
            func.count(Visit.id).label('count')
        ).filter(
            Visit.memorial_id == memorial_id,
            Visit.visited_at >= start_date
        ).group_by(
            cast(Visit.visited_at, Date)
        ).order_by(
            cast(Visit.visited_at, Date)
        ).all()
        
        return [{"date": str(r.date), "count": r.count} for r in results]
    
    @staticmethod
    def get_total_visits_for_user(db: Session, memorial_ids: List[int]) -> int:
        """Obtener total de visitas para múltiples memoriales"""
        if not memorial_ids:
            return 0
        return db.query(Visit).filter(Visit.memorial_id.in_(memorial_ids)).count()
