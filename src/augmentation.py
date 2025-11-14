"""
Data Augmentation para facturas
"""

from PIL import Image
from typing import Dict, List, Tuple, Optional
import copy
from pathlib import Path


class AugmentationConfig:
    """Configuración de transformaciones para data augmentation"""

    # Desplazamientos en píxeles
    # Rango: 30px (mínimo) a 120px (máximo)
    SHIFT_SMALL = 30   # Desplazamiento pequeño
    SHIFT_MEDIUM = 70  # Desplazamiento mediano
    SHIFT_LARGE = 120  # Desplazamiento grande

    # Banco completo de 16 transformaciones disponibles (en orden de prioridad)
    # El usuario puede elegir cuántas usar (1-16)
    ALL_TRANSFORMATIONS = [
        # Prioridad 1-4: Horizontales y verticales pequeñas (más sutiles)
        {"name": "derecha_small", "shift_x": SHIFT_SMALL, "shift_y": 0},
        {"name": "izquierda_small", "shift_x": -SHIFT_SMALL, "shift_y": 0},
        {"name": "abajo_small", "shift_x": 0, "shift_y": SHIFT_SMALL},
        {"name": "arriba_small", "shift_x": 0, "shift_y": -SHIFT_SMALL},

        # Prioridad 5-8: Horizontales y verticales medianas
        {"name": "derecha_medium", "shift_x": SHIFT_MEDIUM, "shift_y": 0},
        {"name": "izquierda_medium", "shift_x": -SHIFT_MEDIUM, "shift_y": 0},
        {"name": "abajo_medium", "shift_x": 0, "shift_y": SHIFT_MEDIUM},
        {"name": "arriba_medium", "shift_x": 0, "shift_y": -SHIFT_MEDIUM},

        # Prioridad 9-12: Diagonales pequeñas
        {"name": "diagonal_dr_small", "shift_x": SHIFT_SMALL, "shift_y": SHIFT_SMALL},
        {"name": "diagonal_ul_small", "shift_x": -SHIFT_SMALL, "shift_y": -SHIFT_SMALL},
        {"name": "diagonal_dl_small", "shift_x": -SHIFT_SMALL, "shift_y": SHIFT_SMALL},
        {"name": "diagonal_ur_small", "shift_x": SHIFT_SMALL, "shift_y": -SHIFT_SMALL},

        # Prioridad 13-16: Diagonales grandes (mayor variabilidad)
        {"name": "diagonal_dr_large", "shift_x": SHIFT_LARGE, "shift_y": SHIFT_LARGE},
        {"name": "diagonal_ul_large", "shift_x": -SHIFT_LARGE, "shift_y": -SHIFT_LARGE},
        {"name": "diagonal_dl_large", "shift_x": -SHIFT_LARGE, "shift_y": SHIFT_LARGE},
        {"name": "diagonal_ur_large", "shift_x": SHIFT_LARGE, "shift_y": -SHIFT_LARGE},
    ]

    def __init__(self, num_transformations: int = 10):
        """
        Inicializa la configuración con el número de transformaciones deseado.

        Args:
            num_transformations: Número de variaciones a generar (1-16)
                - 1-4: Solo desplazamientos pequeños básicos
                - 5-8: Agrega desplazamientos medianos
                - 9-12: Agrega diagonales pequeñas
                - 13-16: Agrega diagonales grandes (máxima variabilidad)

        Raises:
            ValueError: Si num_transformations no está en rango 1-16
        """
        if not 1 <= num_transformations <= 16:
            raise ValueError(
                f"num_transformations debe estar entre 1 y 16, recibido: {num_transformations}"
            )

        self.num_transformations = num_transformations
        # Seleccionar las primeras N transformaciones del banco
        self.TRANSFORMATIONS = self.ALL_TRANSFORMATIONS[:num_transformations]


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

        for idx, transform in enumerate(self.config.TRANSFORMATIONS, start=1):
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
                idx,
                transform
            )

            # Generar nombre de archivo
            filename = f"{base_filename}_aug_{idx:02d}_{transform['name']}.pdf"

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
            transform: Diccionario con info de la transformación

        Returns:
            Nuevo JSON con metadata de augmentation
        """
        # Crear copia profunda del JSON original
        augmented_json = copy.deepcopy(original_json)

        # Actualizar nombre de archivo
        new_filename = f"{base_filename}_aug_{aug_index:02d}_{transform['name']}.pdf"

        # Si existe campo 'filename', actualizarlo
        if 'filename' in augmented_json:
            augmented_json['filename'] = new_filename

        # Si existe campo 'archivo_factura', actualizarlo
        if 'archivo_factura' in augmented_json:
            augmented_json['archivo_factura'] = new_filename

        # Agregar metadata de augmentation
        augmented_json['augmentation'] = {
            'original_filename': f"{base_filename}.pdf",
            'transformation': transform['name'],
            'shift_x': transform['shift_x'],
            'shift_y': transform['shift_y'],
            'augmentation_index': aug_index
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
        Genera variaciones de un PDF usando CROP + DESPLAZAMIENTO (SIN rasterizar).

        PROCESO EN 2 FASES:

        FASE 1 - AUTO-CROP:
        - Detecta automáticamente el bounding box del contenido real
        - Elimina márgenes blancos del PDF
        - Resultado: PDF con SOLO contenido, sin espacios vacíos

        FASE 2 - DESPLAZAMIENTO:
        - Aplica desplazamientos (30px, 70px, 120px) al contenido YA RECORTADO
        - Los shifts son VISUALMENTE NOTORIOS (no se pierden en márgenes)
        - Mantiene calidad vectorial 100%

        VENTAJAS:
        - Texto vectorial (seleccionable, perfecta calidad)
        - Gráficos vectoriales intactos
        - Tamaño de archivo pequeño
        - Variaciones VISUALMENTE SIGNIFICATIVAS
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

        for idx, transform in enumerate(self.config.TRANSFORMATIONS, start=1):
            # Generar nombre de archivo de salida
            filename = f"{base_filename}_aug_{idx:02d}_{transform['name']}.pdf"
            output_pdf_path = os.path.join(output_dir, filename)

            # Aplicar CROP + DESPLAZAMIENTO al PDF (SIN rasterizar)
            # FASE 1: Auto-crop elimina márgenes blancos
            # FASE 2: Desplazamiento sobre contenido recortado (más notorio)
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
                idx,
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
            'total_transformations': len(self.config.TRANSFORMATIONS),
            'shift_levels': [
                self.config.SHIFT_SMALL,
                self.config.SHIFT_MEDIUM,
                self.config.SHIFT_LARGE
            ],
            'transformation_types': [t['name'] for t in self.config.TRANSFORMATIONS]
        }
