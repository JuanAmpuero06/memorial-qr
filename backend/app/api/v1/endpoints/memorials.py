"""
Endpoints de memoriales
"""
from typing import List
from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import User
from app.schemas import MemorialCreate, MemorialResponse, PublicMemorial
from app.services import MemorialService, QRService
from app.api.deps import get_current_user


router = APIRouter()


@router.post("/", response_model=MemorialResponse, status_code=201)
async def create_memorial(
    memorial: MemorialCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Crear nuevo memorial
    
    Args:
        memorial: Datos del memorial
        db: Sesión de base de datos
        current_user: Usuario autenticado
        
    Returns:
        Memorial creado
    """
    return MemorialService.create_memorial(db, memorial, current_user.id)


@router.get("/", response_model=List[MemorialResponse])
async def get_my_memorials(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Obtener todos los memoriales del usuario actual
    
    Args:
        db: Sesión de base de datos
        current_user: Usuario autenticado
        
    Returns:
        Lista de memoriales
    """
    return MemorialService.get_user_memorials(db, current_user.id)


@router.get("/public/{slug}", response_model=PublicMemorial)
async def get_public_memorial(
    slug: str,
    db: Session = Depends(get_db)
):
    """
    Obtener memorial público (sin autenticación)
    
    Args:
        slug: Slug del memorial
        db: Sesión de base de datos
        
    Returns:
        Memorial público
    """
    return MemorialService.get_public_memorial(db, slug)


@router.get("/{slug}/qr")
async def get_qr_code(
    slug: str,
    current_user: User = Depends(get_current_user)
):
    """
    Generar código QR para un memorial
    
    Args:
        slug: Slug del memorial
        current_user: Usuario autenticado
        
    Returns:
        Imagen QR
    """
    return QRService.generate_qr(slug)


@router.post("/{memorial_id}/upload-photo", response_model=MemorialResponse)
async def upload_photo(
    memorial_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Subir foto a un memorial
    
    Args:
        memorial_id: ID del memorial
        file: Archivo de imagen
        db: Sesión de base de datos
        current_user: Usuario autenticado
        
    Returns:
        Memorial actualizado
    """
    return await MemorialService.upload_photo(db, memorial_id, file, current_user)
