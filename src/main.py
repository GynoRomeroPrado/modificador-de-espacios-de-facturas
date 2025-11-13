"""
Script principal para Data Augmentation de Facturas

Este script toma facturas existentes (imagen + JSON) y genera múltiples
variaciones mediante transformaciones geométricas simples (desplazamientos).
"""

import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List

from utils import (
    find_invoice_pairs,
    load_json,
    save_json,
    create_output_dirs,
    print_progress
)
from image_processor import ImageProcessor
from augmentation import InvoiceAugmenter


class InvoiceDatasetAugmenter:
    """Clase principal para augmentar datasets de facturas"""

    def __init__(
        self,
        input_dir: str,
        output_dir: str,
        dpi: int = 300,
        num_transformations: int = 10
    ):
        """
        Inicializa el augmenter del dataset.

        Args:
            input_dir: Directorio con las facturas originales
            output_dir: Directorio donde guardar los resultados
            dpi: DPI para convertir PDFs (default: 300)
                 300 DPI es el estándar profesional para OCR de alta calidad
            num_transformations: Número de variaciones a generar por factura (1-16)
                - 1-4: Solo desplazamientos pequeños (15px)
                - 5-8: Agrega desplazamientos medianos (35px)
                - 9-12: Agrega diagonales pequeñas
                - 13-16: Agrega diagonales grandes (60px) - máxima variabilidad
        """
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.num_transformations = num_transformations

        self.image_processor = ImageProcessor(dpi=dpi)
        self.augmenter = InvoiceAugmenter(
            self.image_processor,
            num_transformations=num_transformations
        )

        self.stats = {
            'original_invoices': 0,
            'augmented_invoices': 0,
            'total_invoices': 0,
            'errors': []
        }

    def process_dataset(self) -> Dict:
        """
        Procesa el dataset completo de facturas.

        Returns:
            Diccionario con estadísticas del proceso
        """
        print("=" * 60)
        print("🚀 INICIANDO DATA AUGMENTATION DE FACTURAS")
        print("=" * 60)

        # Crear directorios de salida
        print("\n📁 Creando estructura de directorios...")
        output_dirs = create_output_dirs(self.output_dir)

        # Encontrar pares de facturas
        print(f"\n🔍 Buscando facturas en: {self.input_dir}")
        invoice_pairs = find_invoice_pairs(self.input_dir)

        if not invoice_pairs:
            print("❌ No se encontraron pares de facturas (imagen + JSON)")
            return self.stats

        print(f"✅ Se encontraron {len(invoice_pairs)} facturas")

        # Aleatorizar orden de procesamiento para evitar sesgos
        import random
        random.shuffle(invoice_pairs)
        print(f"🔀 Orden de procesamiento aleatorizado")

        # Procesar cada factura
        print("\n" + "=" * 60)
        print("📋 PROCESANDO FACTURAS (ORDEN ALEATORIO)")
        print("=" * 60)

        for idx, (image_path, json_path) in enumerate(invoice_pairs, start=1):
            self._process_invoice(
                image_path,
                json_path,
                idx,
                len(invoice_pairs),
                output_dirs
            )

        # Calcular estadísticas finales
        self._calculate_final_stats()

        # Guardar reporte
        self._save_report()

        # Mostrar resumen
        self._print_summary()

        return self.stats

    def _process_invoice(
        self,
        image_path: str,
        json_path: str,
        index: int,
        total: int,
        output_dirs: Dict
    ) -> None:
        """
        Procesa una factura individual.

        Args:
            image_path: Ruta a la imagen de la factura
            json_path: Ruta al JSON de la factura
            index: Índice de la factura (1-based)
            total: Total de facturas
            output_dirs: Diccionario con directorios de salida
        """
        try:
            original_name = Path(image_path).stem
            print(f"\n[{index}/{total}] Procesando: {original_name}")

            # Cargar JSON
            print("  📥 Cargando JSON...")
            json_data = load_json(json_path)

            # Generar nombre estandarizado
            base_filename = f"factura_{index:04d}"
            original_extension = Path(image_path).suffix

            # Detectar si es PDF para procesamiento directo
            is_pdf = original_extension.lower() == '.pdf'

            if is_pdf:
                # PROCESAMIENTO DIRECTO DE PDF (SIN RASTERIZAR)
                # Esto mantiene texto vectorial y calidad original 100%
                print("  📄 Detectado PDF - Procesamiento vectorial directo (sin rasterizar)")

                # Copiar PDF original
                print("  💾 Guardando PDF original...")
                import shutil
                original_pdf_dest = os.path.join(
                    output_dirs['organized'],
                    f"{base_filename}{original_extension}"
                )
                shutil.copy2(image_path, original_pdf_dest)

                # Actualizar JSON para PDF original
                updated_json = json_data.copy()
                updated_json['filename'] = f"{base_filename}{original_extension}"
                if 'archivo_factura' in updated_json:
                    updated_json['archivo_factura'] = f"{base_filename}{original_extension}"
                json_path_dest = os.path.join(output_dirs['organized'], f"{base_filename}.json")
                save_json(updated_json, json_path_dest)

                # Generar variaciones augmentadas (manipulación directa de PDF)
                print(f"  🔄 Generando {self.num_transformations} variaciones con manipulación directa de PDF...")
                augmented_data = self.augmenter.augment_invoice_from_pdf(
                    pdf_path=image_path,
                    json_data=json_data,
                    base_filename=base_filename,
                    output_dir=output_dirs['augmented']
                )

                # Guardar JSONs de variaciones (PDFs ya están guardados)
                print("  💾 Guardando JSONs de variaciones...")
                for pdf_path, aug_json, filename in augmented_data:
                    json_filename = filename.replace('.pdf', '.json')
                    json_path_out = os.path.join(output_dirs['augmented'], json_filename)
                    save_json(aug_json, json_path_out)

            else:
                # PROCESAMIENTO DE IMAGEN (PNG/JPG)
                # Rasterizar y aplicar mejoras OCR
                print("  🖼️  Detectado imagen - Procesamiento con mejoras OCR")

                # Cargar imagen
                print("  📥 Cargando imagen...")
                image = self.image_processor.load_image(image_path)

                # Guardar factura original renombrada con mejoras OCR
                print("  💾 Guardando imagen original con mejoras OCR...")
                self._save_organized_invoice(
                    image,
                    json_data,
                    base_filename,
                    original_extension,
                    output_dirs['organized']
                )

                # Generar variaciones augmentadas
                print(f"  🔄 Generando {self.num_transformations} variaciones augmentadas...")
                augmented_data = self.augmenter.augment_invoice(
                    image,
                    json_data,
                    base_filename
                )

                # Guardar variaciones augmentadas
                print("  💾 Guardando variaciones...")
                self._save_augmented_invoices(
                    augmented_data,
                    output_dirs['augmented']
                )

            # Actualizar estadísticas
            self.stats['original_invoices'] += 1
            self.stats['augmented_invoices'] += len(augmented_data)

            print(f"  ✅ Completado: 1 original + {len(augmented_data)} augmentadas")

        except Exception as e:
            error_msg = f"Error procesando {image_path}: {str(e)}"
            print(f"  ❌ {error_msg}")
            self.stats['errors'].append(error_msg)

    def _save_organized_invoice(
        self,
        image,
        json_data: Dict,
        base_filename: str,
        original_extension: str,
        output_dir: str
    ) -> None:
        """
        Guarda la factura original renombrada.

        Args:
            image: Imagen de la factura
            json_data: Datos JSON de la factura
            base_filename: Nombre base (sin extensión)
            original_extension: Extensión original del archivo
            output_dir: Directorio de salida
        """
        # Guardar imagen con mejoras para OCR
        image_filename = f"{base_filename}{original_extension}"
        image_path = os.path.join(output_dir, image_filename)

        # Guardar con mejoras OCR respetando la extensión original
        self.image_processor.save_image_with_ocr_enhancement(
            image, image_path, enhance=True
        )

        # Actualizar y guardar JSON
        updated_json = json_data.copy()
        updated_json['filename'] = image_filename
        if 'archivo_factura' in updated_json:
            updated_json['archivo_factura'] = image_filename

        json_path = os.path.join(output_dir, f"{base_filename}.json")
        save_json(updated_json, json_path)

    def _save_augmented_invoices(
        self,
        augmented_data: List,
        output_dir: str
    ) -> None:
        """
        Guarda las facturas augmentadas.

        Args:
            augmented_data: Lista de tuplas (imagen, json, filename)
            output_dir: Directorio de salida
        """
        for aug_image, aug_json, filename in augmented_data:
            # Guardar imagen con mejoras para OCR
            image_path = os.path.join(output_dir, filename)
            self.image_processor.save_image_with_ocr_enhancement(
                aug_image, image_path, enhance=True
            )

            # Guardar JSON
            json_filename = filename.replace('.pdf', '.json')
            json_path = os.path.join(output_dir, json_filename)
            save_json(aug_json, json_path)

    def _calculate_final_stats(self) -> None:
        """Calcula estadísticas finales del proceso"""
        self.stats['total_invoices'] = (
            self.stats['original_invoices'] +
            self.stats['augmented_invoices']
        )

        aug_stats = self.augmenter.get_augmentation_stats()
        self.stats['transformations_per_invoice'] = aug_stats['total_transformations']

    def _save_report(self) -> None:
        """Guarda el reporte del proceso"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'input_directory': self.input_dir,
            'output_directory': self.output_dir,
            'statistics': self.stats,
            'augmentation_config': self.augmenter.get_augmentation_stats()
        }

        report_path = os.path.join(self.output_dir, 'dataset_report.json')
        save_json(report, report_path, indent=2)
        print(f"\n📊 Reporte guardado en: {report_path}")

    def _print_summary(self) -> None:
        """Imprime un resumen del proceso"""
        print("\n" + "=" * 60)
        print("✅ PROCESO COMPLETADO")
        print("=" * 60)
        print(f"\n📊 RESUMEN:")
        print(f"  • Facturas originales:     {self.stats['original_invoices']}")
        print(f"  • Facturas augmentadas:    {self.stats['augmented_invoices']}")
        print(f"  • Total de facturas:       {self.stats['total_invoices']}")

        if self.stats['errors']:
            print(f"\n⚠️  Errores encontrados:     {len(self.stats['errors'])}")
            for error in self.stats['errors']:
                print(f"    - {error}")

        expansion_rate = (
            self.stats['total_invoices'] / self.stats['original_invoices']
            if self.stats['original_invoices'] > 0
            else 0
        )
        print(f"\n🚀 Dataset expandido {expansion_rate:.1f}x")
        print("=" * 60)


def main():
    """Función principal"""
    if len(sys.argv) < 3:
        print("Uso: python main.py <input_dir> <output_dir>")
        print("\nEjemplo:")
        print("  python main.py /Drive/Facturas /Drive/Facturas_Procesadas")
        sys.exit(1)

    input_dir = sys.argv[1]
    output_dir = sys.argv[2]

    # Validar que el directorio de entrada exista
    if not os.path.exists(input_dir):
        print(f"❌ Error: El directorio {input_dir} no existe")
        sys.exit(1)

    # Crear augmenter y procesar
    augmenter = InvoiceDatasetAugmenter(input_dir, output_dir)
    stats = augmenter.process_dataset()

    # Retornar código de error si hubo problemas
    if stats['errors']:
        sys.exit(1)


if __name__ == "__main__":
    main()
