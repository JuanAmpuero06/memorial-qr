"""
Configuración centralizada de la aplicación
"""
import os
from typing import List


class Settings:
    """Configuración de la aplicación"""
    
    # General
    APP_NAME: str = "Memorial QR API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Database - Lee directamente del .env
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/dbname")
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
    ]
    
    # File Upload
    UPLOAD_DIR: str = "uploaded_images"
    MAX_UPLOAD_SIZE: int = 5 * 1024 * 1024  # 5MB
    
    # URLs
    BACKEND_URL: str = os.getenv("BACKEND_URL", "http://localhost:8000")
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:5173")


settings = Settings()

