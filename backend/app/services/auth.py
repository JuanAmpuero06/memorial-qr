"""
Servicio de autenticación - Lógica de negocio
"""
from datetime import timedelta
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.repositories import UserRepository
from app.core.security import verify_password, create_access_token
from app.config import settings


class AuthService:
    """Servicio de autenticación"""
    
    @staticmethod
    def authenticate_user(db: Session, email: str, password: str):
        """
        Autenticar usuario con email y contraseña
        
        Args:
            db: Sesión de base de datos
            email: Email del usuario
            password: Contraseña en texto plano
            
        Returns:
            Usuario autenticado
            
        Raises:
            HTTPException: Si las credenciales son inválidas
        """
        user = UserRepository.get_by_email(db, email=email)
        
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email o contraseña incorrectos",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return user
    
    @staticmethod
    def create_token(email: str) -> str:
        """
        Crear token de acceso
        
        Args:
            email: Email del usuario
            
        Returns:
            Token JWT
        """
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": email}, 
            expires_delta=access_token_expires
        )
        return access_token
