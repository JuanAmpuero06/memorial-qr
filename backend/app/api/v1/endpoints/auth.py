"""
Endpoints de autenticación
"""
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.db import get_db
from app.schemas import Token, UserCreate, UserResponse
from app.services import AuthService
from app.repositories import UserRepository


router = APIRouter()


@router.post("/token", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Endpoint de login - Obtener token de acceso
    
    Args:
        form_data: Datos del formulario (username/password)
        db: Sesión de base de datos
        
    Returns:
        Token de acceso
    """
    user = AuthService.authenticate_user(db, form_data.username, form_data.password)
    access_token = AuthService.create_token(user.email)
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register", response_model=UserResponse, status_code=201)
async def register(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    """
    Endpoint de registro - Crear nuevo usuario
    
    Args:
        user: Datos del usuario
        db: Sesión de base de datos
        
    Returns:
        Usuario creado
        
    Raises:
        HTTPException: Si el email ya está registrado
    """
    if UserRepository.exists_by_email(db, user.email):
        raise HTTPException(status_code=400, detail="El email ya está registrado")
    
    return UserRepository.create(db, user)
