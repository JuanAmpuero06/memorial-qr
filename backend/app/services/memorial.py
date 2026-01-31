"""
Servicio de memoriales - Lógica de negocio
"""
import os
import uuid
import shutil
from typing import List
from fastapi import HTTPException, UploadFile, status
from sqlalchemy.orm import Session
from app.models import Memorial, User
from app.repositories import MemorialRepository
from app.schemas import MemorialCreate
from app.config import settings


class MemorialService:
    """Servicio de gestión de memoriales"""
    
    @staticmethod
    def create_memorial(db: Session, memorial: MemorialCreate, user_id: int) -> Memorial:
        """
        Crear nuevo memorial
        
        Args:
            db: Sesión de base de datos
            memorial: Datos del memorial
            user_id: ID del usuario propietario
            
        Returns:
            Memorial creado
        """
        return MemorialRepository.create(db, memorial, user_id)
    
    @staticmethod
    def get_user_memorials(db: Session, user_id: int) -> List[Memorial]:
        """
        Obtener todos los memoriales de un usuario
        
        Args:
            db: Sesión de base de datos
            user_id: ID del usuario
            
        Returns:
            Lista de memoriales
        """
        return MemorialRepository.get_by_user(db, user_id)
    
    @staticmethod
    def get_public_memorial(db: Session, slug: str) -> Memorial:
        """
        Obtener memorial público por slug
        
        Args:
            db: Sesión de base de datos
            slug: Slug del memorial
            
        Returns:
            Memorial encontrado
            
        Raises:
            HTTPException: Si el memorial no existe
        """
        memorial = MemorialRepository.get_by_slug(db, slug)
        if not memorial:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Memorial no encontrado"
            )
        return memorial
    
    @staticmethod
    async def upload_photo(
        db: Session,
        memorial_id: int,
        file: UploadFile,
        current_user: User
    ) -> Memorial:
        """
        Subir foto a un memorial
        
        Args:
            db: Sesión de base de datos
            memorial_id: ID del memorial
            file: Archivo de imagen
            current_user: Usuario actual
            
        Returns:
            Memorial actualizado
            
        Raises:
            HTTPException: Si el memorial no existe o el usuario no tiene permiso
        """
        # Verificar que el memorial existe
        memorial = MemorialRepository.get_by_id(db, memorial_id)
        if not memorial:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Memorial no encontrado"
            )
        
        # Verificar permisos
        if memorial.owner_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permiso para editar este memorial"
            )
        
        # Crear directorio si no existe
        os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
        
        # Generar nombre único
        file_extension = file.filename.split(".")[-1]
        unique_filename = f"{uuid.uuid4()}.{file_extension}"
        file_path = f"{settings.UPLOAD_DIR}/{unique_filename}"
        
        # Guardar archivo
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Actualizar BD
        return MemorialRepository.update_image(db, memorial, unique_filename)
