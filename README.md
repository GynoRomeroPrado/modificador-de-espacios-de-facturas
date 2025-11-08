# 🚀 Data Augmentation para Facturas

Sistema de expansión de datasets de facturas mediante transformaciones geométricas (desplazamientos). Perfecto para aumentar datos de entrenamiento para modelos de detección de campos en facturas.

## ✨ Características

- ✅ **Mantiene nombres originales** de los archivos
- ✅ **Genera 16 variaciones** por cada factura (desplazamientos en diferentes direcciones)
- ✅ **Salida en PDF** (igual que entrada)
- ✅ **Estructura organizada** (facturas_procesadas/ y anotaciones/)
- ✅ **Control de cantidad** (procesa 1 factura para pruebas o todas)
- ✅ **Optimizado para Google Colab** (fácil integración con Google Drive)

## 📊 ¿Qué hace?

Por cada factura en tu dataset:
- **Entrada:** 1 PDF + 1 JSON
- **Salida:** 17 PDFs + 17 JSONs (1 original + 16 variaciones)

### Transformaciones aplicadas (16 variaciones):

| Tipo | Direcciones | Magnitudes |
|------|-------------|------------|
| **Horizontal** | derecha, izquierda | 10px, 20px, 30px |
| **Vertical** | arriba, abajo | 10px, 20px, 30px |
| **Diagonal** | 4 direcciones | 10px |

**Total:** 16 transformaciones

## 📁 Estructura de Datos

### Entrada esperada:
```
Datos extraidos de Originales/
├── facturas_procesadas/
│   ├── IMG-20251026-WA0038.pdf
│   ├── IMG-20251026-WA0039.pdf
│   └── ... (más PDFs)
└── anotaciones/
    ├── IMG-20251026-WA0038.json
    ├── IMG-20251026-WA0039.json
    └── ... (más JSONs)
```

### Salida generada:
```
facturas_con_margenes_modificados/
├── facturas_procesadas/
│   ├── IMG-20251026-WA0038.pdf                    # Original (copia)
│   ├── IMG-20251026-WA0038_derecha_small.pdf      # Variación
│   ├── IMG-20251026-WA0038_izquierda_small.pdf    # Variación
│   ├── IMG-20251026-WA0038_abajo_small.pdf        # Variación
│   ├── IMG-20251026-WA0038_arriba_small.pdf       # Variación
│   ├── IMG-20251026-WA0038_derecha_medium.pdf     # Variación
│   └── ... (11 variaciones más)
│
├── anotaciones/
│   ├── IMG-20251026-WA0038.json                   # Original (copia)
│   ├── IMG-20251026-WA0038_derecha_small.json     # Copia con nombre actualizado
│   └── ... (16 copias más)
│
└── dataset_report.json                             # Reporte del proceso
```

## 🎯 Uso en Google Colab (RECOMENDADO)

### Paso 1: Sube tus datos a Google Drive

Organiza tus archivos en Google Drive:
```
MyDrive/
└── Datos extraidos de Originales/
    ├── facturas_procesadas/  # Tus PDFs aquí
    └── anotaciones/          # Tus JSONs aquí
```

### Paso 2: Abre el Notebook

1. Abre el notebook: `notebooks/Invoice_Dataset_Augmentation.ipynb` en Google Colab
2. Sigue las instrucciones paso a paso
3. Configura las rutas de Google Drive
4. ¡Ejecuta!

### Ejemplo de configuración:
```python
# En la celda de configuración del notebook
INPUT_DIR = "/content/drive/MyDrive/Datos extraidos de Originales"
OUTPUT_DIR = "/content/drive/MyDrive/facturas_con_margenes_modificados"
MAX_INVOICES = 1  # Cambia a None para procesar todas
```

## 💻 Uso Local (Python Script)

### Instalación:

```bash
# Clonar repositorio
git clone https://github.com/GynoRomeroPrado/modificador-de-espacios-de-facturas.git
cd modificador-de-espacios-de-facturas

# Instalar dependencias
pip install -r requirements.txt

# Instalar poppler (necesario para pdf2image)
# Ubuntu/Debian:
sudo apt-get install poppler-utils

# macOS:
brew install poppler

# Windows: Descargar desde https://github.com/oschwartz10612/poppler-windows
```

### Uso básico:

```bash
# Procesar TODAS las facturas
python src/main.py "Datos extraidos de Originales" "facturas_con_margenes_modificados"

# Procesar solo 1 factura (para pruebas)
python src/main.py "Datos extraidos de Originales" "facturas_con_margenes_modificados" 1

# Procesar 5 facturas
python src/main.py "Datos extraidos de Originales" "facturas_con_margenes_modificados" 5
```

