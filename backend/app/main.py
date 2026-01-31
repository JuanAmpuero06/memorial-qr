"""
Aplicación principal de Memorial QR API
Arquitectura limpia con separación de responsabilidades
"""
import os
from fastapi import FastAPI, Depends, File, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session
from typing import List

from app.config import settings
from app.db import Base, engine, get_db
from app.api.v1 import api_router
from app.models import User
from app.schemas import MemorialCreate, MemorialResponse, PublicMemorial
from app.api.deps import get_current_user
from app.services import MemorialService, QRService


# Crear tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Inicializar aplicación
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configurar directorio de archivos estáticos
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
app.mount("/static", StaticFiles(directory=settings.UPLOAD_DIR), name="static")

# Incluir routers de la API v1
app.include_router(api_router, prefix="/api/v1")


# ===== Endpoints de utilidad =====
@app.get("/")
async def root():
    """Endpoint raíz"""
    return {
        "message": "Memorial QR API",
        "version": settings.APP_VERSION,
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint
    Verifica el estado de la aplicación y la base de datos
    """
    db = next(get_db())
    try:
        db.execute(text("SELECT 1"))
        return {
            "status": "healthy",
            "database": "connected",
            "message": "Todo correcto 🚀"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e)
        }
    finally:
        db.close()


# ===== Endpoints legacy (compatibilidad con frontend actual) =====
from app.api.v1.endpoints import auth, users

# Rutas de autenticación sin prefijo para compatibilidad
app.include_router(auth.router, tags=["auth (legacy)"])

# Rutas de usuarios con prefijo
app.include_router(users.router, prefix="/users", tags=["users (legacy)"])

# Rutas de memorials - manteniendo compatibilidad con frontend
@app.post("/memorials/", response_model=MemorialResponse, status_code=201, tags=["memorials (legacy)"])
async def create_memorial_legacy(
    memorial: MemorialCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Crear memorial (endpoint legacy)"""
    return MemorialService.create_memorial(db, memorial, current_user.id)


@app.get("/memorials/", response_model=List[MemorialResponse], tags=["memorials (legacy)"])
async def get_memorials_legacy(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Obtener memoriales del usuario (endpoint legacy)"""
    return MemorialService.get_user_memorials(db, current_user.id)


@app.get("/public/memorials/{slug}", response_model=PublicMemorial, tags=["memorials (legacy)"])
async def get_public_memorial_legacy(slug: str, db: Session = Depends(get_db)):
    """Obtener memorial público (endpoint legacy)"""
    return MemorialService.get_public_memorial(db, slug)


@app.get("/memorials/{slug}/qr", tags=["memorials (legacy)"])
async def get_qr_legacy(slug: str, current_user: User = Depends(get_current_user)):
    """Generar QR (endpoint legacy)"""
    return QRService.generate_qr(slug)


@app.post("/memorials/{memorial_id}/upload-photo", response_model=MemorialResponse, tags=["memorials (legacy)"])
async def upload_photo_legacy(
    memorial_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Subir foto (endpoint legacy)"""
    return await MemorialService.upload_photo(db, memorial_id, file, current_user)

