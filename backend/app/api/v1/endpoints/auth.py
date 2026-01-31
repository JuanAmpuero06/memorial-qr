"""
Endpoints de autenticación
"""
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.db import get_db
from app.schemas import Token, UserCreate, UserResponse
from app.services import AuthService
from app.repositories import UserRepository
from app.core.rate_limit import limiter, RateLimits


router = APIRouter()


@router.post("/token", response_model=Token)
@limiter.limit(RateLimits.LOGIN)
async def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Endpoint de login - Obtener token de acceso
    Rate limit: 5 intentos por minuto (protección contra fuerza bruta)
    
    Args:
        request: Request object (requerido para rate limiting)
        form_data: Datos del formulario (username/password)
        db: Sesión de base de datos
        
    Returns:
        Token de acceso
    """
    user = AuthService.authenticate_user(db, form_data.username, form_data.password)
    access_token = AuthService.create_token(user.email)
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register", response_model=UserResponse, status_code=201)
@limiter.limit(RateLimits.REGISTER)
async def register(
    request: Request,
    user: UserCreate,
    db: Session = Depends(get_db)
):
    """
    Endpoint de registro - Crear nuevo usuario
    Rate limit: 3 registros por minuto (prevenir spam de cuentas)
    
    Args:
        request: Request object (requerido para rate limiting)
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
