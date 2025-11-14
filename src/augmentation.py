"""
Data Augmentation para facturas
"""

from PIL import Image
from typing import Dict, List, Tuple, Optional
import copy
from pathlib import Path
import random


class AugmentationConfig:
    """Configuración de transformaciones para data augmentation"""

    # Desplazamientos ALEATORIOS en píxeles
    # Cada transformación usa valores únicos en este rango
    SHIFT_MIN = 45   # Desplazamiento mínimo (0.63 pulgadas @ 300 DPI)
    SHIFT_MAX = 60   # Desplazamiento máximo (0.84 pulgadas @ 300 DPI)

    # Número máximo de transformaciones disponibles
    # El usuario puede elegir cuántas usar (1-16)
    # Los desplazamientos se generan aleatoriamente para cada transformación
    MAX_TRANSFORMATIONS = 16

    def __init__(self, num_transformations: int = 10):
        """
        Inicializa la configuración con el número de transformaciones deseado.

        Args:
            num_transformations: Número de variaciones a generar (1-16)
                Cada variación tendrá desplazamientos aleatorios entre
                SHIFT_MIN y SHIFT_MAX píxeles.

        Raises:
            ValueError: Si num_transformations no está en rango 1-16
        """
        if not 1 <= num_transformations <= self.MAX_TRANSFORMATIONS:
            raise ValueError(
                f"num_transformations debe estar entre 1 y {self.MAX_TRANSFORMATIONS}, "
                f"recibido: {num_transformations}"
            )

        self.num_transformations = num_transformations

    def generate_random_shifts(self) -> List[Dict]:
        """
        Genera desplazamientos aleatorios para todas las transformaciones.

        Returns:
            Lista de diccionarios con shift_x y shift_y aleatorios
        """
        transformations = []
        for i in range(self.num_transformations):
            # Generar desplazamientos aleatorios únicos para esta transformación
            shift_x = random.randint(self.SHIFT_MIN, self.SHIFT_MAX) * random.choice([-1, 1])
            shift_y = random.randint(self.SHIFT_MIN, self.SHIFT_MAX) * random.choice([-1, 1])

            transformations.append({
                "index": i + 1,
                "shift_x": shift_x,
                "shift_y": shift_y
            })

        return transformations


