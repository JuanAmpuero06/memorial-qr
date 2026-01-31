"""
Servicio de generación de QR - Lógica de negocio
"""
import qrcode
from io import BytesIO
from fastapi.responses import StreamingResponse
from app.config import settings


class QRService:
    """Servicio de generación de códigos QR"""
    
    @staticmethod
    def generate_qr(slug: str) -> StreamingResponse:
        """
        Generar código QR para un memorial
        
        Args:
            slug: Slug del memorial
            
        Returns:
            Imagen QR como StreamingResponse
        """
        # Construir URL
        target_url = f"{settings.FRONTEND_URL}/view/{slug}"
        
        # Generar QR
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(target_url)
        qr.make(fit=True)
        
        # Crear imagen
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convertir a bytes
        img_byte_arr = BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        
        return StreamingResponse(img_byte_arr, media_type="image/png")
