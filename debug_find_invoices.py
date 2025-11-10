#!/usr/bin/env python3
"""
Script de DEBUG para identificar por qué no se encuentran las facturas
"""
import os
from pathlib import Path

def debug_find_invoices(input_dir):
    """Debug detallado de la búsqueda de facturas"""

    print("="*70)
    print("🔍 DEBUG: Búsqueda de facturas")
    print("="*70)

    print(f"\n📁 INPUT_DIR proporcionado:")
    print(f"   Ruta: {input_dir}")
    print(f"   Tipo: {type(input_dir)}")

    # Verificar si input_dir existe
    if not os.path.exists(input_dir):
        print(f"   ❌ Esta ruta NO EXISTE")
        return
    else:
        print(f"   ✅ Esta ruta EXISTE")

    # Listar contenido de input_dir
    print(f"\n📂 Contenido de INPUT_DIR:")
    try:
        items = os.listdir(input_dir)
        for item in items:
            full_path = os.path.join(input_dir, item)
            tipo = "📁 DIR " if os.path.isdir(full_path) else "📄 FILE"
            print(f"   {tipo}: {item}")
    except Exception as e:
        print(f"   ❌ Error al listar: {e}")
        return

    # Verificar subdirectorios esperados
    print(f"\n🔍 Verificando subdirectorios esperados:")

    input_path = Path(input_dir)
    facturas_dir = input_path / 'facturas_procesadas'
    anotaciones_dir = input_path / 'anotaciones'

    print(f"\n   📁 facturas_procesadas/")
    print(f"      Ruta completa: {facturas_dir}")
    if facturas_dir.exists():
        print(f"      ✅ EXISTE")
        pdfs = list(facturas_dir.glob('*.pdf'))
        print(f"      PDFs encontrados: {len(pdfs)}")
        for pdf in pdfs:
            print(f"         • {pdf.name}")
    else:
        print(f"      ❌ NO EXISTE")

    print(f"\n   📁 anotaciones/")
    print(f"      Ruta completa: {anotaciones_dir}")
    if anotaciones_dir.exists():
        print(f"      ✅ EXISTE")
        jsons = list(anotaciones_dir.glob('*.json'))
        print(f"      JSONs encontrados: {len(jsons)}")
        for json_file in jsons:
            print(f"         • {json_file.name}")
    else:
        print(f"      ❌ NO EXISTE")

    # Buscar pares
    print(f"\n🔗 Buscando pares (PDF + JSON):")

    if not facturas_dir.exists() or not anotaciones_dir.exists():
        print(f"   ❌ No se pueden buscar pares porque faltan directorios")
        return

    pairs = []
    pdfs = list(facturas_dir.glob('*.pdf'))

    if len(pdfs) == 0:
        print(f"   ⚠️  No hay PDFs en facturas_procesadas/")
        return

    for pdf_file in pdfs:
        json_file = anotaciones_dir / f"{pdf_file.stem}.json"

        print(f"\n   PDF: {pdf_file.name}")
        print(f"      Buscando JSON: {json_file.name}")
        print(f"      Ruta JSON completa: {json_file}")

        if json_file.exists():
            print(f"      ✅ JSON ENCONTRADO")
            pairs.append((str(pdf_file), str(json_file)))
        else:
            print(f"      ❌ JSON NO ENCONTRADO")
            # Listar JSONs disponibles para comparar
            available_jsons = list(anotaciones_dir.glob('*.json'))
            print(f"      JSONs disponibles en anotaciones/:")
            for j in available_jsons:
                print(f"         • {j.name}")

    # Resultado final
    print(f"\n" + "="*70)
    print(f"📊 RESULTADO:")
    print(f"   Pares encontrados: {len(pairs)}")
    print("="*70)

    if len(pairs) == 0:
        print("\n❌ NO SE ENCONTRARON PARES")
        print("\n💡 POSIBLES CAUSAS:")
        print("   1. Los nombres de PDF y JSON no coinciden exactamente")
        print("   2. Los archivos están en ubicaciones incorrectas")
        print("   3. La ruta INPUT_DIR es incorrecta")
        print("   4. Permisos de lectura insuficientes")
    else:
        print("\n✅ PARES ENCONTRADOS:")
        for pdf, json_path in pairs:
            print(f"   • {Path(pdf).name} + {Path(json_path).name}")

    return pairs

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Uso: python debug_find_invoices.py <INPUT_DIR>")
        print("\nEjemplo:")
        print("  python debug_find_invoices.py '/content/drive/MyDrive/Temp_Prueba_CORREGIDA'")
        sys.exit(1)

    input_dir = sys.argv[1]
    debug_find_invoices(input_dir)
