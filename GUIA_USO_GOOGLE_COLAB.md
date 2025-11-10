# 📘 Guía Completa de Uso - Google Colab

## 🎯 ¿Qué hace este sistema?

Este sistema toma tus facturas en PDF y genera **variaciones con márgenes modificados** para entrenar modelos de IA.

### Ejemplo visual:

```
ENTRADA (1 factura):
📄 IMG-20251026-WA0038.pdf
📄 IMG-20251026-WA0038.json

SALIDA (17 archivos por factura):
📄 IMG-20251026-WA0038.pdf                      ← Original (copia)
📄 IMG-20251026-WA0038_derecha_small.pdf        ← Contenido desplazado 10px a la derecha
📄 IMG-20251026-WA0038_izquierda_small.pdf      ← Contenido desplazado 10px a la izquierda
📄 IMG-20251026-WA0038_abajo_small.pdf          ← Contenido desplazado 10px hacia abajo
📄 IMG-20251026-WA0038_arriba_small.pdf         ← Contenido desplazado 10px hacia arriba
... (12 variaciones más con 20px y 30px)

+ 17 JSONs correspondientes (copias exactas con nombre actualizado)
```

---

## 📋 PASO 1: Preparar tus datos en Google Drive

### 1.1. Estructura requerida

Crea esta estructura en tu Google Drive:

```
MyDrive/
└── Datos extraidos de Originales/
    ├── facturas_procesadas/
    │   ├── IMG-20251026-WA0038.pdf
    │   ├── IMG-20251026-WA0039.pdf
    │   ├── 01-F020-00051515-COSTA DEL SOL WYNDHAM CAJAMARCA_page-0001.pdf
    │   └── ... (más PDFs)
    │
    └── anotaciones/
        ├── IMG-20251026-WA0038.json
        ├── IMG-20251026-WA0039.json
        ├── 01-F020-00051515-COSTA DEL SOL WYNDHAM CAJAMARCA_page-0001.json
        └── ... (más JSONs)
```

**IMPORTANTE:**
- ✅ Cada PDF debe tener su JSON con el **mismo nombre**
- ✅ Los JSONs deben estar en la carpeta `anotaciones/`
- ✅ Los PDFs deben estar en la carpeta `facturas_procesadas/`

### 1.2. Verificar tus archivos

Asegúrate que:
1. Cada PDF tenga su JSON correspondiente
2. Los nombres coincidan exactamente (sin extensión)
3. Los JSONs contengan los datos extraídos de la factura

Ejemplo de JSON válido:
```json
{
  "tipo_documento": "FACTURA ELECTRONICA",
  "serie_completa": "F003-00015692",
  "emisor_ruc": "20137291313",
  "emisor_razon_social": "MINERA YANACOCHA S.R.L.",
  "importe_total": 15753.76,
  "items": [
    {
      "descripcion": "Servicio de Alimentación",
      "cantidad": 1.0,
      "importe_total_item": 15753.76
    }
  ],
  "cuotas": [
    {
      "numero": 1,
      "monto": 15753.76,
      "fecha_vencimiento": "2025-08-20"
    }
  ]
}
```

---

## 📋 PASO 2: Abrir Google Colab

### 2.1. Ir a Google Colab

1. Abre tu navegador
2. Ve a: **https://colab.research.google.com/**
3. Inicia sesión con tu cuenta de Google

### 2.2. Subir el Notebook

**Opción A - Desde GitHub:**
1. En Colab, haz clic en `Archivo` → `Abrir notebook`
2. Ve a la pestaña `GitHub`
3. Pega esta URL: `https://github.com/GynoRomeroPrado/modificador-de-espacios-de-facturas`
4. Selecciona: `notebooks/Invoice_Dataset_Augmentation.ipynb`

**Opción B - Subir directamente:**
1. Descarga el notebook desde el repositorio
2. En Colab, haz clic en `Archivo` → `Subir notebook`
3. Selecciona el archivo `Invoice_Dataset_Augmentation.ipynb`

---

## 📋 PASO 3: Ejecutar el Notebook (Paso a Paso)

### 3.1. Ejecutar Celda 1: Instalación de dependencias

```python
# Celda 1 - Instalación
!pip install -q Pillow pdf2image numpy
!apt-get install -qq poppler-utils

print("✅ Dependencias instaladas")
```

