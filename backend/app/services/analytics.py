"""
Servicio de Analytics - Lógica de negocio para visitas y reacciones
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from app.repositories import MemorialRepository, VisitRepository, ReactionRepository
from app.schemas import (
    VisitStats, DailyVisitStat, MemorialAnalytics, DashboardAnalytics,
    ReactionCount, MemorialReactions
)


class AnalyticsService:
    """Servicio de gestión de analytics"""
    
    @staticmethod
    async def register_visit_async(db: Session, memorial_id: int, ip_address: str = None,
                                    user_agent: str = None, referrer: str = None):
        """Registrar una nueva visita con geolocalización asíncrona"""
        from app.services.geo import GeoService
        
        # Obtener geolocalización
        country = None
        city = None
        
        if ip_address:
            try:
                location = await GeoService.get_location(ip_address)
                country = location.country
                city = location.city
            except Exception as e:
                print(f"Error en geolocalización: {e}")
        
        return VisitRepository.create(
            db, memorial_id, ip_address, user_agent, referrer,
            country=country, city=city
        )
    
    @staticmethod
    def register_visit(db: Session, memorial_id: int, ip_address: str = None,
                       user_agent: str = None, referrer: str = None):
        """Registrar una nueva visita (versión síncrona sin geo)"""
        return VisitRepository.create(db, memorial_id, ip_address, user_agent, referrer)
    
    @staticmethod
    def get_memorial_stats(db: Session, memorial_id: int) -> VisitStats:
        """Obtener estadísticas de visitas de un memorial"""
        return VisitStats(
            total_visits=VisitRepository.get_total_count(db, memorial_id),
            today_visits=VisitRepository.get_today_count(db, memorial_id),
            week_visits=VisitRepository.get_week_count(db, memorial_id),
            month_visits=VisitRepository.get_month_count(db, memorial_id)
        )
    
    @staticmethod
    def get_memorial_analytics(db: Session, memorial_id: int, memorial_name: str, 
                                memorial_slug: str) -> MemorialAnalytics:
        """Obtener analytics completo de un memorial"""
        stats = AnalyticsService.get_memorial_stats(db, memorial_id)
        daily_visits = VisitRepository.get_daily_stats(db, memorial_id, days=30)
        reactions_count = ReactionRepository.get_counts_by_memorial(db, memorial_id)
        
        return MemorialAnalytics(
            memorial_id=memorial_id,
            memorial_name=memorial_name,
            memorial_slug=memorial_slug,
            stats=stats,
            daily_visits=[DailyVisitStat(**d) for d in daily_visits],
            reactions_count=reactions_count
        )
    
    @staticmethod
    def get_dashboard_analytics(db: Session, user_id: int) -> DashboardAnalytics:
        """Obtener analytics del dashboard para un usuario"""
        # Obtener memoriales del usuario
        memorials = MemorialRepository.get_by_user(db, user_id)
        memorial_ids = [m.id for m in memorials]
        
        # Obtener totales
        total_visits = VisitRepository.get_total_visits_for_user(db, memorial_ids)
        total_reactions = ReactionRepository.get_total_reactions_for_user(db, memorial_ids)
        
        # Obtener analytics por memorial
        memorials_analytics = []
        for memorial in memorials:
            analytics = AnalyticsService.get_memorial_analytics(
                db, memorial.id, memorial.name, memorial.slug
            )
            memorials_analytics.append(analytics)
        
        return DashboardAnalytics(
            total_memorials=len(memorials),
            total_visits=total_visits,
            total_reactions=total_reactions,
            memorials_analytics=memorials_analytics
        )
    
    @staticmethod
    def toggle_reaction(db: Session, memorial_id: int, reaction_type: str, 
                        visitor_id: str) -> dict:
        """Toggle de reacción"""
        return ReactionRepository.toggle_reaction(db, memorial_id, reaction_type, visitor_id)
    
    @staticmethod
    def get_memorial_reactions(db: Session, memorial_id: int, 
                                visitor_id: str = None) -> MemorialReactions:
        """Obtener reacciones de un memorial"""
        counts = ReactionRepository.get_counts_by_memorial(db, memorial_id)
        user_reactions = []
        
        if visitor_id:
            user_reactions = ReactionRepository.get_user_reactions(db, memorial_id, visitor_id)
        
        return MemorialReactions(
            memorial_id=memorial_id,
            counts=ReactionCount(**counts),
            user_reactions=user_reactions
        )
