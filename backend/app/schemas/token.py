"""
Schemas de Token
"""
from pydantic import BaseModel


class Token(BaseModel):
    """Schema de respuesta de token"""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Schema de datos del token"""
    email: str | None = None