**Qué hace:** Instala las librerías necesarias para procesar PDFs
**Tiempo:** ~30 segundos
**Salida esperada:** `✅ Dependencias instaladas`

---

### 3.2. Ejecutar Celda 2: Montar Google Drive

```python
# Celda 2 - Montar Drive
from google.colab import drive
drive.mount('/content/drive')

print("✅ Google Drive montado")
```

**Qué hace:** Conecta tu Google Drive con Colab
**Tiempo:** ~5 segundos
**Acción requerida:**
1. Aparecerá un enlace
2. Haz clic en el enlace
3. Selecciona tu cuenta de Google
4. Copia el código de autorización
5. Pégalo en Colab

**Salida esperada:** `Mounted at /content/drive`

---

### 3.3. Ejecutar Celda 3: Clonar repositorio

```python
# Celda 3 - Clonar código
!git clone https://github.com/GynoRomeroPrado/modificador-de-espacios-de-facturas.git
%cd modificador-de-espacios-de-facturas

print("✅ Repositorio clonado")
```

**Qué hace:** Descarga el código del sistema
**Tiempo:** ~10 segundos
**Salida esperada:** Mensajes de git clonando el repositorio

---

### 3.4. Ejecutar Celda 4: **CONFIGURACIÓN IMPORTANTE** ⚠️

```python
# Celda 4 - CONFIGURA ESTAS RUTAS
# ========================================
# ⚙️ CONFIGURA ESTAS RUTAS
# ========================================

# Directorio con tus facturas originales en Google Drive
INPUT_DIR = "/content/drive/MyDrive/Datos extraidos de Originales"

# Directorio donde guardar el dataset augmentado
OUTPUT_DIR = "/content/drive/MyDrive/facturas_con_margenes_modificados"

# DPI para convertir PDFs a imágenes (mayor = mejor calidad, más pesado)
DPI = 200

# Número máximo de facturas a procesar (None = todas, 1 = solo una para pruebas)
MAX_INVOICES = 1  # ⚠️ CAMBIA ESTO SEGÚN NECESITES

print("✅ CONFIGURACIÓN:")
print(f"📁 Input:         {INPUT_DIR}")
print(f"📁 Output:        {OUTPUT_DIR}")
print(f"🔧 DPI:           {DPI}")
print(f"📊 Max facturas:  {MAX_INVOICES or 'Todas'}")
```

**⚠️ IMPORTANTE - Modifica estas rutas:**

1. **INPUT_DIR:** Ruta donde están tus facturas originales
   - Si tu carpeta se llama diferente, cámbiala aquí
   - Ejemplo: `"/content/drive/MyDrive/Mis Facturas"`

2. **OUTPUT_DIR:** Ruta donde se guardarán los resultados
   - Puedes cambiarle el nombre si quieres
   - Ejemplo: `"/content/drive/MyDrive/Facturas Procesadas 2025"`

3. **MAX_INVOICES:** Cuántas facturas procesar
   - `1` → Solo procesa 1 factura (para pruebas)
   - `5` → Procesa 5 facturas
   - `None` → Procesa TODAS las facturas

**Salida esperada:**
```
✅ CONFIGURACIÓN:
📁 Input:         /content/drive/MyDrive/Datos extraidos de Originales
📁 Output:        /content/drive/MyDrive/facturas_con_margenes_modificados
🔧 DPI:           200
📊 Max facturas:  1
```

---

### 3.5. Ejecutar Celda 5: Verificar estructura

```python
# Celda 5 - Verificar estructura
import os
from pathlib import Path

# (código de verificación...)
```

**Qué hace:** Verifica que tus archivos estén correctamente organizados
**Tiempo:** ~2 segundos

**Salida esperada (exitosa):**
```
✅ Directorio encontrado: /content/drive/MyDrive/Datos extraidos de Originales

📊 Contenido:
  • PDFs en facturas_procesadas: 15
  • JSONs en anotaciones:        15
  • Pares completos (PDF+JSON):  15

✅ Listo para procesar 1 factura(s)
   Resultado esperado: 1 × 17 = 17 archivos (PDFs + JSONs)
```

**Si sale error:**
```
❌ ERROR: No existe /content/drive/.../facturas_procesadas
   Debe existir la carpeta 'facturas_procesadas' con los PDFs
```
→ Revisa que la carpeta exista y la ruta sea correcta en INPUT_DIR

