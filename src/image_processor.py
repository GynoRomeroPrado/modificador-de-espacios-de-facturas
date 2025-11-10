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
        Aplica un desplazamiento (shift) a una imagen AUMENTANDO el canvas.

        IMPORTANTE: Este método NO recorta contenido. En lugar de eso,
        aumenta el tamaño del canvas para agregar márgenes blancos.
        TODO el contenido original permanece visible.

        Args:
            image: Imagen original
            shift_x: Desplazamiento horizontal en píxeles (+ = derecha, - = izquierda)
            shift_y: Desplazamiento vertical en píxeles (+ = abajo, - = arriba)
            fill_color: Color de relleno para márgenes (default: blanco)

        Returns:
            Nueva imagen con canvas aumentado y contenido desplazado

        Ejemplos:
            shift_x=10, shift_y=0:  Agrega 10px de margen a la IZQUIERDA
            shift_x=-10, shift_y=0: Agrega 10px de margen a la DERECHA
            shift_x=0, shift_y=10:  Agrega 10px de margen ARRIBA
            shift_x=0, shift_y=-10: Agrega 10px de margen ABAJO
            shift_x=10, shift_y=10: Agrega 10px de margen IZQUIERDA + ARRIBA
        """
        # Calcular nuevo tamaño del canvas (aumenta para acomodar el desplazamiento)
        # El canvas crece en la dirección opuesta al desplazamiento
        new_width = image.width + abs(shift_x)
        new_height = image.height + abs(shift_y)

        # Crear nueva imagen con canvas más grande
        shifted_image = Image.new('RGB', (new_width, new_height), fill_color)

        # Calcular posición donde pegar el contenido original (SIN RECORTAR)
        # Si shift_x > 0: contenido se mueve a la derecha, margen queda a la izquierda
        # Si shift_x < 0: contenido queda a la izquierda, margen queda a la derecha
        # Si shift_y > 0: contenido se mueve abajo, margen queda arriba
        # Si shift_y < 0: contenido queda arriba, margen queda abajo
        paste_x = shift_x if shift_x > 0 else 0
        paste_y = shift_y if shift_y > 0 else 0

        # Pegar TODA la imagen original sin recortar NADA
        shifted_image.paste(image, (paste_x, paste_y))

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
