"""
Servicio de Geolocalización - Resolución de IP a ubicación
"""
import httpx
from typing import Optional, Dict
from dataclasses import dataclass


@dataclass
class GeoLocation:
    """Resultado de geolocalización"""
    country: Optional[str] = None
    country_code: Optional[str] = None
    city: Optional[str] = None
    region: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class GeoService:
    """Servicio de geolocalización usando APIs gratuitas"""
    
    # APIs gratuitas de geolocalización (sin API key)
    PROVIDERS = [
        "https://ipapi.co/{ip}/json/",
        "http://ip-api.com/json/{ip}",
    ]
    
    @staticmethod
    async def get_location(ip_address: str) -> GeoLocation:
        """
        Obtener ubicación geográfica de una IP
        
        Args:
            ip_address: Dirección IP a geolocalizar
            
        Returns:
            Datos de geolocalización
        """
        # No geolocalizar IPs locales
        if GeoService._is_local_ip(ip_address):
            return GeoLocation()
        
        # Intentar con cada proveedor
        for provider_url in GeoService.PROVIDERS:
            try:
                location = await GeoService._query_provider(
                    provider_url.format(ip=ip_address)
                )
                if location.country:
                    return location
            except Exception as e:
                print(f"Error con proveedor {provider_url}: {e}")
                continue
        
        return GeoLocation()
    
    @staticmethod
    async def _query_provider(url: str) -> GeoLocation:
        """Consultar un proveedor de geolocalización"""
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
            
            # Normalizar respuesta según el proveedor
            return GeoService._normalize_response(data, url)
    
    @staticmethod
    def _normalize_response(data: Dict, url: str) -> GeoLocation:
        """Normalizar respuesta de diferentes proveedores"""
        
        # ipapi.co
        if "ipapi.co" in url:
            return GeoLocation(
                country=data.get("country_name"),
                country_code=data.get("country_code"),
                city=data.get("city"),
                region=data.get("region"),
                latitude=data.get("latitude"),
                longitude=data.get("longitude")
            )
        
        # ip-api.com
        if "ip-api.com" in url:
            return GeoLocation(
                country=data.get("country"),
                country_code=data.get("countryCode"),
                city=data.get("city"),
                region=data.get("regionName"),
                latitude=data.get("lat"),
                longitude=data.get("lon")
            )
        
        return GeoLocation()
    
    @staticmethod
    def _is_local_ip(ip: str) -> bool:
        """Verificar si es una IP local/privada"""
        if not ip:
            return True
        
        local_prefixes = [
            "127.",
            "10.",
            "172.16.", "172.17.", "172.18.", "172.19.",
            "172.20.", "172.21.", "172.22.", "172.23.",
            "172.24.", "172.25.", "172.26.", "172.27.",
            "172.28.", "172.29.", "172.30.", "172.31.",
            "192.168.",
            "::1",
            "localhost"
        ]
        
        return any(ip.startswith(prefix) for prefix in local_prefixes)
    
    @staticmethod
    def get_location_sync(ip_address: str) -> GeoLocation:
        """
        Versión síncrona de get_location (para uso en contextos no-async)
        
        Args:
            ip_address: Dirección IP
            
        Returns:
            Datos de geolocalización
        """
        import asyncio
        
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # Si ya hay un loop corriendo, crear una tarea
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(
                        asyncio.run, 
                        GeoService.get_location(ip_address)
                    )
                    return future.result(timeout=10)
            else:
                return loop.run_until_complete(GeoService.get_location(ip_address))
        except Exception as e:
            print(f"Error en geolocalización sync: {e}")
            return GeoLocation()
