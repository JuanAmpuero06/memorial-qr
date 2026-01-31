"""
Servicio de Condolencias - Libro de visitas digital
"""
from typing import List, Tuple
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models import Condolence, Memorial
from app.repositories import CondolenceRepository, MemorialRepository
from app.schemas import CondolenceCreate, CondolenceUpdate, CondolenceListResponse, CondolencePublic


class CondolenceService:
    """Servicio de gestión de condolencias"""
    
    @staticmethod
    def create_condolence(
        db: Session, 
        slug: str, 
        condolence: CondolenceCreate,
        ip_address: str = None
    ) -> Condolence:
        """
        Crear nueva condolencia en un memorial
        
        Args:
            db: Sesión de base de datos
            slug: Slug del memorial
            condolence: Datos de la condolencia
            ip_address: IP del visitante
            
        Returns:
            Condolencia creada
        """
        memorial = MemorialRepository.get_by_slug(db, slug)
        if not memorial:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Memorial no encontrado"
            )
        
        return CondolenceRepository.create(db, memorial.id, condolence, ip_address)
    
    @staticmethod
    def get_condolences(
        db: Session, 
        slug: str, 
        approved_only: bool = True,
        limit: int = 50,
        offset: int = 0
    ) -> CondolenceListResponse:
        """
        Obtener condolencias de un memorial
        
        Args:
            db: Sesión de base de datos
            slug: Slug del memorial
            approved_only: Solo aprobadas (para visitantes)
            limit: Límite de resultados
            offset: Desplazamiento
            
        Returns:
            Lista de condolencias
        """
        memorial = MemorialRepository.get_by_slug(db, slug)
        if not memorial:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Memorial no encontrado"
            )
        
        condolences, total = CondolenceRepository.get_by_memorial(
            db, memorial.id, approved_only, limit, offset
        )
        
        pending_count = 0
        if not approved_only:
            pending_count = CondolenceRepository.get_pending_count(db, memorial.id)
        
        return CondolenceListResponse(
            items=[CondolencePublic.model_validate(c) for c in condolences],
            total=total,
            pending_count=pending_count
        )
    
    @staticmethod
    def moderate_condolence(
        db: Session, 
        condolence_id: int, 
        user_id: int,
        update_data: CondolenceUpdate
    ) -> Condolence:
        """
        Moderar condolencia (aprobar/rechazar/destacar)
        
        Args:
            db: Sesión de base de datos
            condolence_id: ID de la condolencia
            user_id: ID del usuario que modera
            update_data: Datos de actualización
            
        Returns:
            Condolencia actualizada
        """
        condolence = CondolenceRepository.get_by_id(db, condolence_id)
        if not condolence:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Condolencia no encontrada"
            )
        
        # Verificar que el usuario es propietario del memorial
        if condolence.memorial.owner_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permiso para moderar esta condolencia"
            )
        
        return CondolenceRepository.update(db, condolence_id, update_data)
    
    @staticmethod
    def delete_condolence(db: Session, condolence_id: int, user_id: int) -> bool:
        """
        Eliminar condolencia
        
        Args:
            db: Sesión de base de datos
            condolence_id: ID de la condolencia
            user_id: ID del usuario
            
        Returns:
            True si se eliminó correctamente
        """
        condolence = CondolenceRepository.get_by_id(db, condolence_id)
        if not condolence:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Condolencia no encontrada"
            )
        
        if condolence.memorial.owner_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permiso para eliminar esta condolencia"
            )
        
        return CondolenceRepository.delete(db, condolence_id)
