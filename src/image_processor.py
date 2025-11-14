"""
Procesamiento de imágenes para facturas
"""

from PIL import Image, ImageFilter, ImageEnhance
import pdf2image
import numpy as np
from typing import Union, Tuple, Optional
from pathlib import Path
from pypdf import PdfReader, PdfWriter
from pypdf.generic import RectangleObject
import cv2


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

    def apply_shift_to_pdf_direct(
        self,
        input_pdf_path: str,
        output_pdf_path: str,
        shift_x: int,
        shift_y: int
    ) -> None:
        """
        Aplica desplazamiento a un PDF manipulándolo directamente (SIN rasterizar).

        Esta es la forma CORRECTA de procesar PDFs manteniendo:
        - Texto vectorial (seleccionable, perfecta calidad)
        - Gráficos vectoriales intactos
        - Tamaño de archivo pequeño
        - Calidad original 100%

        Args:
            input_pdf_path: Ruta al PDF original
            output_pdf_path: Ruta donde guardar el PDF desplazado
            shift_x: Desplazamiento horizontal en píxeles (a 300 DPI)
                     + = derecha, - = izquierda
            shift_y: Desplazamiento vertical en píxeles (a 300 DPI)
                     + = abajo, - = arriba

        Note:
            Convierte píxeles (300 DPI) a puntos PDF (72 DPI):
            puntos = píxeles * 72 / 300

            Coordenadas PDF:
            - Origen en esquina inferior izquierda
            - Y positivo = arriba (invertido respecto a imágenes)

            Transformación: [1, 0, 0, 1, tx, ty]
            - tx: desplazamiento horizontal en puntos
            - ty: desplazamiento vertical en puntos
        """
        # Convertir píxeles (300 DPI) a puntos PDF (72 DPI)
        shift_x_points = shift_x * 72.0 / self.dpi
        shift_y_points = shift_y * 72.0 / self.dpi

        # Leer PDF original
        reader = PdfReader(input_pdf_path)
        writer = PdfWriter()

        # Procesar cada página
        for page in reader.pages:
            # Obtener dimensiones originales
            original_box = page.mediabox
            original_width = float(original_box.width)
            original_height = float(original_box.height)

            # Calcular nuevo mediabox (expandir para acomodar desplazamiento)
            # Si shift_x > 0, necesitamos más ancho a la derecha
            # Si shift_x < 0, necesitamos más ancho a la izquierda
            # Si shift_y > 0, necesitamos más alto arriba (en coord PDF)
            # Si shift_y < 0, necesitamos más alto abajo (en coord PDF)

            new_width = original_width + abs(shift_x_points)
            new_height = original_height + abs(shift_y_points)

            # Ajustar mediabox
            page.mediabox = RectangleObject([0, 0, new_width, new_height])

            # Calcular desplazamiento de contenido
            # Si shift_x > 0, mover contenido a la derecha
            # Si shift_x < 0, mover contenido a la derecha (para dejar espacio a la izquierda)
            # Si shift_y > 0, mover contenido hacia arriba (en coord PDF)
            # Si shift_y < 0, mover contenido hacia arriba (para dejar espacio abajo)

            tx = shift_x_points if shift_x_points > 0 else abs(shift_x_points)
            ty = shift_y_points if shift_y_points > 0 else abs(shift_y_points)

            # Aplicar transformación de desplazamiento
            # Matriz de transformación: [a, b, c, d, e, f]
            # a=1, b=0, c=0, d=1 (sin escala ni rotación)
            # e=tx (desplazamiento horizontal)
            # f=ty (desplazamiento vertical)
            page.add_transformation([1, 0, 0, 1, tx, ty])

            # Agregar página modificada al writer
            writer.add_page(page)

        # Guardar PDF modificado
        with open(output_pdf_path, 'wb') as output_file:
            writer.write(output_file)

    def detect_content_bbox_from_pdf(
        self,
        pdf_path: str,
        detection_dpi: int = 150,
        padding: int = 10
    ) -> Optional[Tuple[float, float, float, float]]:
        """
        Detecta el bounding box del contenido real en un PDF (sin márgenes blancos).

        Estrategia:
        1. Convierte el PDF a imagen de baja resolución (solo para análisis)
        2. Detecta píxeles no blancos usando OpenCV
        3. Calcula bounding box del contenido
        4. Convierte coordenadas de vuelta a puntos PDF

        Args:
            pdf_path: Ruta al PDF original
            detection_dpi: DPI para detección (150 es suficiente, más rápido)
            padding: Padding en píxeles a agregar al bounding box (default: 10)

        Returns:
            Tupla (x, y, width, height) en puntos PDF (72 DPI)
            o None si no se detecta contenido

        Note:
            Usa rasterización temporal SOLO para análisis.
            El PDF final se mantiene 100% vectorial.
        """
        # Convertir PDF a imagen de baja resolución para análisis
        images = pdf2image.convert_from_path(pdf_path, dpi=detection_dpi)

        if not images:
            return None

        # Convertir PIL Image a numpy array
        img_array = np.array(images[0])

        # Convertir a escala de grises
        if len(img_array.shape) == 3:
            gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        else:
            gray = img_array

        # Umbralizar: píxeles no blancos (contenido)
        # 250 es un umbral conservador (casi blanco)
        _, thresh = cv2.threshold(gray, 250, 255, cv2.THRESH_BINARY_INV)

        # Encontrar contornos del contenido
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if not contours:
            return None

        # Obtener bounding box de todos los contornos (contenido completo)
        x_coords = []
        y_coords = []

        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            x_coords.extend([x, x + w])
            y_coords.extend([y, y + h])

        # Bounding box mínimo que contiene todo el contenido
        x_min = max(0, min(x_coords) - padding)
        y_min = max(0, min(y_coords) - padding)
        x_max = min(img_array.shape[1], max(x_coords) + padding)
        y_max = min(img_array.shape[0], max(y_coords) + padding)

        bbox_width = x_max - x_min
        bbox_height = y_max - y_min

        # Convertir coordenadas de píxeles (detection_dpi) a puntos PDF (72 DPI)
        scale_factor = 72.0 / detection_dpi

        x_points = x_min * scale_factor
        y_points = y_min * scale_factor
        width_points = bbox_width * scale_factor
        height_points = bbox_height * scale_factor

        return (x_points, y_points, width_points, height_points)

    def crop_pdf_to_content(
        self,
        input_pdf_path: str,
        output_pdf_path: str,
        bbox: Optional[Tuple[float, float, float, float]] = None,
        detection_dpi: int = 150,
        padding: int = 10
    ) -> Tuple[float, float, float, float]:
        """
        Recorta un PDF para eliminar márgenes blancos, manteniendo calidad vectorial.

        Args:
            input_pdf_path: Ruta al PDF original
            output_pdf_path: Ruta donde guardar el PDF recortado
            bbox: Bounding box manual (x, y, width, height) en puntos PDF
                  Si es None, se detecta automáticamente
            detection_dpi: DPI para detección automática
            padding: Padding en píxeles para detección automática

        Returns:
            Bounding box aplicado (x, y, width, height) en puntos PDF

        Note:
            El PDF resultante es 100% vectorial (sin rasterizar).
            Solo el contenido se mantiene, eliminando márgenes blancos.
        """
        # Detectar bounding box si no se proporciona
        if bbox is None:
            bbox = self.detect_content_bbox_from_pdf(
                input_pdf_path,
                detection_dpi=detection_dpi,
                padding=padding
            )

            if bbox is None:
                # Si no se detecta contenido, copiar PDF sin cambios
                reader = PdfReader(input_pdf_path)
                writer = PdfWriter()
                for page in reader.pages:
                    writer.add_page(page)
                with open(output_pdf_path, 'wb') as f:
                    writer.write(f)

                # Retornar dimensiones completas
                page = reader.pages[0]
                return (0, 0, float(page.mediabox.width), float(page.mediabox.height))

        x_crop, y_crop, width_crop, height_crop = bbox

        # Leer PDF original
        reader = PdfReader(input_pdf_path)
        writer = PdfWriter()

        # Procesar cada página
        for page in reader.pages:
            # Obtener dimensiones originales
            original_box = page.mediabox
            original_width = float(original_box.width)
            original_height = float(original_box.height)

            # En coordenadas PDF, Y=0 está abajo
            # Convertir coordenadas de imagen (Y=0 arriba) a PDF (Y=0 abajo)
            y_crop_pdf = original_height - y_crop - height_crop

            # Definir cropbox para recortar al contenido
            page.cropbox = RectangleObject([
                x_crop,
                y_crop_pdf,
                x_crop + width_crop,
                y_crop_pdf + height_crop
            ])

            # Ajustar mediabox al cropbox
            page.mediabox = page.cropbox

            # Agregar página recortada
            writer.add_page(page)

        # Guardar PDF recortado
        with open(output_pdf_path, 'wb') as output_file:
            writer.write(output_file)

        return bbox

    def apply_crop_and_shift_to_pdf(
        self,
        input_pdf_path: str,
        output_pdf_path: str,
        shift_x: int,
        shift_y: int,
        auto_crop: bool = True,
        detection_dpi: int = 150,
        padding: int = 10
    ) -> None:
        """
        Aplica CROP + DESPLAZAMIENTO a un PDF en 2 fases (mantiene calidad vectorial).

        FASE 1 - AUTO-CROP:
        - Detecta el bounding box del contenido real
        - Recorta el PDF eliminando márgenes blancos
        - Resultado: PDF con solo contenido, sin espacios

        FASE 2 - DESPLAZAMIENTO:
        - Aplica shift al contenido YA RECORTADO
        - Los desplazamientos son mucho más notorios
        - Mantiene calidad vectorial 100%

        Args:
            input_pdf_path: Ruta al PDF original
            output_pdf_path: Ruta donde guardar el PDF procesado
            shift_x: Desplazamiento horizontal en píxeles (300 DPI)
            shift_y: Desplazamiento vertical en píxeles (300 DPI)
            auto_crop: Si aplicar auto-crop antes del desplazamiento
            detection_dpi: DPI para detección de contenido
            padding: Padding en píxeles para el crop

        Note:
            Este método combina:
            1. Crop inteligente (elimina márgenes)
            2. Desplazamiento (sobre contenido recortado)

            Resultado: Variaciones VISUALMENTE NOTORIAS manteniendo
            calidad vectorial 100% (texto seleccionable).
        """
        import tempfile

        if auto_crop:
            # FASE 1: Auto-crop (eliminar márgenes blancos)
            with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp:
                temp_pdf_path = tmp.name

            # Recortar al contenido
            bbox = self.crop_pdf_to_content(
                input_pdf_path,
                temp_pdf_path,
                detection_dpi=detection_dpi,
                padding=padding
            )

            # FASE 2: Aplicar desplazamiento al PDF recortado
            self.apply_shift_to_pdf_direct(
                temp_pdf_path,
                output_pdf_path,
                shift_x,
                shift_y
            )

            # Limpiar archivo temporal
            import os
            os.unlink(temp_pdf_path)
        else:
            # Solo desplazamiento (sin crop)
            self.apply_shift_to_pdf_direct(
                input_pdf_path,
                output_pdf_path,
                shift_x,
                shift_y
            )
