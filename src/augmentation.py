"""
Data Augmentation para facturas
"""

from PIL import Image
from typing import Dict, List, Tuple
import copy
import random


class AugmentationConfig:
    """Configuración de transformaciones para data augmentation"""

    # Rango de desplazamientos en píxeles (random)
    SHIFT_MIN = 10
    SHIFT_MAX = 45

    # Definición de las 16 transformaciones (direcciones)
    # Los valores exactos se generarán aleatoriamente en cada ejecución
    TRANSFORMATION_DIRECTIONS = [
        # Desplazamientos horizontales
        {"name": "derecha", "direction": "x", "sign": 1},
        {"name": "izquierda", "direction": "x", "sign": -1},

        # Desplazamientos verticales
        {"name": "abajo", "direction": "y", "sign": 1},
        {"name": "arriba", "direction": "y", "sign": -1},

        # Desplazamientos diagonales
        {"name": "diagonal_dr", "direction": "xy", "sign_x": 1, "sign_y": 1},
        {"name": "diagonal_dl", "direction": "xy", "sign_x": -1, "sign_y": 1},
        {"name": "diagonal_ur", "direction": "xy", "sign_x": 1, "sign_y": -1},
        {"name": "diagonal_ul", "direction": "xy", "sign_x": -1, "sign_y": -1},
    ]

    @classmethod
    def generate_transformations(cls, seed: int = None) -> List[Dict]:
        """
        Genera transformaciones con desplazamientos aleatorios.

        Args:
            seed: Semilla para reproducibilidad (opcional)

        Returns:
            Lista de transformaciones con valores random entre SHIFT_MIN y SHIFT_MAX
        """
        if seed is not None:
            random.seed(seed)

        transformations = []

        # Generar 2 variaciones por dirección (16 total)
        for direction_config in cls.TRANSFORMATION_DIRECTIONS:
            for variant in range(2):
                # Generar desplazamiento aleatorio entre 10-45 píxeles
                shift_value = random.randint(cls.SHIFT_MIN, cls.SHIFT_MAX)

                name = f"{direction_config['name']}_v{variant + 1}"

                if direction_config["direction"] == "x":
                    # Horizontal
                    shift_x = direction_config["sign"] * shift_value
                    shift_y = 0
                elif direction_config["direction"] == "y":
                    # Vertical
                    shift_x = 0
                    shift_y = direction_config["sign"] * shift_value
                else:  # "xy" - diagonal
                    # Para diagonales, generar valores random independientes
                    shift_x_val = random.randint(cls.SHIFT_MIN, cls.SHIFT_MAX)
                    shift_y_val = random.randint(cls.SHIFT_MIN, cls.SHIFT_MAX)
                    shift_x = direction_config["sign_x"] * shift_x_val
                    shift_y = direction_config["sign_y"] * shift_y_val

                transformations.append({
                    "name": name,
                    "shift_x": shift_x,
                    "shift_y": shift_y
                })

        return transformations


class InvoiceAugmenter:
    """Clase para aplicar data augmentation a facturas"""

    def __init__(self, image_processor, seed: int = None):
        """
        Inicializa el augmenter.

        Args:
            image_processor: Instancia de ImageProcessor
            seed: Semilla para reproducibilidad de random (opcional)
        """
        self.image_processor = image_processor
        self.config = AugmentationConfig()
        self.seed = seed
        # Generar transformaciones con valores random
        self.transformations = self.config.generate_transformations(seed=seed)

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

        for transform in self.transformations:
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
            'total_transformations': len(self.transformations),
            'shift_range': f"{self.config.SHIFT_MIN}-{self.config.SHIFT_MAX} píxeles",
            'transformation_types': [t['name'] for t in self.transformations],
            'transformations_detail': [
                {
                    'name': t['name'],
                    'shift_x': t['shift_x'],
                    'shift_y': t['shift_y']
                }
                for t in self.transformations
            ]
        }
