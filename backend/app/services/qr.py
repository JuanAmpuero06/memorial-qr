"""
Servicio de generación de QR - Lógica de negocio
Con soporte para QR personalizado con foto integrada
"""
import os
import qrcode
from io import BytesIO
from PIL import Image
from fastapi.responses import StreamingResponse
from app.config import settings


class QRService:
    """Servicio de generación de códigos QR"""
    
    @staticmethod
    def generate_qr(slug: str, with_photo: bool = False, image_filename: str = None) -> StreamingResponse:
        """
        Generar código QR para un memorial
        
        Args:
            slug: Slug del memorial
            with_photo: Si incluir la foto del fallecido en el centro del QR
            image_filename: Nombre del archivo de imagen para incrustar
            
        Returns:
            Imagen QR como StreamingResponse
        """
        # Construir URL
        target_url = f"{settings.FRONTEND_URL}/view/{slug}"
        
        # Generar QR con alta corrección de errores para permitir logo
        qr = qrcode.QRCode(
            version=4,
            error_correction=qrcode.constants.ERROR_CORRECT_H,  # 30% corrección
            box_size=10,
            border=4,
        )
        qr.add_data(target_url)
        qr.make(fit=True)
        
        # Crear imagen QR
        qr_img = qr.make_image(fill_color="#1e293b", back_color="white").convert('RGBA')
        
        # Si se solicita con foto y existe la imagen
        if with_photo and image_filename:
            qr_img = QRService._add_photo_to_qr(qr_img, image_filename)
        
        # Agregar marco decorativo
        qr_img = QRService._add_decorative_frame(qr_img, slug)
        
        # Convertir a bytes
        img_byte_arr = BytesIO()
        qr_img.save(img_byte_arr, format='PNG', quality=95)
        img_byte_arr.seek(0)
        
        return StreamingResponse(img_byte_arr, media_type="image/png")
    
    @staticmethod
    def _add_photo_to_qr(qr_img: Image.Image, image_filename: str) -> Image.Image:
        """
        Agregar foto circular al centro del QR
        
        Args:
            qr_img: Imagen QR base
            image_filename: Nombre del archivo de foto
            
        Returns:
            Imagen QR con foto incrustada
        """
        try:
            # Ruta de la imagen
            image_path = os.path.join(settings.UPLOAD_DIR, image_filename)
            
            if not os.path.exists(image_path):
                return qr_img
            
            # Abrir y procesar la foto
            photo = Image.open(image_path).convert('RGBA')
            
            # Calcular tamaño del logo (25% del QR para mantener legibilidad)
            qr_width, qr_height = qr_img.size
            logo_size = int(qr_width * 0.25)
            
            # Redimensionar foto
            photo = photo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
            
            # Crear máscara circular
            mask = Image.new('L', (logo_size, logo_size), 0)
            from PIL import ImageDraw
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0, logo_size, logo_size), fill=255)
            
            # Crear imagen circular con borde
            circular_photo = Image.new('RGBA', (logo_size + 8, logo_size + 8), (255, 255, 255, 255))
            
            # Agregar borde decorativo
            border_draw = ImageDraw.Draw(circular_photo)
            border_draw.ellipse((0, 0, logo_size + 7, logo_size + 7), fill=(30, 41, 59, 255))  # slate-800
            border_draw.ellipse((3, 3, logo_size + 4, logo_size + 4), fill=(255, 255, 255, 255))
            
            # Aplicar máscara circular a la foto
            output = Image.new('RGBA', (logo_size, logo_size), (0, 0, 0, 0))
            output.paste(photo, mask=mask)
            
            # Pegar foto en el centro del borde
            circular_photo.paste(output, (4, 4), output)
            
            # Calcular posición central
            pos_x = (qr_width - circular_photo.size[0]) // 2
            pos_y = (qr_height - circular_photo.size[1]) // 2
            
            # Crear fondo blanco detrás del logo para mejor contraste
            white_bg = Image.new('RGBA', circular_photo.size, (255, 255, 255, 255))
            qr_img.paste(white_bg, (pos_x, pos_y))
            qr_img.paste(circular_photo, (pos_x, pos_y), circular_photo)
            
            return qr_img
            
        except Exception as e:
            print(f"Error al agregar foto al QR: {e}")
            return qr_img
    
    @staticmethod
    def _add_decorative_frame(qr_img: Image.Image, slug: str) -> Image.Image:
        """
        Agregar marco decorativo y texto al QR
        
        Args:
            qr_img: Imagen QR
            slug: Slug del memorial para mostrar
            
        Returns:
            Imagen QR con marco decorativo
        """
        from PIL import ImageDraw, ImageFont
        
        qr_width, qr_height = qr_img.size
        
        # Crear canvas más grande para el marco
        padding = 40
        bottom_padding = 60
        new_width = qr_width + (padding * 2)
        new_height = qr_height + padding + bottom_padding
        
        # Crear nueva imagen con fondo
        framed = Image.new('RGBA', (new_width, new_height), (255, 255, 255, 255))
        
        # Pegar QR
        framed.paste(qr_img, (padding, padding), qr_img)
        
        draw = ImageDraw.Draw(framed)
        
        # Línea decorativa superior
        draw.line([(20, 15), (new_width - 20, 15)], fill=(217, 119, 6, 255), width=2)
        
        # Línea decorativa inferior
        draw.line([(20, new_height - 45), (new_width - 20, new_height - 45)], 
                  fill=(217, 119, 6, 255), width=2)
        
        # Texto "Memorial QR" en la parte inferior
        try:
            # Intentar usar fuente del sistema
            font = ImageFont.truetype("arial.ttf", 16)
            small_font = ImageFont.truetype("arial.ttf", 12)
        except:
            font = ImageFont.load_default()
            small_font = font
        
        # Texto centrado
        text = "✦ Memorial QR ✦"
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_x = (new_width - text_width) // 2
        draw.text((text_x, new_height - 35), text, fill=(30, 41, 59, 255), font=font)
        
        # Esquinas decorativas
        corner_size = 15
        corner_color = (217, 119, 6, 255)  # amber-600
        
        # Esquina superior izquierda
        draw.line([(10, 10), (10, 10 + corner_size)], fill=corner_color, width=3)
        draw.line([(10, 10), (10 + corner_size, 10)], fill=corner_color, width=3)
        
        # Esquina superior derecha
        draw.line([(new_width - 10, 10), (new_width - 10, 10 + corner_size)], fill=corner_color, width=3)
        draw.line([(new_width - 10, 10), (new_width - 10 - corner_size, 10)], fill=corner_color, width=3)
        
        # Esquina inferior izquierda
        draw.line([(10, new_height - 50), (10, new_height - 50 - corner_size)], fill=corner_color, width=3)
        draw.line([(10, new_height - 50), (10 + corner_size, new_height - 50)], fill=corner_color, width=3)
        
        # Esquina inferior derecha
        draw.line([(new_width - 10, new_height - 50), (new_width - 10, new_height - 50 - corner_size)], fill=corner_color, width=3)
        draw.line([(new_width - 10, new_height - 50), (new_width - 10 - corner_size, new_height - 50)], fill=corner_color, width=3)
        
        return framed
    
    @staticmethod
    def generate_qr_simple(slug: str) -> StreamingResponse:
        """
        Generar código QR simple sin decoraciones
        
        Args:
            slug: Slug del memorial
            
        Returns:
            Imagen QR como StreamingResponse
        """
        target_url = f"{settings.FRONTEND_URL}/view/{slug}"
        
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=10,
            border=4,
        )
        qr.add_data(target_url)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        img_byte_arr = BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        
        return StreamingResponse(img_byte_arr, media_type="image/png")
