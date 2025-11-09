# ESTRUCTURA JSON DEFINITIVA PARA FACTURAS

## 1. ANÁLISIS DE NECESIDADES

Una factura típica tiene:
- **Datos de cabecera** (1 vez): emisor, receptor, fechas, totales
- **Datos de items/líneas** (N veces): productos o servicios con sus cantidades, precios

## 2. ESTRUCTURA PROPUESTA

```json
{
  "tipo_documento": "FACTURA ELECTRONICA",
  "serie_completa": "F001-00000123",
  "fecha_emision": "2025-01-15",
  "fecha_vencimiento": "2025-02-14",
  "moneda": "SOLES",

  "emisor": {
    "ruc": "20123456789",
    "razon_social": "EMPRESA EJEMPLO S.A.C.",
    "nombre_comercial": "EJEMPLO",
    "direccion": "AV. PRINCIPAL 123",
    "telefono": "01-1234567",
    "email": "contacto@ejemplo.com"
  },

  "receptor": {
    "numero_documento": "20987654321",
    "tipo_documento": "RUC",
    "razon_social": "CLIENTE EJEMPLO S.R.L.",
    "direccion": "JR. COMERCIO 456"
  },

  "items": [
    {
      "numero_linea": 1,
      "codigo": "PROD001",
      "descripcion": "Producto ejemplo 1",
      "cantidad": 10.0,
      "unidad_medida": "UND",
      "precio_unitario": 100.00,
      "valor_venta": 1000.00,
      "igv_item": 180.00,
      "precio_total": 1180.00
    },
    {
      "numero_linea": 2,
      "codigo": "SERV002",
      "descripcion": "Servicio ejemplo 2",
      "cantidad": 5.0,
      "unidad_medida": "HRS",
      "precio_unitario": 50.00,
      "valor_venta": 250.00,
      "igv_item": 45.00,
      "precio_total": 295.00
    }
  ],

  "totales": {
    "subtotal": 1250.00,
    "descuento": 0.00,
    "base_imponible": 1250.00,
    "igv": 225.00,
    "otros_cargos": 0.00,
    "importe_total": 1475.00
  },

  "referencias": {
    "numero_contrato": null,
    "orden_compra": "OC-2025-001",
    "guia_remision": "T001-00000123",
    "condicion_pago": "Credito 30 dias"
  },

  "adicionales": {
    "observaciones": "Observaciones adicionales",
    "glosa": "Descripción general de la operación",
    "detraccion_porcentaje": 10.0,
    "detraccion_monto": 147.50
  }
}
```

## 3. ESTRUCTURA ACTUAL (Flat/Plana) vs ESTRUCTURA PROPUESTA (Agrupada)

### ACTUAL (Flat):
```json
{
  "tipo_documento": "...",
  "emisor_ruc": "...",
  "emisor_razon_social": "...",
  "emisor_nombre_comercial": "...",
  "receptor_numero_doc": "...",
  "receptor_tipo_doc": "...",
  "subtotal": 123.45,
  "igv": 22.22,
  "items": [...]
}
```

**Pros:**
- Simple de leer
- Fácil de buscar campos individuales
- Menos anidamiento

**Contras:**
- 29 campos en el nivel raíz (difícil de mantener)
- No hay separación lógica de conceptos
- Nombres de campos largos con prefijos (emisor_*, receptor_*)

### PROPUESTA (Agrupada):
```json
{
  "tipo_documento": "...",
  "emisor": {
    "ruc": "...",
    "razon_social": "..."
  },
  "receptor": {...},
  "items": [...],
  "totales": {...},
  "referencias": {...},
  "adicionales": {...}
}
```

**Pros:**
- Organización lógica por secciones
- Más fácil de extender (agregar campos nuevos)
- Nombres de campos cortos sin prefijos
- Estándar común en APIs REST

**Contras:**
- Requiere un nivel más de anidamiento
- Consultas ligeramente más complejas (ej: `emisor.ruc` en vez de `emisor_ruc`)

## 4. RECOMENDACIÓN: MANTENER ESTRUCTURA FLAT

**Después de analizar ambas opciones, RECOMIENDO MANTENER la estructura FLAT (actual) por las siguientes razones:**

### Razones técnicas:
1. **Compatibilidad**: Si ya tienes código que lee los JSON actuales, cambiar la estructura lo romperá
2. **Simplicidad de consultas**: En bases de datos SQL o análisis con pandas, `emisor_ruc` es más directo que `emisor.ruc`
3. **Exportación a CSV**: La estructura flat se exporta directamente a tablas relacionales
4. **Menos errores**: No hay riesgo de olvidar niveles de anidamiento

