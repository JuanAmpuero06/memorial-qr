"""
Router principal de la API v1
"""
from fastapi import APIRouter
from app.api.v1.endpoints import auth, users, memorials, analytics


api_router = APIRouter()

# Incluir routers de cada módulo
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(memorials.router, prefix="/memorials", tags=["memorials"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