---

### 3.6. Ejecutar Celda 6: **PROCESAR FACTURAS** 🚀

```python
# Celda 6 - Procesar
import sys
sys.path.append('/content/modificador-de-espacios-de-facturas/src')

from main import InvoiceDatasetAugmenter

# Crear augmenter
augmenter = InvoiceDatasetAugmenter(
    input_dir=INPUT_DIR,
    output_dir=OUTPUT_DIR,
    dpi=DPI,
    max_invoices=MAX_INVOICES
)

# Procesar dataset
stats = augmenter.process_dataset()
```

**Qué hace:** ¡PROCESA TUS FACTURAS! Esta es la celda principal
**Tiempo:**
- 1 factura: ~10-20 segundos
- 15 facturas: ~3-5 minutos

**Salida esperada:**
```
============================================================
🚀 INICIANDO DATA AUGMENTATION DE FACTURAS
============================================================

📁 Creando estructura de directorios...

🔍 Buscando facturas en: /content/drive/MyDrive/Datos extraidos de Originales
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

📊 Reporte guardado en: .../dataset_report.json

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

---

### 3.7. Ejecutar Celda 7: Verificar resultados

```python
# Celda 7 - Verificar resultados
# (código para listar archivos generados...)
```

**Qué hace:** Muestra los archivos que se generaron
**Salida esperada:**
```
📁 ARCHIVOS GENERADOS

📂 facturas_procesadas/ (17 PDFs)
  • IMG-20251026-WA0038.pdf
  • IMG-20251026-WA0038_abajo_large.pdf
  • IMG-20251026-WA0038_abajo_medium.pdf
  • IMG-20251026-WA0038_abajo_small.pdf
  • IMG-20251026-WA0038_arriba_large.pdf
  ... (12 más)

📂 anotaciones/ (17 JSONs)
  • IMG-20251026-WA0038.json
  • IMG-20251026-WA0038_abajo_large.json
  ... (15 más)
```

---

### 3.8. (Opcional) Celda 8: Visualizar ejemplos

```python
# Celda 8 - Visualizar
# (código para mostrar imágenes...)
```

**Qué hace:** Muestra visualmente algunas facturas generadas
**Salida esperada:** 4 imágenes de facturas con diferentes desplazamientos

---

## 📋 PASO 4: Ver los resultados en Google Drive

1. Ve a tu Google Drive
2. Navega a: `MyDrive/facturas_con_margenes_modificados/`
3. Verás esta estructura:

```
facturas_con_margenes_modificados/
├── facturas_procesadas/
│   ├── IMG-20251026-WA0038.pdf                    (original)
│   ├── IMG-20251026-WA0038_derecha_small.pdf      (variación)
│   ├── IMG-20251026-WA0038_izquierda_small.pdf    (variación)
│   └── ... (14 variaciones más)
│
├── anotaciones/
│   ├── IMG-20251026-WA0038.json                   (original)
│   ├── IMG-20251026-WA0038_derecha_small.json     (copia)
│   └── ... (16 copias más)
│
└── dataset_report.json                             (reporte)
```

---

## 🎯 PASO 5: Procesar TODAS tus facturas

Una vez que verificaste que funciona con 1 factura:

1. **Vuelve a la Celda 4** (Configuración)
2. **Cambia esta línea:**
   ```python
   MAX_INVOICES = 1  # ← Cambiar a None
   ```
   Por:
   ```python
   MAX_INVOICES = None  # ← Procesa TODAS
   ```
3. **Ejecuta de nuevo desde Celda 5 hasta Celda 7**

**Resultado final:**
- Si tienes 15 facturas → `15 × 17 = 255 archivos totales`

---

## ❓ Preguntas Frecuentes

### ❓ ¿Cuánto espacio ocupa?
- 1 factura genera ~17 archivos
- Cada archivo PDF: ~300-500 KB
- Total por factura: ~5-10 MB
- 15 facturas: ~75-150 MB

### ❓ ¿Cuánto tiempo tarda?
- 1 factura: 10-20 segundos
- 15 facturas: 3-5 minutos
- Depende del tamaño de los PDFs y DPI

### ❓ ¿Puedo cambiar los desplazamientos?
Sí, edita el archivo `src/augmentation.py`:
```python
SHIFT_SMALL = 10   # Cambiar a 5, 15, etc.
SHIFT_MEDIUM = 20  # Cambiar a 10, 25, etc.
SHIFT_LARGE = 30   # Cambiar a 20, 40, etc.
```

### ❓ ¿Los JSONs se modifican?
No, solo se copia el JSON y se actualiza el nombre del archivo para que coincida con el PDF generado. Todos los datos internos (items, cuotas, campos) se mantienen intactos.

### ❓ ¿Qué pasa si se interrumpe el proceso?
Puedes volver a ejecutar. El sistema sobrescribirá los archivos que ya existan.

### ❓ ¿Puedo procesar facturas de hoteles y normales juntas?
Sí, el sistema procesa ambos tipos por igual. No hace distinción.

---

## 🎓 Ejemplo Completo (Paso a Paso Visual)

### Antes de ejecutar:
```
📁 Google Drive
└── MyDrive/
    └── Datos extraidos de Originales/
        ├── facturas_procesadas/
        │   └── FACTURA-001.pdf (1 archivo)
        └── anotaciones/
            └── FACTURA-001.json (1 archivo)
