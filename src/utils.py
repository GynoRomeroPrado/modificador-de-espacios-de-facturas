"""
Utilidades para el sistema de Data Augmentation de Facturas
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Tuple, Optional


def load_json(json_path: str) -> Dict:
    """
    Carga un archivo JSON.

    Args:
        json_path: Ruta al archivo JSON

    Returns:
        Diccionario con los datos del JSON
    """
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json(data: Dict, output_path: str, indent: int = 2) -> None:
    """
    Guarda un diccionario como archivo JSON.

    Args:
        data: Diccionario a guardar
        output_path: Ruta donde guardar el JSON
        indent: Nivel de indentación (default: 2)
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=indent)


def find_invoice_pairs(input_dir: str) -> List[Tuple[str, str]]:
    """
    Encuentra pares de factura (PDF + JSON) en estructura de directorios específica.

    Args:
        input_dir: Directorio raíz donde buscar (debe contener facturas_procesadas/ y anotaciones/)

    Returns:
        Lista de tuplas (ruta_pdf, ruta_json)
    """
    input_path = Path(input_dir)
    pairs = []

    # Directorios esperados
    facturas_dir = input_path / 'facturas_procesadas'
    anotaciones_dir = input_path / 'anotaciones'

    # Validar que existan los directorios
    if not facturas_dir.exists():
        print(f"❌ Error: No se encontró el directorio {facturas_dir}")
        return pairs

    if not anotaciones_dir.exists():
        print(f"❌ Error: No se encontró el directorio {anotaciones_dir}")
        return pairs

    # Buscar todos los PDFs en facturas_procesadas
    for pdf_file in facturas_dir.glob('*.pdf'):
        # Buscar el JSON correspondiente en anotaciones
        json_file = anotaciones_dir / f"{pdf_file.stem}.json"

        if json_file.exists():
            pairs.append((str(pdf_file), str(json_file)))
        else:
            print(f"⚠️  Advertencia: No se encontró JSON para {pdf_file.name}")

    return pairs


def generate_invoice_name(index: int, extension: str = '.pdf') -> str:
    """
    Genera un nombre estandarizado para una factura.

    Args:
        index: Índice de la factura (empezando en 1)
        extension: Extensión del archivo

    Returns:
        Nombre de archivo formateado (ej: "factura_0001.pdf")
    """
    return f"factura_{index:04d}{extension}"


def generate_augmented_name(base_name: str, aug_index: int, transformation: str) -> str:
    """
    Genera un nombre para una factura augmentada.

    Args:
        base_name: Nombre base de la factura (sin extensión)
        aug_index: Índice de la augmentación (1-16)
        transformation: Tipo de transformación aplicada

    Returns:
        Nombre de archivo augmentado (ej: "factura_0001_aug_01_derecha.png")
    """
    return f"{base_name}_aug_{aug_index:02d}_{transformation}.png"


def create_output_dirs(output_dir: str) -> Dict[str, str]:
    """
    Crea la estructura de directorios de salida.

    Args:
        output_dir: Directorio raíz de salida

    Returns:
        Diccionario con las rutas de los subdirectorios
    """
    output_path = Path(output_dir)

    dirs = {
        'facturas_procesadas': output_path / 'facturas_procesadas',
        'anotaciones': output_path / 'anotaciones'
    }

    for dir_path in dirs.values():
        dir_path.mkdir(parents=True, exist_ok=True)

    return {k: str(v) for k, v in dirs.items()}


def validate_json_structure(json_data: Dict, required_fields: Optional[List[str]] = None) -> bool:
    """
    Valida que un JSON tenga la estructura esperada.

    Args:
        json_data: Datos del JSON a validar
        required_fields: Lista de campos requeridos (opcional)

    Returns:
        True si es válido, False en caso contrario
    """
    if required_fields is None:
        # Campos mínimos esperados
        required_fields = ['filename']

    for field in required_fields:
        if field not in json_data:
            return False

    return True


def print_progress(current: int, total: int, message: str = "") -> None:
    """
    Imprime el progreso de una operación.

    Args:
        current: Número actual
        total: Total de items
        message: Mensaje adicional
    """
    percentage = (current / total) * 100
    print(f"[{current}/{total}] ({percentage:.1f}%) {message}")
