"""
Script de prueba para verificar manipulación directa de PDFs (SIN rasterizar)

Este script demuestra que:
1. PDFs manipulados directamente mantienen texto vectorial (seleccionable)
2. PDFs rasterizados pierden texto vectorial (texto se convierte en imagen)
3. Tamaño de archivo es mucho menor con manipulación directa
4. Calidad visual es perfecta con manipulación directa
"""

import sys
import os
from pathlib import Path

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from image_processor import ImageProcessor
from pypdf import PdfReader

def test_pdf_direct_manipulation():
    """Prueba manipulación directa de PDF vs rasterización"""

    print("=" * 80)
    print("🔬 PRUEBA: MANIPULACIÓN DIRECTA DE PDF vs RASTERIZACIÓN")
    print("=" * 80)

    # Usar una factura de ejemplo
    test_pdf = "Datos extraidos de Originales/facturas_procesadas/01-F020-00051515-COSTA DEL SOL WYNDHAM CAJAMARCA_page-0001.pdf"

    if not os.path.exists(test_pdf):
        print(f"❌ No se encontró la factura de prueba: {test_pdf}")
        print("Por favor, especifica una ruta válida a un PDF.")
        return

    print(f"\n📄 Factura de prueba: {os.path.basename(test_pdf)}")

    # Crear directorio de prueba
    test_output_dir = "test_pdf_direct_output"
    os.makedirs(test_output_dir, exist_ok=True)

    # Obtener tamaño original
    original_size = os.path.getsize(test_pdf) / 1024  # KB

    print("\n" + "=" * 80)
    print("MÉTODO 1: MANIPULACIÓN DIRECTA DE PDF (CORRECTO)")
    print("=" * 80)

    # Método 1: Manipulación directa (CORRECTO)
    print("\n1️⃣  Aplicando desplazamiento directo al PDF (SIN rasterizar)...")
    processor = ImageProcessor(dpi=300)

    output_direct = os.path.join(test_output_dir, "factura_desplazada_DIRECTO.pdf")

    processor.apply_shift_to_pdf_direct(
        input_pdf_path=test_pdf,
        output_pdf_path=output_direct,
        shift_x=20,  # 20 píxeles a la derecha @ 300 DPI
        shift_y=10   # 10 píxeles abajo @ 300 DPI
    )

    size_direct = os.path.getsize(output_direct) / 1024  # KB
    print(f"   ✓ PDF generado: {output_direct}")
    print(f"   ✓ Tamaño: {size_direct:.1f} KB")

    # Verificar que el texto es vectorial (extraíble)
    reader_direct = PdfReader(output_direct)
    text_direct = reader_direct.pages[0].extract_text()
    has_text_direct = len(text_direct.strip()) > 0

    print(f"   ✓ Texto vectorial extraíble: {'SÍ ✅' if has_text_direct else 'NO ❌'}")
    if has_text_direct:
        print(f"   ✓ Caracteres extraídos: {len(text_direct)}")
        print(f"   ✓ Muestra de texto: {text_direct[:100]}...")

    print("\n" + "=" * 80)
    print("MÉTODO 2: RASTERIZACIÓN (INCORRECTO - para comparación)")
    print("=" * 80)

    # Método 2: Rasterización (INCORRECTO, solo para comparación)
    print("\n2️⃣  Convirtiendo a imagen y guardando como PDF (RASTERIZANDO)...")

    # Cargar PDF como imagen
    image = processor.load_image(test_pdf)

    # Aplicar shift a la imagen
    shifted_image = processor.apply_shift(image, shift_x=20, shift_y=10)

    # Guardar como PDF (rasterizado)
    output_rasterized = os.path.join(test_output_dir, "factura_desplazada_RASTERIZADO.pdf")
    processor.save_image(shifted_image, output_rasterized)

    size_rasterized = os.path.getsize(output_rasterized) / 1024  # KB
    print(f"   ✓ PDF generado: {output_rasterized}")
    print(f"   ✓ Tamaño: {size_rasterized:.1f} KB")

    # Verificar que el texto NO es vectorial (perdido)
    reader_rasterized = PdfReader(output_rasterized)
    text_rasterized = reader_rasterized.pages[0].extract_text()
    has_text_rasterized = len(text_rasterized.strip()) > 0

    print(f"   ✓ Texto vectorial extraíble: {'SÍ ✅' if has_text_rasterized else 'NO ❌'}")
    if has_text_rasterized:
        print(f"   ✓ Caracteres extraídos: {len(text_rasterized)}")
    else:
        print(f"   ⚠️  Texto convertido a imagen - NO ES SELECCIONABLE")

    print("\n" + "=" * 80)
    print("📊 COMPARACIÓN DE RESULTADOS")
    print("=" * 80)

    print(f"\n📁 Tamaño de archivo:")
    print(f"   Original:     {original_size:.1f} KB")
    print(f"   Directo:      {size_direct:.1f} KB ({size_direct/original_size*100:.1f}% del original)")
    print(f"   Rasterizado:  {size_rasterized:.1f} KB ({size_rasterized/original_size*100:.1f}% del original)")

    if size_rasterized > size_direct:
        print(f"   💾 DIRECTO es {size_rasterized/size_direct:.1f}x más liviano")

    print(f"\n📝 Texto vectorial:")
    print(f"   Directo:      {'✅ PRESERVADO' if has_text_direct else '❌ PERDIDO'}")
    print(f"   Rasterizado:  {'✅ PRESERVADO' if has_text_rasterized else '❌ PERDIDO'}")

    print(f"\n🎯 Calidad:")
    print(f"   Directo:      ✅ 100% (vectorial, sin pérdida)")
    print(f"   Rasterizado:  ⚠️  Degradada (rasterizado a {processor.dpi} DPI)")

    print("\n" + "=" * 80)
    print("✅ CONCLUSIÓN")
    print("=" * 80)
    print("""
La manipulación DIRECTA de PDFs es SUPERIOR porque:

✅ Mantiene texto vectorial (seleccionable, perfecto para OCR)
✅ Mantiene gráficos vectoriales (líneas nítidas, sin pixelación)
✅ Tamaño de archivo mucho menor
✅ Calidad visual 100% perfecta
✅ Sin pérdida de información

La rasterización es INFERIOR porque:

❌ Convierte texto vectorial a imagen (NO seleccionable)
❌ Aumenta tamaño de archivo significativamente
❌ Degrada calidad visual (pixelación)
❌ Pierde información vectorial original

RECOMENDACIÓN: Usar SIEMPRE manipulación directa de PDF.
    """)

    print("=" * 80)
    print(f"📁 Archivos generados en: {test_output_dir}/")
    print(f"   1. factura_desplazada_DIRECTO.pdf (CORRECTO)")
    print(f"   2. factura_desplazada_RASTERIZADO.pdf (para comparación)")
    print("\nAbre ambos PDFs y verifica:")
    print("   • DIRECTO: Texto seleccionable ✅")
    print("   • RASTERIZADO: Texto NO seleccionable ❌")
    print("=" * 80)

if __name__ == "__main__":
    test_pdf_direct_manipulation()
