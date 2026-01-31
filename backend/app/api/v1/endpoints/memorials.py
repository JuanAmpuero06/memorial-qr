"""
Endpoints de memoriales
"""
from typing import List
from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import User
from app.schemas import MemorialCreate, MemorialUpdate, MemorialResponse, PublicMemorial
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
    with_photo: bool = False,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Generar código QR para un memorial
    
    Args:
        slug: Slug del memorial
        with_photo: Si incluir la foto del fallecido en el QR
        current_user: Usuario autenticado
        
    Returns:
        Imagen QR (simple o con foto integrada)
    """
    from app.repositories import MemorialRepository
    
    # Obtener el memorial para verificar si tiene foto
    memorial = MemorialRepository.get_by_slug(db, slug)
    image_filename = memorial.image_filename if memorial else None
    
    return QRService.generate_qr(slug, with_photo=with_photo, image_filename=image_filename)


@router.get("/{slug}/qr-simple")
async def get_qr_code_simple(
    slug: str,
    current_user: User = Depends(get_current_user)
):
    """
    Generar código QR simple sin decoraciones
    
    Args:
        slug: Slug del memorial
        current_user: Usuario autenticado
        
    Returns:
        Imagen QR simple
    """
    return QRService.generate_qr_simple(slug)


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


@router.get("/{memorial_id}", response_model=MemorialResponse)
async def get_memorial(
    memorial_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Obtener un memorial específico por ID
    
    Args:
        memorial_id: ID del memorial
        db: Sesión de base de datos
        current_user: Usuario autenticado
        
    Returns:
        Memorial encontrado
    """
    return MemorialService.get_memorial_by_id(db, memorial_id, current_user)


@router.put("/{memorial_id}", response_model=MemorialResponse)
async def update_memorial(
    memorial_id: int,
    memorial_data: MemorialUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Actualizar un memorial existente
    
    Args:
        memorial_id: ID del memorial
        memorial_data: Datos a actualizar
        db: Sesión de base de datos
        current_user: Usuario autenticado
        
    Returns:
        Memorial actualizado
    """
    return MemorialService.update_memorial(db, memorial_id, memorial_data, current_user)


@router.delete("/{memorial_id}")
async def delete_memorial(
    memorial_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Eliminar un memorial
    
    Args:
        memorial_id: ID del memorial
        db: Sesión de base de datos
        current_user: Usuario autenticado
        
    Returns:
        Mensaje de confirmación
    """
    return MemorialService.delete_memorial(db, memorial_id, current_user)
