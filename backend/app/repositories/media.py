"""
Repositorio de Galería Multimedia
"""
import os
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models import MediaItem
from app.schemas import MediaItemCreate, MediaItemUpdate
from app.config import settings


class MediaRepository:
    """Repositorio para operaciones de base de datos de galería multimedia"""
    
    @staticmethod
    def create(
        db: Session, 
        memorial_id: int, 
        filename: str,
        original_filename: str,
        media_type: str = "image",
        mime_type: str = None,
        file_size: int = None,
        metadata: MediaItemCreate = None
    ) -> MediaItem:
        """Crear nuevo elemento multimedia"""
        db_item = MediaItem(
            memorial_id=memorial_id,
            filename=filename,
            original_filename=original_filename,
            media_type=media_type,
            mime_type=mime_type,
            file_size=file_size,
            title=metadata.title if metadata else None,
            caption=metadata.caption if metadata else None,
            alt_text=metadata.alt_text if metadata else None,
            taken_at=metadata.taken_at if metadata else None,
            location=metadata.location if metadata else None,
            display_order=metadata.display_order if metadata else 0,
            is_featured=metadata.is_featured if metadata else False
        )
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item
    
    @staticmethod
    def get_by_id(db: Session, item_id: int) -> Optional[MediaItem]:
        """Obtener elemento por ID"""
        return db.query(MediaItem).filter(MediaItem.id == item_id).first()
    
    @staticmethod
    def get_by_memorial(db: Session, memorial_id: int) -> List[MediaItem]:
        """Obtener todos los elementos de un memorial"""
        return db.query(MediaItem).filter(
            MediaItem.memorial_id == memorial_id
        ).order_by(
            MediaItem.is_featured.desc(),
            MediaItem.display_order.asc(),
            MediaItem.created_at.desc()
        ).all()
    
    @staticmethod
    def update(
        db: Session, 
        item_id: int, 
        update_data: MediaItemUpdate
    ) -> Optional[MediaItem]:
        """Actualizar elemento multimedia"""
        item = db.query(MediaItem).filter(MediaItem.id == item_id).first()
        if not item:
            return None
        
        update_dict = update_data.model_dump(exclude_unset=True)
        
        # Si se marca como cover, desmarcar otras
        if update_dict.get('is_cover') == True:
            db.query(MediaItem).filter(
                MediaItem.memorial_id == item.memorial_id,
                MediaItem.id != item_id
            ).update({'is_cover': False})
        
        for key, value in update_dict.items():
            setattr(item, key, value)
        
        db.commit()
        db.refresh(item)
        return item
    
    @staticmethod
    def delete(db: Session, item_id: int) -> bool:
        """Eliminar elemento multimedia"""
        item = db.query(MediaItem).filter(MediaItem.id == item_id).first()
        if not item:
            return False
        
        # Eliminar archivo físico
        try:
            file_path = os.path.join(settings.UPLOAD_DIR, item.filename)
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f"Error eliminando archivo: {e}")
        
        db.delete(item)
        db.commit()
        return True
    
    @staticmethod
    def get_count(db: Session, memorial_id: int) -> int:
        """Obtener cantidad de elementos en galería"""
        return db.query(MediaItem).filter(
            MediaItem.memorial_id == memorial_id
        ).count()
    
    @staticmethod
    def update_dimensions(
        db: Session, 
        item_id: int, 
        width: int, 
        height: int
    ) -> Optional[MediaItem]:
        """Actualizar dimensiones de imagen/video"""
        item = db.query(MediaItem).filter(MediaItem.id == item_id).first()
        if not item:
            return None
        
        item.width = width
        item.height = height
        db.commit()
        db.refresh(item)
        return item
    
    @staticmethod
    def reorder(db: Session, memorial_id: int, item_ids: List[int]) -> bool:
        """Reordenar elementos de galería"""
        for order, item_id in enumerate(item_ids):
            item = db.query(MediaItem).filter(
                MediaItem.id == item_id,
                MediaItem.memorial_id == memorial_id
            ).first()
            if item:
                item.display_order = order
        
        db.commit()
        return True
