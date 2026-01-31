"""
Router principal de la API v1
"""
from fastapi import APIRouter
from app.api.v1.endpoints import auth, users, memorials, analytics, condolences, timeline, gallery


api_router = APIRouter()

# Incluir routers de cada módulo
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(memorials.router, prefix="/memorials", tags=["memorials"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
api_router.include_router(condolences.router, prefix="/condolences", tags=["condolences"])
api_router.include_router(timeline.router, prefix="/timeline", tags=["timeline"])
api_router.include_router(gallery.router, prefix="/gallery", tags=["gallery"])
