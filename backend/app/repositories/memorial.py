"""
Repositorio de memoriales - Capa de acceso a datos
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models import Memorial
from app.schemas import MemorialCreate
from slugify import slugify
import uuid


class MemorialRepository:
    """Repositorio para operaciones de base de datos de memoriales"""
    
    @staticmethod
    def get_by_id(db: Session, memorial_id: int) -> Optional[Memorial]:
        """Obtener memorial por ID"""
        return db.query(Memorial).filter(Memorial.id == memorial_id).first()
    
    @staticmethod
    def get_by_slug(db: Session, slug: str) -> Optional[Memorial]:
        """Obtener memorial por slug"""
        return db.query(Memorial).filter(Memorial.slug == slug).first()
    
    @staticmethod
    def get_by_user(db: Session, user_id: int) -> List[Memorial]:
        """Obtener todos los memoriales de un usuario"""
        return db.query(Memorial).filter(Memorial.owner_id == user_id).all()
    
    @staticmethod
    def create(db: Session, memorial: MemorialCreate, user_id: int) -> Memorial:
        """Crear nuevo memorial"""
        # Generar slug único
        base_slug = slugify(memorial.name)
        unique_suffix = str(uuid.uuid4())[:8]
        final_slug = f"{base_slug}-{unique_suffix}"
        
        db_memorial = Memorial(
            name=memorial.name,
            epitaph=memorial.epitaph,
            bio=memorial.bio,
            slug=final_slug,
            owner_id=user_id
        )
        db.add(db_memorial)
        db.commit()
        db.refresh(db_memorial)
        return db_memorial
    
    @staticmethod
    def update_image(db: Session, memorial: Memorial, image_filename: str) -> Memorial:
        """Actualizar la imagen de un memorial"""
        memorial.image_filename = image_filename
        db.commit()
        db.refresh(memorial)
        return memorial
    
    @staticmethod
    def delete(db: Session, memorial: Memorial) -> None:
        """Eliminar un memorial"""
        db.delete(memorial)
        db.commit()
