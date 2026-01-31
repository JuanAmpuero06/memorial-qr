"""
Repositorio de usuarios - Capa de acceso a datos
"""
from typing import Optional
from sqlalchemy.orm import Session
from app.models import User
from app.schemas import UserCreate
from app.core.security import get_password_hash


class UserRepository:
    """Repositorio para operaciones de base de datos de usuarios"""
    
    @staticmethod
    def get_by_id(db: Session, user_id: int) -> Optional[User]:
        """Obtener usuario por ID"""
        return db.query(User).filter(User.id == user_id).first()
    
    @staticmethod
    def get_by_email(db: Session, email: str) -> Optional[User]:
        """Obtener usuario por email"""
        return db.query(User).filter(User.email == email).first()
    
    @staticmethod
    def create(db: Session, user: UserCreate) -> User:
        """Crear nuevo usuario"""
        hashed_password = get_password_hash(user.password)
        db_user = User(
            email=user.email,
            hashed_password=hashed_password
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    
    @staticmethod
    def exists_by_email(db: Session, email: str) -> bool:
        """Verificar si existe un usuario con el email"""
        return db.query(User).filter(User.email == email).first() is not None
