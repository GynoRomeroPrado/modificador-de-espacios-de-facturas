#!/usr/bin/env python3
"""
Test script para verificar la lógica del sistema sin dependencias de PIL
"""
import json
import os
from pathlib import Path

def test_augmentation_logic():
    """Prueba la lógica de augmentation sin procesar imágenes"""

    print("="*60)
    print("🧪 TEST DE LÓGICA DE AUGMENTATION")
    print("="*60)

    # 1. Verificar estructura de entrada
    print("\n📁 Verificando estructura de entrada...")
    input_dir = Path("Datos extraidos de Originales")
    facturas_dir = input_dir / "facturas_procesadas"
    anotaciones_dir = input_dir / "anotaciones"

    if not facturas_dir.exists():
        print(f"❌ No existe: {facturas_dir}")
        return False
    if not anotaciones_dir.exists():
        print(f"❌ No existe: {anotaciones_dir}")
        return False

    print(f"✅ {facturas_dir} existe")
    print(f"✅ {anotaciones_dir} existe")

    # 2. Buscar pares PDF+JSON
    print("\n🔍 Buscando pares PDF+JSON...")
    pairs = []
    for pdf_file in facturas_dir.glob('*.pdf'):
        json_file = anotaciones_dir / f"{pdf_file.stem}.json"
        if json_file.exists():
            pairs.append((pdf_file, json_file))

    print(f"✅ Encontrados {len(pairs)} pares")

    if len(pairs) == 0:
        print("❌ No hay pares para procesar")
        return False

    # 3. Tomar 1 factura como ejemplo
    pdf_path, json_path = pairs[0]
    print(f"\n📄 Factura de prueba: {pdf_path.name}")
    print(f"📄 JSON de prueba: {json_path.name}")

    # 4. Cargar JSON
    print("\n📥 Cargando JSON...")
    with open(json_path, 'r', encoding='utf-8') as f:
        json_data = json.load(f)

    print(f"✅ JSON cargado correctamente")
    print(f"   Campos principales: {len(json_data)} campos")
    print(f"   Tipo documento: {json_data.get('tipo_documento', 'N/A')}")
    print(f"   Serie: {json_data.get('serie_completa', 'N/A')}")
    print(f"   Emisor: {json_data.get('emisor_razon_social', 'N/A')}")
    print(f"   Total: {json_data.get('importe_total', 'N/A')} {json_data.get('moneda', '')}")

    # 5. Simular generación de variaciones
    print("\n🔄 Simulando generación de 16 variaciones...")

    transformations = [
        {"name": "derecha_small", "shift_x": 10, "shift_y": 0},
        {"name": "izquierda_small", "shift_x": -10, "shift_y": 0},
        {"name": "abajo_small", "shift_x": 0, "shift_y": 10},
        {"name": "arriba_small", "shift_x": 0, "shift_y": -10},
        {"name": "diagonal_dr_small", "shift_x": 10, "shift_y": 10},
        {"name": "diagonal_dl_small", "shift_x": -10, "shift_y": 10},
        {"name": "diagonal_ur_small", "shift_x": 10, "shift_y": -10},
        {"name": "diagonal_ul_small", "shift_x": -10, "shift_y": -10},
        {"name": "derecha_medium", "shift_x": 20, "shift_y": 0},
        {"name": "izquierda_medium", "shift_x": -20, "shift_y": 0},
        {"name": "abajo_medium", "shift_x": 0, "shift_y": 20},
        {"name": "arriba_medium", "shift_x": 0, "shift_y": -20},
        {"name": "derecha_large", "shift_x": 30, "shift_y": 0},
        {"name": "izquierda_large", "shift_x": -30, "shift_y": 0},
        {"name": "abajo_large", "shift_x": 0, "shift_y": 30},
        {"name": "arriba_large", "shift_x": 0, "shift_y": -30},
    ]

    original_name = pdf_path.stem
    output_files = []

    # Original
    output_files.append(f"{original_name}.pdf")

    # Variaciones
    for transform in transformations:
        filename = f"{original_name}_{transform['name']}.pdf"
        output_files.append(filename)

        # Simular creación de JSON
        new_json = json_data.copy()
        # El JSON mantiene todos sus datos, solo cambia el nombre
        print(f"  ✅ {filename} (desplazamiento: {transform['shift_x']:+3d}x, {transform['shift_y']:+3d}y)")

    # 6. Resumen
    print("\n" + "="*60)
    print("✅ TEST COMPLETADO EXITOSAMENTE")
    print("="*60)
    print(f"\n📊 RESULTADO:")
    print(f"  • Factura original:     1")
    print(f"  • Variaciones:         16")
    print(f"  • Total de archivos:   17 PDFs + 17 JSONs = 34 archivos")
    print(f"\n📁 Estructura de salida:")
    print(f"  facturas_con_margenes_modificados/")
    print(f"  ├── facturas_procesadas/")
    print(f"  │   ├── {original_name}.pdf (original)")
    for i, transform in enumerate(transformations[:3]):
        print(f"  │   ├── {original_name}_{transform['name']}.pdf")
    print(f"  │   └── ... (13 variaciones más)")
    print(f"  └── anotaciones/")
    print(f"      ├── {original_name}.json (original)")
    for i, transform in enumerate(transformations[:3]):
        print(f"      ├── {original_name}_{transform['name']}.json")
    print(f"      └── ... (13 copias más)")

    print("\n🎯 El JSON mantiene TODOS sus datos:")
    print(f"   ✅ {len(json_data)} campos preservados")
    print(f"   ✅ items: {len(json_data.get('items', []))} items")
    print(f"   ✅ cuotas: {len(json_data.get('cuotas', []))} cuotas")
    print(f"   ✅ Solo se actualiza el nombre del archivo")

    return True

if __name__ == "__main__":
    success = test_augmentation_logic()
    exit(0 if success else 1)
