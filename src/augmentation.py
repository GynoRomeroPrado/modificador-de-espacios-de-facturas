"""
Data Augmentation para facturas
"""

from PIL import Image
from typing import Dict, List, Tuple
import copy


class AugmentationConfig:
    """Configuración de transformaciones para data augmentation"""

    # Desplazamientos en píxeles
    SHIFT_SMALL = 10
    SHIFT_MEDIUM = 20
    SHIFT_LARGE = 30

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

        for transform in self.config.TRANSFORMATIONS:
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
                transform
            )

            # Generar nombre de archivo (mantiene nombre original + transformación + .pdf)
            filename = f"{base_filename}_{transform['name']}.pdf"

            augmented_data.append((augmented_image, augmented_json, filename))

        return augmented_data

    def _create_augmented_json(
        self,
        original_json: Dict,
        base_filename: str,
        transform: Dict
    ) -> Dict:
        """
        Crea una copia del JSON original actualizado con el nuevo nombre.

        Args:
            original_json: JSON original
            base_filename: Nombre base del archivo
            transform: Diccionario con info de la transformación

        Returns:
            Copia del JSON con nombre de archivo actualizado
        """
        # Crear copia profunda del JSON original
        augmented_json = copy.deepcopy(original_json)

        # Actualizar nombre de archivo
        new_filename = f"{base_filename}_{transform['name']}.pdf"

        # Si existe campo 'filename', actualizarlo
        if 'filename' in augmented_json:
            augmented_json['filename'] = new_filename

        # Si existe campo 'archivo_factura', actualizarlo
        if 'archivo_factura' in augmented_json:
            augmented_json['archivo_factura'] = new_filename

        return augmented_json

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
