"""
Endpoints de Analytics - Visitas y Reacciones
"""
from typing import Optional
from fastapi import APIRouter, Depends, Request, Header
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import User
from app.schemas import DashboardAnalytics, MemorialReactions, ReactionCreate
from app.services import AnalyticsService
from app.api.deps import get_current_user
from app.repositories import MemorialRepository


router = APIRouter()


@router.get("/dashboard", response_model=DashboardAnalytics)
async def get_dashboard_analytics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Obtener analytics del dashboard para el usuario autenticado
    
    Returns:
        Analytics completo del dashboard
    """
    return AnalyticsService.get_dashboard_analytics(db, current_user.id)


@router.post("/visit/{slug}")
async def register_visit(
    slug: str,
    request: Request,
    db: Session = Depends(get_db),
    user_agent: Optional[str] = Header(None),
    referer: Optional[str] = Header(None)
):
    """
    Registrar una visita a un memorial (endpoint público)
    
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
async def get_reactions(
    slug: str,
    visitor_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Obtener reacciones de un memorial (endpoint público)
    
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
async def toggle_reaction(
    slug: str,
    reaction_data: ReactionCreate,
    db: Session = Depends(get_db)
):
    """
    Toggle de reacción en un memorial (endpoint público)
    
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
