"""
Script principal para Data Augmentation de Facturas

Este script toma facturas existentes (PDF + JSON) y genera múltiples
variaciones mediante transformaciones geométricas simples (desplazamientos).
"""

import os
import sys
import shutil
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

    def __init__(self, input_dir: str, output_dir: str, dpi: int = 200, max_invoices: int = None):
        """
        Inicializa el augmenter del dataset.

        Args:
            input_dir: Directorio con las facturas originales
            output_dir: Directorio donde guardar los resultados
            dpi: DPI para convertir PDFs (default: 200)
            max_invoices: Número máximo de facturas a procesar (None = todas)
        """
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.max_invoices = max_invoices

        self.image_processor = ImageProcessor(dpi=dpi)
        self.augmenter = InvoiceAugmenter(self.image_processor)

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
            print("❌ No se encontraron pares de facturas (PDF + JSON)")
            return self.stats

        # Limitar número de facturas si se especificó
        if self.max_invoices and self.max_invoices < len(invoice_pairs):
            invoice_pairs = invoice_pairs[:self.max_invoices]
            print(f"✅ Procesando {self.max_invoices} de {len(invoice_pairs)} facturas disponibles")
        else:
            print(f"✅ Se encontraron {len(invoice_pairs)} facturas")

        # Procesar cada factura
        print("\n" + "=" * 60)
        print("📋 PROCESANDO FACTURAS")
        print("=" * 60)

        for idx, (pdf_path, json_path) in enumerate(invoice_pairs, start=1):
            self._process_invoice(
                pdf_path,
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
        pdf_path: str,
        json_path: str,
        index: int,
        total: int,
        output_dirs: Dict
    ) -> None:
        """
        Procesa una factura individual.

        Args:
            pdf_path: Ruta al PDF de la factura
            json_path: Ruta al JSON de la factura
            index: Índice de la factura (1-based)
            total: Total de facturas
            output_dirs: Diccionario con directorios de salida
        """
        try:
            original_name = Path(pdf_path).stem
            print(f"\n[{index}/{total}] Procesando: {original_name}")

            # Cargar PDF y JSON
            print("  📥 Cargando PDF y JSON...")
            image = self.image_processor.load_image(pdf_path)
            json_data = load_json(json_path)

            # 1. Guardar factura original (copia)
            print("  💾 Guardando factura original...")
            self._save_original_invoice(
                pdf_path,
                json_path,
                original_name,
                output_dirs
            )

            # 2. Generar 16 variaciones augmentadas
            print("  🔄 Generando 16 variaciones augmentadas...")
            augmented_data = self.augmenter.augment_invoice(
                image,
                json_data,
                original_name
            )

            # 3. Guardar variaciones augmentadas
            print("  💾 Guardando variaciones...")
            self._save_augmented_invoices(
                augmented_data,
                output_dirs
            )

            # Actualizar estadísticas
            self.stats['original_invoices'] += 1
            self.stats['augmented_invoices'] += len(augmented_data)

            print(f"  ✅ Completado: 1 original + {len(augmented_data)} augmentadas = {len(augmented_data) + 1} archivos")

        except Exception as e:
            error_msg = f"Error procesando {pdf_path}: {str(e)}"
            print(f"  ❌ {error_msg}")
            self.stats['errors'].append(error_msg)

    def _save_original_invoice(
        self,
        pdf_path: str,
        json_path: str,
        original_name: str,
        output_dirs: Dict
    ) -> None:
        """
        Guarda la factura original (copia del PDF y JSON).

        Args:
            pdf_path: Ruta al PDF original
            json_path: Ruta al JSON original
            original_name: Nombre original del archivo (sin extensión)
            output_dirs: Diccionario con directorios de salida
        """
        # Copiar PDF original
        pdf_output = os.path.join(output_dirs['facturas_procesadas'], f"{original_name}.pdf")
        shutil.copy2(pdf_path, pdf_output)

        # Copiar JSON original
        json_output = os.path.join(output_dirs['anotaciones'], f"{original_name}.json")
        shutil.copy2(json_path, json_output)

    def _save_augmented_invoices(
        self,
        augmented_data: List,
        output_dirs: Dict
    ) -> None:
        """
        Guarda las facturas augmentadas.

        Args:
            augmented_data: Lista de tuplas (imagen, json, filename)
            output_dirs: Diccionario con directorios de salida
        """
        for aug_image, aug_json, filename in augmented_data:
            # Guardar PDF
            pdf_path = os.path.join(output_dirs['facturas_procesadas'], filename)
            self.image_processor.save_image(aug_image, pdf_path)

            # Guardar JSON
            json_filename = filename.replace('.pdf', '.json')
            json_path = os.path.join(output_dirs['anotaciones'], json_filename)
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
        print("Uso: python main.py <input_dir> <output_dir> [max_invoices]")
        print("\nEjemplo:")
        print("  python main.py 'Datos extraidos de Originales' facturas_con_margenes_modificados")
        print("  python main.py 'Datos extraidos de Originales' facturas_con_margenes_modificados 1")
        sys.exit(1)

    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
    max_invoices = int(sys.argv[3]) if len(sys.argv) > 3 else None

    # Validar que el directorio de entrada exista
    if not os.path.exists(input_dir):
        print(f"❌ Error: El directorio {input_dir} no existe")
        sys.exit(1)

    # Crear augmenter y procesar
    augmenter = InvoiceDatasetAugmenter(input_dir, output_dir, max_invoices=max_invoices)
    stats = augmenter.process_dataset()

    # Retornar código de error si hubo problemas
    if stats['errors']:
        sys.exit(1)


if __name__ == "__main__":
    main()
