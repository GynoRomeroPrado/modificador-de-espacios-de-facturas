# 📊 Ejemplos de Entrada y Salida

Este documento muestra ejemplos concretos de cómo funciona el sistema.

---

## 🎯 Ejemplo 1: Factura Normal (Minera Yanacocha)

### 📥 ENTRADA:

```
Datos extraidos de Originales/
├── facturas_procesadas/
│   └── IMG-20251026-WA0038.pdf
└── anotaciones/
    └── IMG-20251026-WA0038.json
```

**Contenido del JSON (simplificado):**
```json
{
  "tipo_documento": "FACTURA ELECTRONICA",
  "serie_completa": "F003-00015692",
  "emisor_razon_social": "MINERA YANACOCHA S.R.L.",
  "receptor_razon_social": "CONSULTORIA ENTRENAMIENTO Y SERVICIOS GROUP S.R.L.",
  "importe_total": 15753.76,
  "moneda": "SOLES",
  "items": [
    {
      "descripcion": "Servicio de Alimentación",
      "cantidad": 1.0,
      "importe_total_item": 15753.76
    }
  ]
}
```

### 📤 SALIDA:

```
facturas_con_margenes_modificados/
├── facturas_procesadas/
│   ├── IMG-20251026-WA0038.pdf                         ← Original (copia)
│   ├── IMG-20251026-WA0038_derecha_small.pdf          ← Desplazado 10px →
│   ├── IMG-20251026-WA0038_izquierda_small.pdf        ← Desplazado 10px ←
│   ├── IMG-20251026-WA0038_abajo_small.pdf            ← Desplazado 10px ↓
│   ├── IMG-20251026-WA0038_arriba_small.pdf           ← Desplazado 10px ↑
│   ├── IMG-20251026-WA0038_diagonal_dr_small.pdf      ← Desplazado 10px ↘
│   ├── IMG-20251026-WA0038_diagonal_dl_small.pdf      ← Desplazado 10px ↙
│   ├── IMG-20251026-WA0038_diagonal_ur_small.pdf      ← Desplazado 10px ↗
│   ├── IMG-20251026-WA0038_diagonal_ul_small.pdf      ← Desplazado 10px ↖
│   ├── IMG-20251026-WA0038_derecha_medium.pdf         ← Desplazado 20px →
│   ├── IMG-20251026-WA0038_izquierda_medium.pdf       ← Desplazado 20px ←
│   ├── IMG-20251026-WA0038_abajo_medium.pdf           ← Desplazado 20px ↓
│   ├── IMG-20251026-WA0038_arriba_medium.pdf          ← Desplazado 20px ↑
│   ├── IMG-20251026-WA0038_derecha_large.pdf          ← Desplazado 30px →
│   ├── IMG-20251026-WA0038_izquierda_large.pdf        ← Desplazado 30px ←
│   ├── IMG-20251026-WA0038_abajo_large.pdf            ← Desplazado 30px ↓
│   └── IMG-20251026-WA0038_arriba_large.pdf           ← Desplazado 30px ↑
│
└── anotaciones/
    ├── IMG-20251026-WA0038.json
    ├── IMG-20251026-WA0038_derecha_small.json
    ├── IMG-20251026-WA0038_izquierda_small.json
    └── ... (14 JSONs más con los mismos datos)
```

**Total: 17 PDFs + 17 JSONs = 34 archivos**

**Contenido de un JSON variado (ejemplo: `IMG-20251026-WA0038_derecha_small.json`):**
```json
{
  "tipo_documento": "FACTURA ELECTRONICA",
  "serie_completa": "F003-00015692",
  "emisor_razon_social": "MINERA YANACOCHA S.R.L.",
  "receptor_razon_social": "CONSULTORIA ENTRENAMIENTO Y SERVICIOS GROUP S.R.L.",
  "importe_total": 15753.76,
  "moneda": "SOLES",
  "items": [
    {
      "descripcion": "Servicio de Alimentación",
      "cantidad": 1.0,
      "importe_total_item": 15753.76
    }
  ]
}
```

**🔍 Nota:** El JSON es **idéntico** al original. Solo cambia el nombre del archivo.

---

## 🎯 Ejemplo 2: Factura de Hotel (Casa Andina)

### 📥 ENTRADA:

```
Datos extraidos de Originales/
├── facturas_procesadas/
│   └── 01-F023-00074322-CASA ANDINA PREMIUM MIRAFLORES_page-0001.pdf
└── anotaciones/
    └── 01-F023-00074322-CASA ANDINA PREMIUM MIRAFLORES_page-0001.json
```

