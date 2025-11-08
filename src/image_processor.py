"""
Procesamiento de imágenes para facturas
"""

from PIL import Image
import pdf2image
import numpy as np
from typing import Union, Tuple
from pathlib import Path


class ImageProcessor:
    """Clase para procesar imágenes de facturas"""

    def __init__(self, dpi: int = 200):
        """
        Inicializa el procesador de imágenes.

        Args:
            dpi: DPI para convertir PDFs a imágenes (default: 200)
        """
        self.dpi = dpi

    def load_image(self, image_path: str) -> Image.Image:
        """
        Carga una imagen desde un archivo (PDF, JPG, PNG).

        Args:
            image_path: Ruta al archivo de imagen

        Returns:
            Objeto PIL.Image
        """
        path = Path(image_path)
        extension = path.suffix.lower()

        if extension == '.pdf':
            return self._load_pdf(image_path)
        elif extension in ['.jpg', '.jpeg', '.png']:
            return Image.open(image_path).convert('RGB')
        else:
            raise ValueError(f"Formato no soportado: {extension}")

    def _load_pdf(self, pdf_path: str) -> Image.Image:
        """
        Convierte la primera página de un PDF a imagen.

        Args:
            pdf_path: Ruta al archivo PDF

        Returns:
            Objeto PIL.Image
        """
        images = pdf2image.convert_from_path(pdf_path, dpi=self.dpi)
        return images[0]  # Solo la primera página

    def save_image(self, image: Image.Image, output_path: str) -> None:
        """
        Guarda una imagen en formato PNG o PDF.

        Args:
            image: Imagen PIL a guardar
            output_path: Ruta donde guardar la imagen
        """
        extension = Path(output_path).suffix.lower()

        if extension == '.pdf':
            image.save(output_path, 'PDF', resolution=self.dpi)
        elif extension == '.png':
            image.save(output_path, 'PNG')
        else:
            # Por defecto guardar como PNG
            image.save(output_path, 'PNG')

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
