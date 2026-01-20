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

# Lo que el usuario nos envía para crear
class MemorialCreate(BaseModel):
    name: str
    epitaph: Optional[str] = None
    bio: Optional[str] = None
    birth_date: Optional[str] = None # Podrías usar date, pero string es más fácil por ahora
    death_date: Optional[str] = None

# Lo que nosotros devolvemos (incluyendo el ID y el Slug generado)
class MemorialResponse(MemorialCreate):
    id: int
    slug: str
    owner_id: int
    created_at: datetime
    
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
    
# --- ESQUEMA PÚBLICO (Lo que ve la gente en el cementerio) ---
class PublicMemorial(BaseModel):
    name: str
    epitaph: Optional[str] = None
    bio: Optional[str] = None
    # birth_date: ... (puedes agregarlo si quieres)
    # death_date: ...
    
    class Config:
        from_attributes = True