```

### Después de ejecutar con MAX_INVOICES=1:
```
📁 Google Drive
└── MyDrive/
    ├── Datos extraidos de Originales/  (sin cambios)
    │
    └── facturas_con_margenes_modificados/  (NUEVO)
        ├── facturas_procesadas/
        │   ├── FACTURA-001.pdf                    (original)
        │   ├── FACTURA-001_derecha_small.pdf      (10px →)
        │   ├── FACTURA-001_izquierda_small.pdf    (10px ←)
        │   ├── FACTURA-001_abajo_small.pdf        (10px ↓)
        │   ├── FACTURA-001_arriba_small.pdf       (10px ↑)
        │   ├── FACTURA-001_diagonal_dr_small.pdf  (10px ↘)
        │   ├── FACTURA-001_diagonal_dl_small.pdf  (10px ↙)
        │   ├── FACTURA-001_diagonal_ur_small.pdf  (10px ↗)
        │   ├── FACTURA-001_diagonal_ul_small.pdf  (10px ↖)
        │   ├── FACTURA-001_derecha_medium.pdf     (20px →)
        │   ├── FACTURA-001_izquierda_medium.pdf   (20px ←)
        │   ├── FACTURA-001_abajo_medium.pdf       (20px ↓)
        │   ├── FACTURA-001_arriba_medium.pdf      (20px ↑)
        │   ├── FACTURA-001_derecha_large.pdf      (30px →)
        │   ├── FACTURA-001_izquierda_large.pdf    (30px ←)
        │   ├── FACTURA-001_abajo_large.pdf        (30px ↓)
        │   └── FACTURA-001_arriba_large.pdf       (30px ↑)
        │
        ├── anotaciones/
        │   ├── FACTURA-001.json                   (original)
        │   ├── FACTURA-001_derecha_small.json
        │   └── ... (16 JSONs más)
        │
        └── dataset_report.json
```

**Total: 17 PDFs + 17 JSONs + 1 reporte = 35 archivos**

---

## 🚨 Solución de Problemas

### Error: "No se encontró el directorio"
```
❌ Error: No se encontró el directorio .../facturas_procesadas
```
**Solución:**
1. Verifica que montaste Google Drive (Celda 2)
2. Verifica que la ruta en INPUT_DIR es correcta
3. Verifica que la carpeta `facturas_procesadas/` existe

### Error: "No se encontraron pares"
```
❌ No se encontraron pares de facturas (PDF + JSON)
```
**Solución:**
1. Verifica que cada PDF tenga su JSON con el mismo nombre
2. Verifica que los archivos estén en las carpetas correctas

### Error: "ModuleNotFoundError: No module named 'PIL'"
```
ModuleNotFoundError: No module named 'PIL'
```
**Solución:**
Ejecuta de nuevo la Celda 1 (Instalación de dependencias)

### El proceso tarda mucho
**Solución:**
1. Reduce DPI a 150 (menos calidad, más rápido)
2. Procesa menos facturas primero (MAX_INVOICES=5)

---

## 📞 ¿Necesitas ayuda?

Si tienes problemas, abre un Issue en GitHub:
https://github.com/GynoRomeroPrado/modificador-de-espacios-de-facturas/issues

---

**¡Listo! Ahora tienes todo lo necesario para usar el sistema desde Google Colab 🚀**
