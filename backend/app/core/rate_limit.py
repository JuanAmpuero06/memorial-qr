"""
Configuración de Rate Limiting con SlowAPI
Protección contra abuso de la API
"""
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from fastapi import Request
from fastapi.responses import JSONResponse


def get_real_ip(request: Request) -> str:
    """
    Obtiene la IP real del cliente, considerando proxies (Traefik)
    Revisa headers X-Forwarded-For y X-Real-IP
    """
    # Traefik añade X-Forwarded-For
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        # El primer valor es la IP original del cliente
        return forwarded.split(",")[0].strip()
    
    # Fallback a X-Real-IP
    real_ip = request.headers.get("X-Real-IP")
    if real_ip:
        return real_ip
    
    # Último recurso: IP directa
    return get_remote_address(request)


# Inicializar el limiter con función de obtención de IP
limiter = Limiter(key_func=get_real_ip)


async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    """
    Handler personalizado para cuando se excede el rate limit
    Devuelve un JSON con información útil
    """
    return JSONResponse(
        status_code=429,
        content={
            "error": "rate_limit_exceeded",
            "message": "Has excedido el límite de peticiones. Por favor espera un momento.",
            "detail": str(exc.detail),
            "retry_after": exc.detail.split("per")[1].strip() if "per" in str(exc.detail) else "1 minute"
        },
        headers={"Retry-After": "60"}
    )


# Límites predefinidos para diferentes tipos de endpoints
class RateLimits:
    """
    Límites de rate limiting para diferentes tipos de endpoints
    Formato: "número/período" (second, minute, hour, day)
    """
    # Autenticación - muy estricto para prevenir fuerza bruta
    LOGIN = "5/minute"
    REGISTER = "3/minute"
    
    # Endpoints públicos - moderado
    PUBLIC_READ = "30/minute"
    PUBLIC_WRITE = "10/minute"  # Condolencias, reacciones
    
    # Endpoints autenticados - más permisivo
    AUTHENTICATED_READ = "60/minute"
    AUTHENTICATED_WRITE = "30/minute"
    
    # Uploads - muy limitado
    UPLOAD = "10/minute"
    
    # Analytics - moderado
    ANALYTICS = "20/minute"