### Razones prácticas:
1. Ya tienes facturas procesadas con la estructura actual
2. El único cambio real necesario es agregar el campo `items`
3. La estructura flat es suficientemente clara con los prefijos

## 5. ESTRUCTURA DEFINITIVA RECOMENDADA (Flat + Items)

```json
{
  // DOCUMENTO
  "tipo_documento": "FACTURA ELECTRONICA",
  "serie_completa": "F001-00000123",
  "fecha_emision": "2025-01-15",
  "fecha_vencimiento": "2025-02-14",
  "moneda": "SOLES",

  // EMISOR (6 campos)
  "emisor_ruc": "20123456789",
  "emisor_razon_social": "EMPRESA EJEMPLO S.A.C.",
  "emisor_nombre_comercial": "EJEMPLO",
  "emisor_direccion": "AV. PRINCIPAL 123 LIMA-LIMA-MIRAFLORES",
  "emisor_telefono": "01-1234567",
  "emisor_email": "contacto@ejemplo.com",

  // RECEPTOR (4 campos)
  "receptor_numero_doc": "20987654321",
  "receptor_tipo_doc": "RUC",
  "receptor_razon_social": "CLIENTE EJEMPLO S.R.L.",
  "receptor_direccion": "JR. COMERCIO 456 LIMA-LIMA-SURCO",

  // TOTALES (5 campos)
  "subtotal": 1250.00,
  "igv": 225.00,
  "importe_total": 1475.00,
  "descuento": 0.00,
  "otros_cargos": 0.00,

  // REFERENCIAS (4 campos)
  "numero_contrato": null,
  "orden_compra": "OC-2025-001",
  "guia_remision": "T001-00000123",
  "condicion_pago": "Credito 30 dias",

  // ADICIONALES (4 campos)
  "observaciones": "SON: MIL CUATROCIENTOS SETENTA Y CINCO CON 00/100 SOLES",
  "glosa": "Venta de productos varios",
  "detraccion_porcentaje": 10.0,
  "detraccion_monto": 147.50,

  // ITEMS (ARRAY - puede tener N elementos)
  "items": [
    {
      "item": 1,
      "codigo": "PROD001",
      "descripcion": "Producto ejemplo 1 - Descripción detallada",
      "cantidad": 10.0,
      "unidad_medida": "UND",
      "precio_unitario": 100.00,
      "valor_venta": 1000.00,
      "igv_item": 180.00,
      "precio_total": 1180.00
    },
    {
      "item": 2,
      "codigo": "SERV002",
      "descripcion": "Servicio ejemplo 2",
      "cantidad": 5.0,
      "unidad_medida": "HRS",
      "precio_unitario": 50.00,
      "valor_venta": 250.00,
      "igv_item": 45.00,
      "precio_total": 295.00
    }
  ]
}
```

## 6. CAMPOS DE ITEMS - DEFINICIÓN DETALLADA

Cada elemento del array `items` debe tener:

| Campo | Tipo | Descripción | Ejemplo | Obligatorio |
|-------|------|-------------|---------|-------------|
| `item` | number | Número de línea secuencial (1, 2, 3...) | 1 | Sí |
| `codigo` | string/null | Código del producto/servicio | "PROD001" | No (puede ser null) |
| `descripcion` | string | Descripción completa del item | "Gasolina 90 Octanos" | Sí |
| `cantidad` | number | Cantidad numérica | 10.5 | Sí |
| `unidad_medida` | string | Unidad (UND, KG, M, GAL, etc.) | "GAL" | Sí |
| `precio_unitario` | number | Precio por unidad SIN IGV | 15.50 | Sí |
| `valor_venta` | number | Total de la línea SIN IGV (cantidad × precio_unitario) | 162.75 | Sí |
| `igv_item` | number | IGV de esta línea específica | 29.30 | Sí |
| `precio_total` | number | Total de la línea CON IGV (valor_venta + igv_item) | 192.05 | Sí |

### Notas importantes sobre items:
1. **Número de item (`item`)**: Agregar este campo para facilitar el orden y referencia
2. **Código puede ser null**: Muchas facturas no tienen código de producto
3. **Validación matemática**:
   - `valor_venta = cantidad × precio_unitario`
   - `igv_item = valor_venta × 0.18` (para Perú)
   - `precio_total = valor_venta + igv_item`
