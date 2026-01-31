"""
Endpoints de Galería Multimedia
"""
from typing import Optional
from fastapi import APIRouter, Depends, File, UploadFile, Form
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import User
from app.schemas import (
    MediaItemCreate, MediaItemUpdate, 
    MediaItemResponse, GalleryResponse
)
from app.services import GalleryService
from app.api.deps import get_current_user


router = APIRouter()


# ============ ENDPOINTS PÚBLICOS ============

@router.get("/public/{slug}", response_model=GalleryResponse)
async def get_public_gallery(
    slug: str,
    db: Session = Depends(get_db)
):
    """
    Obtener galería de un memorial (público)
    
    Args:
        slug: Slug del memorial
        
    Returns:
        Galería con elementos multimedia
    """
    return GalleryService.get_gallery(db, slug)


# ============ ENDPOINTS AUTENTICADOS ============

@router.post("/{memorial_id}", response_model=MediaItemResponse, status_code=201)
async def upload_media(
    memorial_id: int,
    file: UploadFile = File(...),
    title: Optional[str] = Form(None),
    caption: Optional[str] = Form(None),
    taken_at: Optional[str] = Form(None),
    location: Optional[str] = Form(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Subir archivo multimedia a la galería
    
    Args:
        memorial_id: ID del memorial
        file: Archivo a subir (imagen o video)
        title: Título opcional
        caption: Descripción opcional
        taken_at: Fecha en que se tomó
        location: Lugar donde se tomó
        
    Returns:
        Elemento multimedia creado
    """
    metadata = MediaItemCreate(
        title=title,
        caption=caption,
        taken_at=taken_at,
        location=location
    )
    
    return await GalleryService.upload_media(
        db, memorial_id, file, current_user.id, metadata
    )


@router.put("/{item_id}", response_model=MediaItemResponse)
async def update_media_item(
    item_id: int,
    update_data: MediaItemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Actualizar metadatos de elemento multimedia
    
    Args:
        item_id: ID del elemento
        update_data: Datos de actualización
        
    Returns:
        Elemento actualizado
    """
    return GalleryService.update_media_item(
        db, item_id, current_user.id, update_data
    )


@router.delete("/{item_id}")
async def delete_media_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Eliminar elemento de galería
    
    Args:
        item_id: ID del elemento
        
    Returns:
        Confirmación de eliminación
    """
    GalleryService.delete_media_item(db, item_id, current_user.id)
    return {"message": "Elemento eliminado"}