**Contenido del JSON (simplificado):**
```json
{
  "tipo_documento": "FACTURA ELECTRONICA",
  "serie_completa": "F023-00074322",
  "emisor_razon_social": "NESSUS HOTELES PERU S.A.",
  "emisor_nombre_comercial": "CASA ANDINA",
  "receptor_razon_social": "MINERA YANACOCHA S.R.L.",
  "receptor_contacto": "IZQUIERDO ORTIZ,FERNANDO",
  "importe_total": 364.8,
  "moneda": "DOLARES AMERICANOS",
  "glosa": "ALOJAMIENTO",
  "items": [
    {
      "descripcion": "ALOJAMIENTO Transf.Conta/Transf.Account : YANACO",
      "cantidad": 1.0,
      "precio_unitario": 285.0,
      "importe_total_item": 364.8
    }
  ]
}
```

### 📤 SALIDA:

```
facturas_con_margenes_modificados/
├── facturas_procesadas/
│   ├── 01-F023-00074322-CASA ANDINA PREMIUM MIRAFLORES_page-0001.pdf
│   ├── 01-F023-00074322-CASA ANDINA PREMIUM MIRAFLORES_page-0001_derecha_small.pdf
│   ├── 01-F023-00074322-CASA ANDINA PREMIUM MIRAFLORES_page-0001_izquierda_small.pdf
│   ├── 01-F023-00074322-CASA ANDINA PREMIUM MIRAFLORES_page-0001_abajo_small.pdf
│   └── ... (13 variaciones más)
│
└── anotaciones/
    ├── 01-F023-00074322-CASA ANDINA PREMIUM MIRAFLORES_page-0001.json
    ├── 01-F023-00074322-CASA ANDINA PREMIUM MIRAFLORES_page-0001_derecha_small.json
    └── ... (15 JSONs más)
```

**Total: 17 PDFs + 17 JSONs = 34 archivos**

---

## 🎯 Ejemplo 3: Múltiples Facturas

### 📥 ENTRADA (3 facturas):

```
Datos extraidos de Originales/
├── facturas_procesadas/
│   ├── IMG-20251026-WA0038.pdf
│   ├── IMG-20251026-WA0039.pdf
│   └── 01-F020-00051515-COSTA DEL SOL WYNDHAM CAJAMARCA_page-0001.pdf
│
└── anotaciones/
    ├── IMG-20251026-WA0038.json
    ├── IMG-20251026-WA0039.json
    └── 01-F020-00051515-COSTA DEL SOL WYNDHAM CAJAMARCA_page-0001.json
```

**Total entrada: 3 PDFs + 3 JSONs = 6 archivos**

### 📤 SALIDA:

```
facturas_con_margenes_modificados/
├── facturas_procesadas/
│   ├── IMG-20251026-WA0038.pdf
│   ├── IMG-20251026-WA0038_derecha_small.pdf
│   ├── IMG-20251026-WA0038_izquierda_small.pdf
│   ├── ... (14 variaciones más de WA0038)
│   │
│   ├── IMG-20251026-WA0039.pdf
│   ├── IMG-20251026-WA0039_derecha_small.pdf
│   ├── IMG-20251026-WA0039_izquierda_small.pdf
│   ├── ... (14 variaciones más de WA0039)
│   │
│   ├── 01-F020-00051515-COSTA DEL SOL WYNDHAM CAJAMARCA_page-0001.pdf
│   ├── 01-F020-00051515-COSTA DEL SOL WYNDHAM CAJAMARCA_page-0001_derecha_small.pdf
│   └── ... (15 variaciones más de COSTA DEL SOL)
│
└── anotaciones/
    ├── (51 JSONs correspondientes a los 51 PDFs)
```

**Total salida: 51 PDFs + 51 JSONs = 102 archivos**

**Cálculo:** 3 facturas × 17 archivos por factura = 51 archivos (PDFs + JSONs)

---

## 📊 Tabla de Transformaciones

Estas son las **16 variaciones** que se generan por cada factura:

| # | Nombre Variación | Desplazamiento X | Desplazamiento Y | Dirección |
|---|------------------|------------------|------------------|-----------|
| 1 | `derecha_small` | +10px | 0 | → |
| 2 | `izquierda_small` | -10px | 0 | ← |
| 3 | `abajo_small` | 0 | +10px | ↓ |
| 4 | `arriba_small` | 0 | -10px | ↑ |
| 5 | `diagonal_dr_small` | +10px | +10px | ↘ |
| 6 | `diagonal_dl_small` | -10px | +10px | ↙ |
| 7 | `diagonal_ur_small` | +10px | -10px | ↗ |
| 8 | `diagonal_ul_small` | -10px | -10px | ↖ |
| 9 | `derecha_medium` | +20px | 0 | → |
| 10 | `izquierda_medium` | -20px | 0 | ← |
| 11 | `abajo_medium` | 0 | +20px | ↓ |
| 12 | `arriba_medium` | 0 | -20px | ↑ |
| 13 | `derecha_large` | +30px | 0 | → |
| 14 | `izquierda_large` | -30px | 0 | ← |
| 15 | `abajo_large` | 0 | +30px | ↓ |
| 16 | `arriba_large` | 0 | -30px | ↑ |

