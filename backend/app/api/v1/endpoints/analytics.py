"""
Endpoints de Analytics - Visitas y Reacciones
"""
from typing import Optional
from datetime import date, datetime, timedelta
from fastapi import APIRouter, Depends, Request, Header, Query
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import User
from app.schemas import DashboardAnalytics, MemorialReactions, ReactionCreate
from app.services import AnalyticsService
from app.api.deps import get_current_user
from app.repositories import MemorialRepository, VisitRepository
from app.core.rate_limit import limiter, RateLimits


router = APIRouter()


@router.get("/dashboard", response_model=DashboardAnalytics)
@limiter.limit(RateLimits.ANALYTICS)
async def get_dashboard_analytics(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    start_date: Optional[date] = Query(None, description="Fecha inicio (YYYY-MM-DD)"),
    end_date: Optional[date] = Query(None, description="Fecha fin (YYYY-MM-DD)"),
    period: Optional[str] = Query(None, description="Período: today, week, month, year, all")
):
    """
    Obtener analytics del dashboard para el usuario autenticado
    
    Args:
        start_date: Filtrar desde esta fecha
        end_date: Filtrar hasta esta fecha
        period: Período predefinido (today, week, month, year, all)
        
    Returns:
        Analytics completo del dashboard
    """
    # Procesar período predefinido
    if period:
        today = date.today()
        if period == "today":
            start_date = today
            end_date = today
        elif period == "week":
            start_date = today - timedelta(days=7)
            end_date = today
        elif period == "month":
            start_date = today - timedelta(days=30)
            end_date = today
        elif period == "year":
            start_date = today - timedelta(days=365)
            end_date = today
        # "all" = sin filtros
    
    return AnalyticsService.get_dashboard_analytics(
        db, current_user.id, start_date=start_date, end_date=end_date
    )


@router.get("/filtered/{slug}")
async def get_filtered_analytics(
    slug: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    period: Optional[str] = Query(None)
):
    """
    Obtener analytics filtrados para un memorial específico
    """
    memorial = MemorialRepository.get_by_slug(db, slug)
    if not memorial or memorial.owner_id != current_user.id:
        from fastapi import HTTPException, status
        raise HTTPException(status_code=404, detail="Memorial no encontrado")
    
    # Procesar período
    if period:
        today = date.today()
        periods = {
            "today": (today, today),
            "week": (today - timedelta(days=7), today),
            "month": (today - timedelta(days=30), today),
            "year": (today - timedelta(days=365), today),
        }
        if period in periods:
            start_date, end_date = periods[period]
    
    return AnalyticsService.get_memorial_analytics_filtered(
        db, memorial.id, memorial.name, memorial.slug,
        start_date=start_date, end_date=end_date
    )


@router.post("/visit/{slug}")
@limiter.limit(RateLimits.PUBLIC_READ)
async def register_visit(
    slug: str,
    request: Request,
    db: Session = Depends(get_db),
    user_agent: Optional[str] = Header(None),
    referer: Optional[str] = Header(None)
):
    """
    Registrar una visita a un memorial (endpoint público)
    Rate limit: 30 visitas por minuto por IP
    
    Args:
        slug: Slug del memorial
        request: Request para obtener IP
        
    Returns:
        Confirmación de visita registrada
    """
    # Obtener memorial por slug
    memorial = MemorialRepository.get_by_slug(db, slug)
    if not memorial:
        return {"error": "Memorial no encontrado"}
    
    # Obtener IP del cliente
    client_ip = request.client.host if request.client else None
    
    # Registrar visita con geolocalización asíncrona
    await AnalyticsService.register_visit_async(
        db, 
        memorial.id, 
        ip_address=client_ip,
        user_agent=user_agent,
        referrer=referer
    )
    
    return {"message": "Visita registrada", "memorial_id": memorial.id}


@router.get("/locations/{slug}")
async def get_location_stats(
    slug: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Obtener estadísticas de ubicación de visitantes
    
    Args:
        slug: Slug del memorial
        
    Returns:
        Estadísticas de ubicación
    """
    from app.repositories import VisitRepository
    
    memorial = MemorialRepository.get_by_slug(db, slug)
    if not memorial:
        return {"error": "Memorial no encontrado"}
    
    if memorial.owner_id != current_user.id:
        from fastapi import HTTPException, status
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para ver estas estadísticas"
        )
    
    locations = VisitRepository.get_location_stats(db, memorial.id)
    return {"memorial_id": memorial.id, "locations": locations}


@router.get("/reactions/{slug}", response_model=MemorialReactions)
@limiter.limit(RateLimits.PUBLIC_READ)
async def get_reactions(
    request: Request,
    slug: str,
    visitor_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Obtener reacciones de un memorial (endpoint público)
    Rate limit: 30 peticiones por minuto
    
    Args:
        slug: Slug del memorial
        visitor_id: ID del visitante para obtener sus reacciones
        
    Returns:
        Reacciones del memorial
    """
    memorial = MemorialRepository.get_by_slug(db, slug)
    if not memorial:
        return MemorialReactions(memorial_id=0, counts={}, user_reactions=[])
    
    return AnalyticsService.get_memorial_reactions(db, memorial.id, visitor_id)


@router.post("/reactions/{slug}")
@limiter.limit(RateLimits.PUBLIC_WRITE)
async def toggle_reaction(
    request: Request,
    slug: str,
    reaction_data: ReactionCreate,
    db: Session = Depends(get_db)
):
    """
    Toggle de reacción en un memorial (endpoint público)
    Rate limit: 10 reacciones por minuto (prevenir spam)
    
    Args:
        slug: Slug del memorial
        reaction_data: Datos de la reacción
        
    Returns:
        Resultado del toggle
    """
    memorial = MemorialRepository.get_by_slug(db, slug)
    if not memorial:
        return {"error": "Memorial no encontrado"}
    
    # Validar tipo de reacción
    valid_types = ['candle', 'flower', 'heart', 'pray', 'dove']
    if reaction_data.reaction_type not in valid_types:
        return {"error": "Tipo de reacción no válido"}
    
    result = AnalyticsService.toggle_reaction(
        db, 
        memorial.id, 
        reaction_data.reaction_type, 
        reaction_data.visitor_id
    )
    
    # Obtener conteos actualizados
    reactions = AnalyticsService.get_memorial_reactions(
        db, memorial.id, reaction_data.visitor_id
    )
    
    return {
        **result,
        "counts": reactions.counts,
        "user_reactions": reactions.user_reactions
    }