### Uso desde Python:

```python
from src.main import InvoiceDatasetAugmenter

# Crear augmenter
augmenter = InvoiceDatasetAugmenter(
    input_dir="Datos extraidos de Originales",
    output_dir="facturas_con_margenes_modificados",
    dpi=200,
    max_invoices=1  # None para procesar todas
)

# Procesar
stats = augmenter.process_dataset()

# Ver estadísticas
print(f"Facturas procesadas: {stats['original_invoices']}")
print(f"Variaciones generadas: {stats['augmented_invoices']}")
print(f"Total de archivos: {stats['total_invoices']}")
```

## 📋 Ejemplo de Output

Al ejecutar con 1 factura, verás:

```
============================================================
🚀 INICIANDO DATA AUGMENTATION DE FACTURAS
============================================================

📁 Creando estructura de directorios...

🔍 Buscando facturas en: Datos extraidos de Originales
✅ Procesando 1 de 15 facturas disponibles

============================================================
📋 PROCESANDO FACTURAS
============================================================

[1/1] Procesando: IMG-20251026-WA0038
  📥 Cargando PDF y JSON...
  💾 Guardando factura original...
  🔄 Generando 16 variaciones augmentadas...
  💾 Guardando variaciones...
  ✅ Completado: 1 original + 16 augmentadas = 17 archivos

📊 Reporte guardado en: facturas_con_margenes_modificados/dataset_report.json

============================================================
✅ PROCESO COMPLETADO
============================================================

📊 RESUMEN:
  • Facturas originales:     1
  • Facturas augmentadas:    16
  • Total de facturas:       17

🚀 Dataset expandido 17.0x
============================================================
```

## 🔧 Configuración Avanzada

### Modificar transformaciones:

Edita `src/augmentation.py` para cambiar las transformaciones:

```python
class AugmentationConfig:
    # Cambia las magnitudes de desplazamiento
    SHIFT_SMALL = 10   # Cambiar a 5, 15, etc.
    SHIFT_MEDIUM = 20  # Cambiar a 10, 25, etc.
    SHIFT_LARGE = 30   # Cambiar a 20, 40, etc.
```

### Modificar DPI de salida:

```python
augmenter = InvoiceDatasetAugmenter(
    input_dir="...",
    output_dir="...",
    dpi=300  # Más calidad, más pesado (default: 200)
)
```

## 📊 Formato de JSON

Los JSONs NO contienen bounding boxes, solo datos extraídos de la factura:

```json
{
  "tipo_documento": "FACTURA ELECTRÓNICA",
  "serie_completa": "F003-00015692",
  "fecha_emision": "2025-07-21",
  "moneda": "SOLES",
  "emisor_ruc": "20137291313",
  "emisor_razon_social": "MINERA YANACOCHA S.R.L.",
  "subtotal": 13350.64,
  "igv": 2403.12,
  "importe_total": 15753.76
}
```

## ❓ Preguntas Frecuentes

### ¿Por qué 16 variaciones y no más?

16 variaciones proporcionan un buen balance entre:
- Diversidad de datos (3 magnitudes × múltiples direcciones)
- Tiempo de procesamiento razonable
- Espacio en disco (17x expansión por factura)

### ¿Puedo usar imágenes PNG/JPG en lugar de PDF?

El sistema está optimizado para PDFs, pero puedes modificar `src/utils.py` para soportar otros formatos.

### ¿Qué pasa si tengo 100 facturas?

```
100 facturas × 17 = 1,700 archivos totales
Tiempo estimado: ~5-10 minutos (depende del DPI y tamaño)
Espacio en disco: ~500MB - 2GB (depende del DPI)
```

### ¿Los JSONs se modifican?

No, los JSONs se copian con el nombre actualizado pero el contenido permanece igual.

## 🤝 Contribuciones

¡Contribuciones son bienvenidas! Si encuentras bugs o tienes ideas para mejorar:

1. Abre un Issue describiendo el problema o mejora
2. Haz un Fork del repositorio
3. Crea un Pull Request con tus cambios

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver archivo `LICENSE` para más detalles.

## 📧 Contacto

- **GitHub:** [@GynoRomeroPrado](https://github.com/GynoRomeroPrado)
- **Repositorio:** [modificador-de-espacios-de-facturas](https://github.com/GynoRomeroPrado/modificador-de-espacios-de-facturas)

---

Hecho con ❤️ para mejorar datasets de facturas
