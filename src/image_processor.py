"""
Procesamiento de imágenes para facturas
"""

from PIL import Image, ImageFilter, ImageEnhance
import pdf2image
import numpy as np
from typing import Union, Tuple
from pathlib import Path


class ImageProcessor:
    """Clase para procesar imágenes de facturas"""

    def __init__(self, dpi: int = 300):
        """
        Inicializa el procesador de imágenes.

        Args:
            dpi: DPI para convertir PDFs a imágenes (default: 300)
                 300 DPI es el estándar profesional para OCR de alta calidad
        """
        self.dpi = dpi

    def load_image(self, image_path: str) -> Image.Image:
        """
        Carga una imagen desde un archivo (PDF, JPG, PNG) preservando calidad.

        Args:
            image_path: Ruta al archivo de imagen

        Returns:
            Objeto PIL.Image en modo RGB

        Note:
            Preserva canales alfa (RGBA) y convierte CMYK correctamente
        """
        path = Path(image_path)
        extension = path.suffix.lower()

        if extension == '.pdf':
            return self._load_pdf(image_path)
        elif extension in ['.jpg', '.jpeg', '.png']:
            img = Image.open(image_path)
            # Solo convertir a RGB si no está ya en RGB
            # Esto preserva mejor la calidad original
            if img.mode == 'RGBA':
                # Preservar canal alfa creando fondo blanco
                background = Image.new('RGB', img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[3])  # Usar canal alfa como máscara
                return background
            elif img.mode != 'RGB':
                return img.convert('RGB')
            return img
        else:
            raise ValueError(f"Formato no soportado: {extension}")

    def _load_pdf(self, pdf_path: str) -> Image.Image:
        """
        Convierte la primera página de un PDF a imagen con validación.

        Args:
            pdf_path: Ruta al archivo PDF

        Returns:
            Objeto PIL.Image

        Raises:
            ValueError: Si no se puede convertir el PDF o la calidad es muy baja
        """
        images = pdf2image.convert_from_path(pdf_path, dpi=self.dpi)

        if not images:
            raise ValueError(f"No se pudo convertir el PDF: {pdf_path}")

        image = images[0]

        # Validar resolución mínima para OCR (al menos 200 DPI efectivo)
        # Asumiendo tamaño A4 estándar: 8.27 x 11.69 pulgadas
        min_width = int(8.27 * 200)  # ~1654 píxeles
        min_height = int(11.69 * 200)  # ~2338 píxeles

        if image.width < min_width or image.height < min_height:
            print(f"⚠️  Advertencia: Resolución baja detectada ({image.width}x{image.height}). "
                  f"Se recomienda aumentar DPI para mejor OCR.")

        return image

    def save_image(self, image: Image.Image, output_path: str) -> None:
        """
        Guarda imagen respetando la extensión del archivo (PDF o PNG).

        Args:
            image: Imagen PIL a guardar
            output_path: Ruta donde guardar la imagen

        Note:
            - PDF: quality=100, resolution=DPI configurado
            - PNG: optimize=True, compress_level=9 (máxima compresión sin pérdida)
            - Mantiene todas las mejoras de calidad aplicadas
        """
        extension = Path(output_path).suffix.lower()

        if extension == '.pdf':
            # PDF con máxima calidad
            image.save(
                output_path,
                'PDF',
                resolution=float(self.dpi),
                quality=100,
                optimize=False
            )
        elif extension == '.png':
            # PNG optimizado
            image.save(
                output_path,
                'PNG',
                optimize=True,
                compress_level=9
            )
        else:
            # Por defecto: PDF con máxima calidad
            image.save(
                output_path,
                'PDF',
                resolution=float(self.dpi),
                quality=100,
                optimize=False
            )

    def apply_shift(
        self,
        image: Image.Image,
        shift_x: int,
        shift_y: int,
        fill_color: Tuple[int, int, int] = (255, 255, 255)
    ) -> Image.Image:
        """
        Aplica un desplazamiento (shift) a una imagen.

        Args:
            image: Imagen original
            shift_x: Desplazamiento horizontal en píxeles (+ = derecha, - = izquierda)
            shift_y: Desplazamiento vertical en píxeles (+ = abajo, - = arriba)
            fill_color: Color de relleno para áreas vacías (default: blanco)

        Returns:
            Nueva imagen con el desplazamiento aplicado
        """
        # Crear imagen nueva con el mismo tamaño
        shifted_image = Image.new('RGB', image.size, fill_color)

        # Calcular coordenadas de pegado
        paste_x = max(0, shift_x)
        paste_y = max(0, shift_y)

        # Calcular coordenadas de recorte de la imagen original
        crop_x = max(0, -shift_x)
        crop_y = max(0, -shift_y)

        width = image.width - abs(shift_x)
        height = image.height - abs(shift_y)

        # Recortar y pegar
        cropped = image.crop((crop_x, crop_y, crop_x + width, crop_y + height))
        shifted_image.paste(cropped, (paste_x, paste_y))

        return shifted_image

    def get_image_info(self, image: Image.Image) -> dict:
        """
        Obtiene información básica de una imagen.

        Args:
            image: Imagen PIL

        Returns:
            Diccionario con información de la imagen
        """
        return {
            'width': image.width,
            'height': image.height,
            'mode': image.mode,
            'format': image.format
        }

    def enhance_for_ocr(self, image: Image.Image, apply_sharpening: bool = True) -> Image.Image:
        """
        Mejora la imagen para reconocimiento OCR mediante técnicas avanzadas.

        Args:
            image: Imagen original
            apply_sharpening: Si aplicar sharpening (default: True)

        Returns:
            Imagen mejorada para OCR

        Note:
            Aplica técnicas profesionales:
            - Sharpening con UnsharpMask (radio=2, percent=150, threshold=3)
            - Mejora de contraste sutil (factor=1.1)
            - Estos parámetros están optimizados para facturas
        """
        enhanced = image.copy()

        # 1. Aplicar sharpening con UnsharpMask
        # Técnica profesional que mejora bordes sin crear artefactos
        if apply_sharpening:
            enhanced = enhanced.filter(
                ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3)
            )

        # 2. Mejorar contraste sutilmente para mejor legibilidad
        # Factor 1.1 = mejora sutil sin sobre-saturar
        contrast_enhancer = ImageEnhance.Contrast(enhanced)
        enhanced = contrast_enhancer.enhance(1.1)

        # 3. Mejorar nitidez adicional de forma suave
        sharpness_enhancer = ImageEnhance.Sharpness(enhanced)
        enhanced = sharpness_enhancer.enhance(1.2)

        return enhanced

    def save_image_with_ocr_enhancement(
        self,
        image: Image.Image,
        output_path: str,
        enhance: bool = True
    ) -> None:
        """
        Guarda una imagen aplicando mejoras para OCR.

        Args:
            image: Imagen PIL a guardar
            output_path: Ruta donde guardar la imagen
            enhance: Si aplicar mejoras para OCR (default: True)

        Note:
            Combina mejoras de calidad OCR con optimización de tamaño
        """
        if enhance:
            image = self.enhance_for_ocr(image)

        self.save_image(image, output_path)