4. **Descripción completa**: Debe incluir toda la información de la línea

## 7. CASOS ESPECIALES

### Caso 1: Factura sin items (raro pero posible)
```json
{
  ...
  "items": []
}
```

### Caso 2: Factura con 1 solo item (servicios simples)
```json
{
  ...
  "items": [
    {
      "item": 1,
      "codigo": null,
      "descripcion": "Servicio de transporte de carga",
      "cantidad": 1.0,
      "unidad_medida": "ZZ",
      "precio_unitario": 100.00,
      "valor_venta": 100.00,
      "igv_item": 18.00,
      "precio_total": 118.00
    }
  ]
}
```

### Caso 3: Factura con muchos items (supermercado, ferreterías)
```json
{
  ...
  "items": [
    { "item": 1, ... },
    { "item": 2, ... },
    { "item": 3, ... },
    ...
    { "item": 50, ... }
  ]
}
```

### Caso 4: Item sin código de producto
```json
{
  "item": 1,
  "codigo": null,  // ← null cuando no existe
  "descripcion": "Servicio de consultoría",
  ...
}
```

## 8. VALIDACIONES RECOMENDADAS

### Validación 1: Suma de items = Totales
```python
suma_valor_venta_items = sum(item['valor_venta'] for item in json['items'])
assert abs(suma_valor_venta_items - json['subtotal']) < 0.05  # Tolerancia 5 centavos
```

### Validación 2: IGV correcto (18% en Perú)
```python
for item in json['items']:
    igv_esperado = item['valor_venta'] * 0.18
    assert abs(item['igv_item'] - igv_esperado) < 0.05
```

### Validación 3: Items no vacío si hay importe total > 0
```python
if json['importe_total'] > 0:
    assert len(json['items']) > 0, "Factura con monto pero sin items"
```

## 9. PROMPT FINAL PARA GEMINI

El prompt actual está bien estructurado. Pequeños ajustes recomendados:

**Agregar:**
- Campo `item` (número de línea) en cada elemento del array
- Instrucción para mantener el orden de los items como aparecen en la factura
- Validación matemática de totales

**Versión mejorada del prompt:**

```
⚠️ MUY IMPORTANTE - ITEMS/PRODUCTOS:
El campo "items" es un ARRAY que contiene TODOS los productos/servicios listados en la factura.
Cada item debe ser un objeto con estos campos (usa los nombres exactos):
{
  "item": número de línea (1, 2, 3...),
  "codigo": "código del producto/servicio (si existe, sino null)",
  "descripcion": "descripción COMPLETA del producto/servicio",
  "cantidad": cantidad numérica,
  "unidad_medida": "unidad (ej: UND, KG, M, GAL, etc.)",
  "precio_unitario": precio unitario SIN IGV,
  "valor_venta": valor total de la línea SIN IGV (cantidad × precio_unitario),
  "igv_item": IGV de esta línea (generalmente 18% del valor_venta),
  "precio_total": precio total de la línea CON IGV (valor_venta + igv_item)
}

IMPORTANTE:
- Mantén el ORDEN de los items como aparecen en la factura (de arriba hacia abajo)
- Numera los items secuencialmente: 1, 2, 3, 4...
- Si un campo no existe, usa null (especialmente "codigo")
- Asegúrate que: valor_venta = cantidad × precio_unitario
- Asegúrate que: precio_total = valor_venta + igv_item
- Si no hay items en la factura, usa un array vacío []
```

## 10. RESUMEN DE CAMBIOS NECESARIOS

### En el código (process_batch.py):
- [x] Agregar campo `items` al prompt
- [ ] Agregar campo `item` (número de línea) en el ejemplo del prompt
- [ ] Agregar instrucción de orden y numeración

### En la validación:
- [ ] Opcional: Agregar validación de suma de items vs totales
- [ ] Opcional: Agregar warning si items está vacío pero hay importe_total > 0

## 11. DECISIÓN FINAL

**ESTRUCTURA RECOMENDADA:** Flat + Items (estructura actual)

**CAMPOS TOTALES:** 24 campos flat + 1 array de items

**MODIFICACIÓN AL PROMPT:** Agregar campo `item` (número de línea)

¿Apruebas esta estructura? Si es así, procedo a:
1. Ajustar el prompt con el campo `item`
2. Reprocesar la carpeta "Originales" con la estructura definitiva
3. Validar que los JSON generados sean correctos
