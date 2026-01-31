"""
Endpoints de Condolencias - Libro de visitas digital
"""
from typing import Optional
from fastapi import APIRouter, Depends, Request, Query
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import User
from app.schemas import (
    CondolenceCreate, CondolenceUpdate, CondolenceResponse, 
    CondolenceListResponse
)
from app.services import CondolenceService
from app.api.deps import get_current_user
from app.core.rate_limit import limiter, RateLimits


router = APIRouter()


# ============ ENDPOINTS PÚBLICOS ============

@router.get("/{slug}", response_model=CondolenceListResponse)
@limiter.limit(RateLimits.PUBLIC_READ)
async def get_condolences(
    request: Request,
    slug: str,
    limit: int = Query(default=50, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db)
):
    """
    Obtener condolencias aprobadas de un memorial (público)
    Rate limit: 30 peticiones por minuto
    
    Args:
        slug: Slug del memorial
        limit: Límite de resultados
        offset: Desplazamiento
        
    Returns:
        Lista de condolencias aprobadas
    """
    return CondolenceService.get_condolences(
        db, slug, approved_only=True, limit=limit, offset=offset
    )


@router.post("/{slug}", response_model=CondolenceResponse, status_code=201)
@limiter.limit(RateLimits.PUBLIC_WRITE)
async def create_condolence(
    slug: str,
    condolence: CondolenceCreate,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Crear nueva condolencia (público, requiere moderación)
    Rate limit: 10 condolencias por minuto (prevenir spam)
    
    Args:
        slug: Slug del memorial
        condolence: Datos de la condolencia
        
    Returns:
        Condolencia creada (pendiente de aprobación)
    """
    ip_address = request.client.host if request.client else None
    
    result = CondolenceService.create_condolence(db, slug, condolence, ip_address)
    
    return result


# ============ ENDPOINTS AUTENTICADOS (MODERACIÓN) ============

@router.get("/manage/{slug}", response_model=CondolenceListResponse)
async def get_all_condolences(
    slug: str,
    limit: int = Query(default=50, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Obtener todas las condolencias (incluyendo pendientes) para el propietario
    
    Args:
        slug: Slug del memorial
        
    Returns:
        Lista de todas las condolencias con conteo de pendientes
    """
    # Verificar que el usuario es propietario
    from app.repositories import MemorialRepository
    memorial = MemorialRepository.get_by_slug(db, slug)
    
    if not memorial or memorial.owner_id != current_user.id:
        from fastapi import HTTPException, status
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para ver estas condolencias"
        )
    
    return CondolenceService.get_condolences(
        db, slug, approved_only=False, limit=limit, offset=offset
    )


@router.patch("/{condolence_id}", response_model=CondolenceResponse)
async def moderate_condolence(
    condolence_id: int,
    update_data: CondolenceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Moderar condolencia (aprobar/rechazar/destacar)
    
    Args:
        condolence_id: ID de la condolencia
        update_data: Datos de moderación
        
    Returns:
        Condolencia actualizada
    """
    return CondolenceService.moderate_condolence(
        db, condolence_id, current_user.id, update_data
    )


@router.delete("/{condolence_id}")
async def delete_condolence(
    condolence_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Eliminar condolencia
    
    Args:
        condolence_id: ID de la condolencia
        
    Returns:
        Confirmación de eliminación
    """
    CondolenceService.delete_condolence(db, condolence_id, current_user.id)
    return {"message": "Condolencia eliminada"}
