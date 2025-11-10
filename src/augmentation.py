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
    # Rango: 15px (mínimo) a 60px (máximo)
    SHIFT_SMALL = 15   # Desplazamiento pequeño
    SHIFT_MEDIUM = 35  # Desplazamiento mediano
    SHIFT_LARGE = 60   # Desplazamiento grande

    # Definición de las 16 transformaciones
    TRANSFORMATIONS = [
        # Desplazamientos horizontales pequeños
        {"name": "derecha_small", "shift_x": SHIFT_SMALL, "shift_y": 0},
        {"name": "izquierda_small", "shift_x": -SHIFT_SMALL, "shift_y": 0},

        # Desplazamientos verticales pequeños
        {"name": "abajo_small", "shift_x": 0, "shift_y": SHIFT_SMALL},
        {"name": "arriba_small", "shift_x": 0, "shift_y": -SHIFT_SMALL},

        # Desplazamientos diagonales pequeños
        {"name": "diagonal_dr_small", "shift_x": SHIFT_SMALL, "shift_y": SHIFT_SMALL},
        {"name": "diagonal_dl_small", "shift_x": -SHIFT_SMALL, "shift_y": SHIFT_SMALL},
        {"name": "diagonal_ur_small", "shift_x": SHIFT_SMALL, "shift_y": -SHIFT_SMALL},
        {"name": "diagonal_ul_small", "shift_x": -SHIFT_SMALL, "shift_y": -SHIFT_SMALL},

        # Desplazamientos horizontales medianos
        {"name": "derecha_medium", "shift_x": SHIFT_MEDIUM, "shift_y": 0},
        {"name": "izquierda_medium", "shift_x": -SHIFT_MEDIUM, "shift_y": 0},

        # Desplazamientos verticales medianos
        {"name": "abajo_medium", "shift_x": 0, "shift_y": SHIFT_MEDIUM},
        {"name": "arriba_medium", "shift_x": 0, "shift_y": -SHIFT_MEDIUM},

        # Desplazamientos horizontales grandes
        {"name": "derecha_large", "shift_x": SHIFT_LARGE, "shift_y": 0},
        {"name": "izquierda_large", "shift_x": -SHIFT_LARGE, "shift_y": 0},

        # Desplazamientos verticales grandes
        {"name": "abajo_large", "shift_x": 0, "shift_y": SHIFT_LARGE},
        {"name": "arriba_large", "shift_x": 0, "shift_y": -SHIFT_LARGE},
    ]


class InvoiceAugmenter:
    """Clase para aplicar data augmentation a facturas"""

    def __init__(self, image_processor):
        """
        Inicializa el augmenter.

        Args:
            image_processor: Instancia de ImageProcessor
        """
        self.image_processor = image_processor
        self.config = AugmentationConfig()

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
        Genera variaciones de un PDF manipulándolo directamente (SIN rasterizar).

        Esta es la forma CORRECTA de procesar PDFs ya que mantiene:
        - Texto vectorial (seleccionable, perfecta calidad)
        - Gráficos vectoriales intactos
        - Tamaño de archivo pequeño
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

            # Aplicar transformación directa al PDF (SIN rasterizar)
            self.image_processor.apply_shift_to_pdf_direct(
                input_pdf_path=pdf_path,
                output_pdf_path=output_pdf_path,
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
