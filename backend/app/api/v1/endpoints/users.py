"""
Endpoints de usuarios
"""
from fastapi import APIRouter, Depends
from app.models import User
from app.schemas import UserResponse
from app.api.deps import get_current_user


router = APIRouter()


@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_user)):
    """
    Obtener información del usuario actual
    
    Args:
        current_user: Usuario autenticado
        
    Returns:
        Datos del usuario
    """
    return current_user