class InvoiceAugmenter:
    """Clase para aplicar data augmentation a facturas"""

    def __init__(self, image_processor, num_transformations: int = 10):
        """
        Inicializa el augmenter.

        Args:
            image_processor: Instancia de ImageProcessor
            num_transformations: Número de variaciones a generar (1-16)
        """
        self.image_processor = image_processor
        self.config = AugmentationConfig(num_transformations=num_transformations)

    def augment_invoice(
        self,
        image: Image.Image,
        json_data: Dict,
        base_filename: str
    ) -> List[Tuple[Image.Image, Dict, str]]:
        """
        Genera todas las variaciones augmentadas de una factura.

        Args:
            image: Imagen original de la factura
            json_data: JSON con los datos de la factura
            base_filename: Nombre base del archivo (sin extensión)

        Returns:
            Lista de tuplas (imagen_augmentada, json_augmentado, nombre_archivo)
        """
        augmented_data = []

        # Generar desplazamientos aleatorios para todas las transformaciones
        transformations = self.config.generate_random_shifts()

        for transform in transformations:
            # Aplicar transformación a la imagen
            augmented_image = self.image_processor.apply_shift(
                image,
                shift_x=transform['shift_x'],
                shift_y=transform['shift_y']
            )

            # Crear JSON augmentado
            augmented_json = self._create_augmented_json(
                json_data,
                base_filename,
                transform['index'],
                transform
            )

            # Generar nombre de archivo simplificado (sin dirección)
            filename = f"{base_filename}_aug_{transform['index']:02d}.pdf"

            augmented_data.append((augmented_image, augmented_json, filename))

        return augmented_data

    def _create_augmented_json(
        self,
        original_json: Dict,
        base_filename: str,
        aug_index: int,
        transform: Dict
    ) -> Dict:
        """
        Crea una copia del JSON original con metadata de augmentation.

        Args:
            original_json: JSON original
            base_filename: Nombre base del archivo
            aug_index: Índice de la augmentación
            transform: Diccionario con info de la transformación (shift_x, shift_y)

        Returns:
            Nuevo JSON con metadata de augmentation
        """
        # Crear copia profunda del JSON original
        augmented_json = copy.deepcopy(original_json)

        # Actualizar nombre de archivo (simplificado, sin dirección)
        new_filename = f"{base_filename}_aug_{aug_index:02d}.pdf"

        # Si existe campo 'filename', actualizarlo
        if 'filename' in augmented_json:
            augmented_json['filename'] = new_filename

        # Si existe campo 'archivo_factura', actualizarlo
        if 'archivo_factura' in augmented_json:
            augmented_json['archivo_factura'] = new_filename

        # Agregar metadata de augmentation
        augmented_json['augmentation'] = {
            'original_filename': f"{base_filename}.pdf",
            'shift_x': transform['shift_x'],
            'shift_y': transform['shift_y'],
            'augmentation_index': aug_index,
            'shift_range': f"{self.config.SHIFT_MIN}-{self.config.SHIFT_MAX}px"
        }

        # Marcar como dato augmentado
        augmented_json['is_augmented'] = True

        return augmented_json

    def augment_invoice_from_pdf(
        self,
        pdf_path: str,
        json_data: Dict,
        base_filename: str,
        output_dir: str
    ) -> List[Tuple[str, Dict, str]]:
        """
        Genera variaciones de un PDF usando CROP + DESPLAZAMIENTO ALEATORIO (SIN rasterizar).

        PROCESO EN 2 FASES:

        FASE 1 - AUTO-CROP:
        - Detecta automáticamente el bounding box del contenido real
        - Elimina márgenes blancos del PDF
        - Resultado: PDF con SOLO contenido, sin espacios vacíos

        FASE 2 - DESPLAZAMIENTO ALEATORIO:
        - Aplica desplazamientos ALEATORIOS (45-60px) al contenido YA RECORTADO
        - Cada PDF recibe desplazamientos ÚNICOS en X y Y
        - Direcciones aleatorias (±X, ±Y)
        - Mantiene calidad vectorial 100%

        VENTAJAS:
        - Texto vectorial (seleccionable, perfecta calidad)
        - Gráficos vectoriales intactos
        - Tamaño de archivo pequeño
        - Variaciones ÚNICAS (no repetibles)
        - Calidad original 100%

        Args:
            pdf_path: Ruta al PDF original
            json_data: JSON con los datos de la factura
            base_filename: Nombre base del archivo (sin extensión)
            output_dir: Directorio donde guardar PDFs generados

        Returns:
            Lista de tuplas (ruta_pdf_generado, json_augmentado, nombre_archivo)
        """
        import os
        augmented_data = []

        # Generar desplazamientos aleatorios para todas las transformaciones
        transformations = self.config.generate_random_shifts()

        for transform in transformations:
            # Generar nombre de archivo de salida (simplificado)
            filename = f"{base_filename}_aug_{transform['index']:02d}.pdf"
            output_pdf_path = os.path.join(output_dir, filename)

            # Aplicar CROP + DESPLAZAMIENTO ALEATORIO al PDF (SIN rasterizar)
            # FASE 1: Auto-crop elimina márgenes blancos
            # FASE 2: Desplazamiento aleatorio sobre contenido recortado
            self.image_processor.apply_crop_and_shift_to_pdf(
                input_pdf_path=pdf_path,
                output_pdf_path=output_pdf_path,
                shift_x=transform['shift_x'],
                shift_y=transform['shift_y'],
                auto_crop=True,  # Activar auto-crop para variaciones notorias
                detection_dpi=150,  # DPI para detección (150 es rápido y suficiente)
                padding=10  # 10px de padding alrededor del contenido
            )

            # Crear JSON augmentado
            augmented_json = self._create_augmented_json(
                json_data,
                base_filename,
                transform['index'],
                transform
            )

            augmented_data.append((output_pdf_path, augmented_json, filename))

        return augmented_data

    def get_augmentation_stats(self) -> Dict:
        """
        Retorna estadísticas sobre las transformaciones disponibles.

        Returns:
            Diccionario con estadísticas
        """
        return {
            'total_transformations': self.config.num_transformations,
            'shift_range': {
                'min': self.config.SHIFT_MIN,
                'max': self.config.SHIFT_MAX,
                'unit': 'pixels'
            },
            'shift_type': 'random',
            'description': f'Cada transformación usa desplazamientos aleatorios entre {self.config.SHIFT_MIN}-{self.config.SHIFT_MAX}px'
        }
