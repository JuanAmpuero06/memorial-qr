from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List

# --- ESQUEMAS DE MEMORIAL (Básico por ahora) ---
class MemorialBase(BaseModel):
    name: str
    epitaph: Optional[str] = None

class Memorial(MemorialBase):
    id: int
    slug: str
    owner_id: int
    class Config:
        from_attributes = True

# --- ESQUEMAS DE USUARIO ---

# Lo que recibimos cuando alguien se registra
class UserCreate(BaseModel):
    email: EmailStr
    password: str

# Lo que devolvemos al frontend (¡SIN PASSWORD!)
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    is_active: bool
    created_at: datetime
    # memorials: List[Memorial] = [] # Descomentar luego cuando tengamos memoriales

    class Config:
        # Esto permite que Pydantic lea datos de objetos SQLAlchemy
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str