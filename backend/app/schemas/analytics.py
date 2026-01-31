"""
Schemas de Visitas y Reacciones
"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


# ============ VISITAS ============

class VisitCreate(BaseModel):
    """Schema para registrar visita"""
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    referrer: Optional[str] = None


class VisitResponse(BaseModel):
    """Schema de respuesta de visita"""
    id: int
    memorial_id: int
    visited_at: datetime
    country: Optional[str] = None
    city: Optional[str] = None
    
    class Config:
        from_attributes = True


class VisitStats(BaseModel):
    """Estadísticas de visitas"""
    total_visits: int
    today_visits: int
    week_visits: int
    month_visits: int


class DailyVisitStat(BaseModel):
    """Estadística diaria"""
    date: str
    count: int


class MemorialAnalytics(BaseModel):
    """Analytics completo de un memorial"""
    memorial_id: int
    memorial_name: str
    memorial_slug: str
    stats: VisitStats
    daily_visits: List[DailyVisitStat]
    reactions_count: dict


class DashboardAnalytics(BaseModel):
    """Analytics del dashboard general"""
    total_memorials: int
    total_visits: int
    total_reactions: int
    memorials_analytics: List[MemorialAnalytics]


# ============ REACCIONES ============

class ReactionCreate(BaseModel):
    """Schema para crear reacción"""
    reaction_type: str  # 'candle', 'flower', 'heart', 'pray', 'dove'
    visitor_id: str  # UUID del visitante


class ReactionResponse(BaseModel):
    """Schema de respuesta de reacción"""
    id: int
    memorial_id: int
    reaction_type: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class ReactionCount(BaseModel):
    """Conteo de reacciones por tipo"""
    candle: int = 0
    flower: int = 0
    heart: int = 0
    pray: int = 0
    dove: int = 0


class MemorialReactions(BaseModel):
    """Reacciones de un memorial"""
    memorial_id: int
    counts: ReactionCount
    user_reactions: List[str] = []  # Lista de tipos de reacción del usuario actual
