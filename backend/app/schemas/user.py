"""
Schemas de Usuario
"""
from pydantic import BaseModel, EmailStr
from datetime import datetime


class UserBase(BaseModel):
    """Schema base de usuario"""
    email: EmailStr


class UserCreate(UserBase):
    """Schema para crear usuario"""
    password: str


class UserResponse(UserBase):
    """Schema de respuesta de usuario"""
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True
