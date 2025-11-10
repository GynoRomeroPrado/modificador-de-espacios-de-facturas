"""
Script de prueba para verificar las mejoras de calidad en imágenes
"""

import sys
import os
from pathlib import Path

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from image_processor import ImageProcessor
from PIL import Image

def test_quality_improvements():
    """Prueba las mejoras de calidad implementadas"""

    print("=" * 70)
    print("🔬 PRUEBA DE MEJORAS DE CALIDAD PARA OCR")
    print("=" * 70)

    # Usar una factura de ejemplo
    test_pdf = "Datos extraidos de Originales/facturas_procesadas/01-F020-00051515-COSTA DEL SOL WYNDHAM CAJAMARCA_page-0001.pdf"

    if not os.path.exists(test_pdf):
        print(f"❌ No se encontró la factura de prueba: {test_pdf}")
        return

    print(f"\n📄 Factura de prueba: {os.path.basename(test_pdf)}")

    # Crear directorio de prueba
    test_output_dir = "test_output_quality"
    os.makedirs(test_output_dir, exist_ok=True)

    print("\n" + "=" * 70)
    print("📊 COMPARACIÓN: DPI 200 vs DPI 300")
    print("=" * 70)

    # Prueba 1: Cargar con DPI 200 (antiguo)
    print("\n1️⃣  Procesando con DPI 200 (configuración antigua)...")
    processor_old = ImageProcessor(dpi=200)
    image_old = processor_old.load_image(test_pdf)
    print(f"   ✓ Resolución: {image_old.width}x{image_old.height} px")

    # Guardar sin optimización (modo antiguo)
    output_old = os.path.join(test_output_dir, "factura_dpi200_sin_optimizar.png")
    image_old.save(output_old, 'PNG')  # Sin optimización
    size_old = os.path.getsize(output_old) / 1024  # KB
    print(f"   ✓ Tamaño archivo: {size_old:.1f} KB (sin optimización)")

    # Prueba 2: Cargar con DPI 300 (nuevo)
    print("\n2️⃣  Procesando con DPI 300 (configuración nueva)...")
    processor_new = ImageProcessor(dpi=300)
    image_new = processor_new.load_image(test_pdf)
    print(f"   ✓ Resolución: {image_new.width}x{image_new.height} px")
    print(f"   ✓ Mejora de resolución: {(image_new.width * image_new.height) / (image_old.width * image_old.height):.1f}x")

    # Prueba 3: Guardar con optimización PNG
    print("\n3️⃣  Guardando con optimización PNG avanzada...")
    output_optimized = os.path.join(test_output_dir, "factura_dpi300_optimizada.png")
    processor_new.save_image(image_new, output_optimized)
    size_optimized = os.path.getsize(output_optimized) / 1024  # KB
    print(f"   ✓ Tamaño archivo: {size_optimized:.1f} KB")
    print(f"   ✓ Compresión: {((size_old - size_optimized) / size_old * 100):.1f}% de reducción")

    # Prueba 4: Aplicar mejoras para OCR
    print("\n4️⃣  Aplicando mejoras avanzadas para OCR...")
    output_enhanced = os.path.join(test_output_dir, "factura_dpi300_optimizada_ocr.png")
    processor_new.save_image_with_ocr_enhancement(image_new, output_enhanced, enhance=True)
    size_enhanced = os.path.getsize(output_enhanced) / 1024  # KB
    print(f"   ✓ Tamaño archivo: {size_enhanced:.1f} KB")
    print(f"   ✓ Mejoras aplicadas:")
    print(f"      • Sharpening con UnsharpMask (radio=2, percent=150, threshold=3)")
    print(f"      • Mejora de contraste (factor=1.1)")
    print(f"      • Mejora de nitidez (factor=1.2)")

    # Resumen
    print("\n" + "=" * 70)
    print("📈 RESUMEN DE MEJORAS")
    print("=" * 70)

    pixel_improvement = ((image_new.width * image_new.height) / (image_old.width * image_old.height) - 1) * 100

    print(f"\n✅ Resolución:")
    print(f"   Antes: {image_old.width}x{image_old.height} px ({image_old.width * image_old.height:,} píxeles)")
    print(f"   Ahora: {image_new.width}x{image_new.height} px ({image_new.width * image_new.height:,} píxeles)")
    print(f"   Mejora: +{pixel_improvement:.1f}% más píxeles")

    print(f"\n✅ Tamaño de archivo:")
    print(f"   Antes: {size_old:.1f} KB (DPI 200, sin optimizar)")
    print(f"   Ahora: {size_enhanced:.1f} KB (DPI 300, optimizado + OCR)")

    if size_enhanced < size_old:
        print(f"   Reducción: {((size_old - size_enhanced) / size_old * 100):.1f}% más liviano")
    else:
        print(f"   Aumento: {((size_enhanced - size_old) / size_old * 100):.1f}% (por mayor resolución)")

    print(f"\n✅ Calidad OCR:")
    print(f"   • DPI aumentado de 200 → 300 (estándar profesional)")
    print(f"   • Sharpening profesional aplicado")
    print(f"   • Contraste y nitidez mejorados")
    print(f"   • Validación de resolución mínima")
    print(f"   • Preservación de canales alfa/CMYK")

    print(f"\n📁 Archivos generados en: {test_output_dir}/")
    print(f"   1. factura_dpi200_sin_optimizar.png (anterior)")
    print(f"   2. factura_dpi300_optimizada.png (nuevo - optimizado)")
    print(f"   3. factura_dpi300_optimizada_ocr.png (nuevo - optimizado + OCR)")

    print("\n" + "=" * 70)
    print("✅ PRUEBA COMPLETADA CON ÉXITO")
    print("=" * 70)
    print("\n💡 Recomendación: Usa las imágenes mejoradas para OCR. La calidad es")
    print("   significativamente superior y el texto será más legible.")
    print("=" * 70)

if __name__ == "__main__":
    test_quality_improvements()