---

## 🔍 ¿Qué significa "desplazar"?

Cuando decimos "desplazamiento de 10px a la derecha", significa:

```
ORIGINAL:                    DESPLAZADO 10px →:
┌─────────────────┐         ┌─────────────────┐
│ FACTURA         │         │          FACTURA│
│ RUC: 20137...   │         │    RUC: 20137...│
│ Total: 15753.76 │         │  Total: 15753.76│
└─────────────────┘         └─────────────────┘
```

El contenido de la factura se **mueve** dentro del PDF, pero el tamaño del PDF sigue igual.

---

## 📁 Estructura de Reporte

Además de los PDFs y JSONs, se genera un reporte:

**Archivo:** `facturas_con_margenes_modificados/dataset_report.json`

```json
{
  "timestamp": "2025-11-09T22:30:15.123456",
  "input_directory": "/content/drive/MyDrive/Datos extraidos de Originales",
  "output_directory": "/content/drive/MyDrive/facturas_con_margenes_modificados",
  "statistics": {
    "original_invoices": 3,
    "augmented_invoices": 48,
    "total_invoices": 51,
    "errors": []
  },
  "augmentation_config": {
    "total_transformations": 16,
    "shift_levels": [10, 20, 30],
    "transformation_types": [
      "derecha_small",
      "izquierda_small",
      "abajo_small",
      "arriba_small",
      "diagonal_dr_small",
      "diagonal_dl_small",
      "diagonal_ur_small",
      "diagonal_ul_small",
      "derecha_medium",
      "izquierda_medium",
      "abajo_medium",
      "arriba_medium",
      "derecha_large",
      "izquierda_large",
      "abajo_large",
      "arriba_large"
    ]
  }
}
```

---

## 🎓 Caso de Uso Real

### Escenario:
Tienes 15 facturas para entrenar un modelo de IA que extrae datos de facturas.

### Problema:
15 facturas es muy poco para entrenar un modelo robusto.

### Solución:
Usar este sistema para generar variaciones:

```
ANTES:  15 facturas
DESPUÉS: 15 × 17 = 255 facturas

Multiplicador: 17x
```

### ¿Por qué funciona?
Al desplazar el contenido de la factura, el modelo aprende a:
- Detectar campos **en diferentes posiciones**
- No depender de **coordenadas fijas**
- Ser más **robusto** ante variaciones de formato

---

## 📊 Comparación de Tamaños

### Entrada (1 factura):
```
IMG-20251026-WA0038.pdf      380 KB
IMG-20251026-WA0038.json     3 KB
                             --------
Total:                       383 KB
```

### Salida (17 archivos):
```
17 PDFs × 380 KB =          6.5 MB
17 JSONs × 3 KB =           51 KB
                            --------
Total:                      6.5 MB
```

**Multiplicador de espacio:** ~17x

---

## ✅ Verificación de Resultados

Para verificar que todo salió bien, revisa:

### ✅ Checklist:

- [ ] Cada factura original tiene 16 variaciones
- [ ] Los nombres de archivos siguen el patrón: `NOMBRE_ORIGINAL_transformacion.pdf`
- [ ] Cada PDF tiene su JSON correspondiente con el mismo nombre
- [ ] El JSON mantiene todos los datos (items, cuotas, etc.)
- [ ] Existe el archivo `dataset_report.json`
- [ ] El reporte muestra 0 errores

### Comando para verificar (en Colab):

```python
import os
from pathlib import Path

output_dir = "/content/drive/MyDrive/facturas_con_margenes_modificados"
facturas_dir = Path(output_dir) / "facturas_procesadas"
anotaciones_dir = Path(output_dir) / "anotaciones"

num_pdfs = len(list(facturas_dir.glob("*.pdf")))
num_jsons = len(list(anotaciones_dir.glob("*.json")))

print(f"✅ PDFs generados: {num_pdfs}")
print(f"✅ JSONs generados: {num_jsons}")
print(f"✅ Iguales: {'Sí' if num_pdfs == num_jsons else 'NO'}")
```

---

**¡Ahora tienes ejemplos claros de cómo funciona el sistema! 🎉**
