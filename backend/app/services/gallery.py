"""
Servicio de Galería Multimedia
"""
import os
import uuid
from typing import List
from sqlalchemy.orm import Session
from fastapi import HTTPException, UploadFile, status
from app.models import MediaItem
from app.repositories import MediaRepository, MemorialRepository
from app.schemas import MediaItemCreate, MediaItemUpdate, GalleryResponse, MediaItemResponse
from app.config import settings


class GalleryService:
    """Servicio de gestión de galería multimedia"""
    
    # Límite de archivos por memorial
    MAX_ITEMS_PER_MEMORIAL = 50
    
    # Tamaño máximo por archivo (10MB)
    MAX_FILE_SIZE = 10 * 1024 * 1024
    
    # Tipos permitidos
    ALLOWED_IMAGE_TYPES = ["image/jpeg", "image/png", "image/webp", "image/gif"]
    ALLOWED_VIDEO_TYPES = ["video/mp4", "video/webm"]
    
    @staticmethod
    async def upload_media(
        db: Session,
        memorial_id: int,
        file: UploadFile,
        user_id: int,
        metadata: MediaItemCreate = None
    ) -> MediaItem:
        """
        Subir archivo multimedia a la galería
        
        Args:
            db: Sesión de base de datos
            memorial_id: ID del memorial
            file: Archivo subido
            user_id: ID del usuario
            metadata: Metadatos opcionales
            
        Returns:
            Elemento multimedia creado
        """
        # Verificar memorial y permisos
        memorial = MemorialRepository.get_by_id(db, memorial_id)
        if not memorial:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Memorial no encontrado"
            )
        
        if memorial.owner_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permiso para modificar este memorial"
            )
        
        # Verificar límite de archivos
        current_count = MediaRepository.get_count(db, memorial_id)
        if current_count >= GalleryService.MAX_ITEMS_PER_MEMORIAL:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Límite de {GalleryService.MAX_ITEMS_PER_MEMORIAL} archivos alcanzado"
            )
        
        # Determinar tipo de media
        content_type = file.content_type or ""
        if content_type in GalleryService.ALLOWED_IMAGE_TYPES:
            media_type = "image"
        elif content_type in GalleryService.ALLOWED_VIDEO_TYPES:
            media_type = "video"
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Tipo de archivo no permitido"
            )
        
        # Leer contenido y verificar tamaño
        content = await file.read()
        file_size = len(content)
        
        if file_size > GalleryService.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El archivo excede el tamaño máximo permitido (10MB)"
            )
        
        # Generar nombre único
        ext = file.filename.split(".")[-1] if file.filename and "." in file.filename else "jpg"
        filename = f"gallery_{memorial_id}_{uuid.uuid4().hex[:12]}.{ext}"
        file_path = os.path.join(settings.UPLOAD_DIR, filename)
        
        # Crear directorio si no existe
        os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
        
        # Guardar archivo
        with open(file_path, "wb") as f:
            f.write(content)
        
        # Crear registro en base de datos
        item = MediaRepository.create(
            db,
            memorial_id=memorial_id,
            filename=filename,
            original_filename=file.filename,
            media_type=media_type,
            mime_type=content_type,
            file_size=file_size,
            metadata=metadata
        )
        
        # Intentar obtener dimensiones de imagen
        if media_type == "image":
            try:
                from PIL import Image
                from io import BytesIO
                img = Image.open(BytesIO(content))
                MediaRepository.update_dimensions(db, item.id, img.width, img.height)
            except Exception:
                pass
        
        return item
    
    @staticmethod
    def get_gallery(db: Session, slug: str) -> GalleryResponse:
        """
        Obtener galería de un memorial
        
        Args:
            db: Sesión de base de datos
            slug: Slug del memorial
            
        Returns:
            Galería con elementos
        """
        memorial = MemorialRepository.get_by_slug(db, slug)
        if not memorial:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Memorial no encontrado"
            )
        
        items = MediaRepository.get_by_memorial(db, memorial.id)
        
        return GalleryResponse(
            memorial_id=memorial.id,
            items=[MediaItemResponse.model_validate(i) for i in items],
            total=len(items)
        )
    
    @staticmethod
    def update_media_item(
        db: Session,
        item_id: int,
        user_id: int,
        update_data: MediaItemUpdate
    ) -> MediaItem:
        """
        Actualizar metadatos de elemento multimedia
        
        Args:
            db: Sesión de base de datos
            item_id: ID del elemento
            user_id: ID del usuario
            update_data: Datos de actualización
            
        Returns:
            Elemento actualizado
        """
        item = MediaRepository.get_by_id(db, item_id)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Elemento no encontrado"
            )
        
        if item.memorial.owner_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permiso para modificar este elemento"
            )
        
        return MediaRepository.update(db, item_id, update_data)
    
    @staticmethod
    def delete_media_item(db: Session, item_id: int, user_id: int) -> bool:
        """
        Eliminar elemento de galería
        
        Args:
            db: Sesión de base de datos
            item_id: ID del elemento
            user_id: ID del usuario
            
        Returns:
            True si se eliminó correctamente
        """
        item = MediaRepository.get_by_id(db, item_id)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Elemento no encontrado"
            )
        
        if item.memorial.owner_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permiso para eliminar este elemento"
            )
        
        return MediaRepository.delete(db, item_id)
