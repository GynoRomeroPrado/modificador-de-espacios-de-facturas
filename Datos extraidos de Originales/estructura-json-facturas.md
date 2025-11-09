# ESTRUCTURA JSON DEFINITIVA PARA EXTRACCIÓN DE FACTURAS
## Sistema InvokeX v5.5 - Documentación de Estructura de Datos

---

## 📋 INFORMACIÓN GENERAL

- **Versión**: 2.0
- **Fecha**: 8 de Noviembre, 2025
- **Propósito**: Estructura JSON estándar para la extracción de datos de facturas
- **Basado en**: Trazabilidad de Base de Datos v5.5 (97 campos)
- **Uso**: Extracción de datos vía OCR (Docling/LayoutLMv3)

---

## 🎯 ESTRUCTURA JSON COMPLETA

```json
{
  "tipo_documento": "FACTURA ELECTRONICA",
  "serie_completa": "F001-00000123",
  "fecha_emision": "2025-01-15",
  "fecha_vencimiento": "2025-02-14",
  "moneda": "SOLES",
  
  "emisor_ruc": "20123456789",
  "emisor_razon_social": "EMPRESA EJEMPLO S.A.C.",
  "emisor_direccion": "AV. PRINCIPAL 123 LIMA-LIMA-MIRAFLORES",
  "emisor_sucursal": null,
  "emisor_telefono": "(51-1) 123-4567",
  "emisor_web": "www.ejemplo.com",
  
  "receptor_numero_doc": "20987654321",
  "receptor_tipo_doc": "RUC",
  "receptor_razon_social": "CLIENTE EJEMPLO S.R.L.",
  "receptor_direccion": "JR. COMERCIO 456 LIMA-LIMA-SURCO",
  "receptor_contacto": null,
  "receptor_telefono": null,
  "receptor_email": null,
  "receptor_sucursal": null,
  
  "subtotal": 1250.00,
  "descuento": 0.00,
  "subtotal_con_descuento": 1250.00,
  "igv": 225.00,
  "isc": null,
  "otros_cargos": 0.00,
  "importe_total": 1475.00,
  "tipo_cambio": null,
  "importe_total_moneda_base": null,
  "retencion_monto": null,
  "retencion_porcentaje": null,
  "percepcion_monto": null,
  "percepcion_porcentaje": null,
  "detraccion_monto": 147.50,
  "detraccion_porcentaje": 10.0,
  "detraccion_codigo_bienes": null,
  "anticipo_monto": null,
  "anticipo_numero": null,
  
  "numero_contrato": "CW120329",
  "orden_compra": "OC-2025-001",
  "orden_servicio": null,
  "numero_pedido": null,
  "guia_remision": "T001-00000123",
  "condicion_pago": "Credito 30 dias",
  "forma_pago": "TRANSFERENCIA",
  "cuenta_bancaria": null,
  "numero_cuenta_detraccion": "00000347620",
  
  "glosa": "Venta de productos varios",
  "observaciones": "SON: MIL CUATROCIENTOS SETENTA Y CINCO CON 00/100 SOLES",
  "centro_costo": null,
  "proyecto": null,
  "ubicacion_obra": null,
  "numero_vale": null,
  "numero_placa": null,
  "referencia_1": null,
  "referencia_2": null,
  
  "cod_qr": null,
  "hash_sunat": null,
  "numero_autorizacion": null,
  "serie_fisica": null,
  "numero_fisico": null,
  
  "doc_relacionado_tipo": null,
  "doc_relacionado_numero": null,
  "doc_relacionado_fecha": null,
  "motivo_emision": null,
  
  "emisor_departamento": "LIMA",
  "emisor_provincia": "LIMA",
  "emisor_distrito": "MIRAFLORES",
  "emisor_ubigeo": "150122",
  "emisor_codigo_postal": null,
  "emisor_email": "facturacion@ejemplo.com",
  "emisor_nombre_comercial": "EJEMPLO SAC",
  "emisor_codigo_establecimiento": null,
  
  "receptor_departamento": "LIMA",
  "receptor_provincia": "LIMA", 
  "receptor_distrito": "SURCO",
  "receptor_ubigeo": "150140",
  "receptor_codigo_postal": null,
  "receptor_nombre_comercial": null,
  
  "is_exportacion": false,
  "incoterm": null,
  "puerto_embarque": null,
  "puerto_destino": null,
  "nave": null,
  "numero_contenedor": null,
  
  "agente_retencion": true,
  "agente_percepcion": false,
  "buen_contribuyente": false,
  
  "vendedor_codigo": null,
  "vendedor_nombre": null,
  "cajero_codigo": null,
  "cajero_nombre": null,
  
  "fecha_registro": null,
  "fecha_pago": null,
  "fecha_cancelacion": null,
  
  "items": [
    {
      "item": 1,
      "codigo": "PROD001",
      "descripcion": "Cemento Portland Tipo I - Bolsa 42.5 kg",
      "cantidad": 100.0,
      "unidad_medida": "BOL",
      "precio_unitario": 25.00,
      "valor_venta": 2500.00,
      "descuento_item": 0.00,
      "subtotal_item": 2500.00,
      "tipo_igv": "GRAVADO",
      "igv_item": 450.00,
      "isc_item": null,
      "otro_tributo": null,
      "importe_total_item": 2950.00,
      "lote": null,
      "fecha_vencimiento": null,
      "serie": null,
      "modelo": null,
      "marca": null,
      "placa": null,
      "partida_arancelaria": null,
      "centro_costo_item": null,
      "cuenta_contable": null,
      "proyecto_item": null,
      "orden_item": null,
      "ubicacion": null,
      "observacion_item": null
    },
    {
      "item": 2,
      "codigo": null,
      "descripcion": "Servicio de transporte de materiales - 10 viajes",
      "cantidad": 10.0,
      "unidad_medida": "ZZ",
      "precio_unitario": 150.00,
      "valor_venta": 1500.00,
      "descuento_item": 0.00,
      "subtotal_item": 1500.00,
      "tipo_igv": "GRAVADO",
      "igv_item": 270.00,
      "isc_item": null,
      "otro_tributo": null,
      "importe_total_item": 1770.00,
      "lote": null,
      "fecha_vencimiento": null,
      "serie": null,
      "modelo": null,
      "marca": null,
      "placa": "ABC-123",
      "partida_arancelaria": null,
      "centro_costo_item": null,
      "cuenta_contable": null,
      "proyecto_item": null,
      "orden_item": null,
      "ubicacion": "OBRA TRUJILLO",
      "observacion_item": null
    }
  ],
  
  "cuotas": [
    {
      "numero": 1,
      "monto": 737.50,
      "fecha_vencimiento": "2025-02-14",
      "estado": "PENDIENTE"
    },
    {
      "numero": 2,
      "monto": 737.50,
      "fecha_vencimiento": "2025-03-14",
      "estado": "PENDIENTE"
    }
  ]
}
```

---

## 📊 DEFINICIÓN DE CAMPOS

### 🔷 SECCIÓN 1: DOCUMENTO (5 campos)

| Campo | Tipo | Nullable | Descripción | Ejemplo |
|-------|------|----------|-------------|---------|
| `tipo_documento` | string | NO | Tipo de comprobante | "FACTURA ELECTRONICA" |
| `serie_completa` | string | NO | Serie y número del documento | "F001-00000123" |
| `fecha_emision` | string | SÍ | Fecha de emisión (YYYY-MM-DD) | "2025-01-15" |
| `fecha_vencimiento` | string | SÍ | Fecha de vencimiento | "2025-02-14" |
| `moneda` | string | SÍ | Moneda del documento | "SOLES" o "DOLARES AMERICANOS" |

### 🔷 SECCIÓN 2: EMISOR (6 campos base + 8 adicionales)

| Campo | Tipo | Nullable | Descripción |
|-------|------|----------|-------------|
| `emisor_ruc` | string | NO | RUC del emisor |
| `emisor_razon_social` | string | NO | Razón social |
| `emisor_direccion` | string | SÍ | Dirección completa |
| `emisor_sucursal` | string | SÍ | Código/nombre de sucursal |
| `emisor_telefono` | string | SÍ | Teléfono |
| `emisor_web` | string | SÍ | Sitio web |
| `emisor_departamento` | string | SÍ | Departamento |
| `emisor_provincia` | string | SÍ | Provincia |
| `emisor_distrito` | string | SÍ | Distrito |
| `emisor_ubigeo` | string | SÍ | Código UBIGEO |
| `emisor_codigo_postal` | string | SÍ | Código postal |
| `emisor_email` | string | SÍ | Email de contacto |
| `emisor_nombre_comercial` | string | SÍ | Nombre comercial |
| `emisor_codigo_establecimiento` | string | SÍ | Código SUNAT del establecimiento |

### 🔷 SECCIÓN 3: RECEPTOR (8 campos base + 6 adicionales)

| Campo | Tipo | Nullable | Descripción |
|-------|------|----------|-------------|
| `receptor_numero_doc` | string | NO | RUC/DNI del receptor |
| `receptor_tipo_doc` | string | SÍ | Tipo de documento (RUC, DNI, CE) |
| `receptor_razon_social` | string | NO | Razón social/nombre |
| `receptor_direccion` | string | SÍ | Dirección completa |
| `receptor_contacto` | string | SÍ | Persona de contacto |
| `receptor_telefono` | string | SÍ | Teléfono |
| `receptor_email` | string | SÍ | Email |
| `receptor_sucursal` | string | SÍ | Sucursal de destino |
| `receptor_departamento` | string | SÍ | Departamento |
| `receptor_provincia` | string | SÍ | Provincia |
| `receptor_distrito` | string | SÍ | Distrito |
| `receptor_ubigeo` | string | SÍ | Código UBIGEO |
| `receptor_codigo_postal` | string | SÍ | Código postal |
| `receptor_nombre_comercial` | string | SÍ | Nombre comercial |

### 🔷 SECCIÓN 4: IMPORTES Y TRIBUTOS (17 campos)

| Campo | Tipo | Nullable | Descripción |
|-------|------|----------|-------------|
| `subtotal` | number | NO | Subtotal sin IGV |
| `descuento` | number | SÍ | Descuento global |
| `subtotal_con_descuento` | number | SÍ | Subtotal después del descuento |
| `igv` | number | NO | Impuesto General a las Ventas |
| `isc` | number | SÍ | Impuesto Selectivo al Consumo |
| `otros_cargos` | number | SÍ | Otros cargos adicionales |
| `importe_total` | number | NO | Total a pagar |
| `tipo_cambio` | number | SÍ | Tipo de cambio si es moneda extranjera |
| `importe_total_moneda_base` | number | SÍ | Total en moneda base (PEN) |
| `retencion_monto` | number | SÍ | Monto de retención |
| `retencion_porcentaje` | number | SÍ | Porcentaje de retención |
| `percepcion_monto` | number | SÍ | Monto de percepción |
| `percepcion_porcentaje` | number | SÍ | Porcentaje de percepción |
| `detraccion_monto` | number | SÍ | Monto de detracción |
| `detraccion_porcentaje` | number | SÍ | Porcentaje de detracción |
| `detraccion_codigo_bienes` | string | SÍ | Código de bienes/servicios sujetos |
| `anticipo_monto` | number | SÍ | Monto de anticipo |
| `anticipo_numero` | string | SÍ | Número de documento de anticipo |

### 🔷 SECCIÓN 5: REFERENCIAS (10 campos)

| Campo | Tipo | Nullable | Descripción |
|-------|------|----------|-------------|
| `numero_contrato` | string | SÍ | Número de contrato |
| `orden_compra` | string | SÍ | Orden de compra |
| `orden_servicio` | string | SÍ | Orden de servicio |
| `numero_pedido` | string | SÍ | Número de pedido |
| `guia_remision` | string | SÍ | Guía de remisión |
| `condicion_pago` | string | SÍ | Condición de pago |
| `forma_pago` | string | SÍ | Forma de pago |
| `cuenta_bancaria` | string | SÍ | Cuenta para pago |
| `numero_cuenta_detraccion` | string | SÍ | Cuenta Banco de la Nación |

### 🔷 SECCIÓN 6: INFORMACIÓN ADICIONAL (9 campos)

| Campo | Tipo | Nullable | Descripción |
|-------|------|----------|-------------|
| `glosa` | string | SÍ | Glosa o descripción general |
| `observaciones` | string | SÍ | Observaciones (incluye monto en letras) |
| `centro_costo` | string | SÍ | Centro de costo |
| `proyecto` | string | SÍ | Código/nombre de proyecto |
| `ubicacion_obra` | string | SÍ | Ubicación de la obra |
| `numero_vale` | string | SÍ | Número de vale |
| `numero_placa` | string | SÍ | Placa de vehículo |
| `referencia_1` | string | SÍ | Campo de referencia adicional 1 |
| `referencia_2` | string | SÍ | Campo de referencia adicional 2 |

### 🔷 SECCIÓN 7: ITEMS (Array de objetos)

Cada elemento del array `items` contiene:

| Campo | Tipo | Nullable | Descripción |
|-------|------|----------|-------------|
| `item` | number | NO | Número secuencial (1, 2, 3...) |
| `codigo` | string | SÍ | Código del producto/servicio |
| `descripcion` | string | NO | Descripción completa |
| `cantidad` | number | NO | Cantidad |
| `unidad_medida` | string | NO | Unidad de medida |
| `precio_unitario` | number | NO | Precio unitario sin IGV |
| `valor_venta` | number | NO | Total línea sin IGV |
| `descuento_item` | number | SÍ | Descuento de la línea |
| `subtotal_item` | number | SÍ | Subtotal después del descuento |
| `tipo_igv` | string | SÍ | Tipo de IGV (GRAVADO, EXONERADO, INAFECTO) |
| `igv_item` | number | SÍ | IGV de la línea |
| `isc_item` | number | SÍ | ISC de la línea |
| `otro_tributo` | number | SÍ | Otros tributos |
| `importe_total_item` | number | NO | Total de la línea con IGV |
| `lote` | string | SÍ | Lote del producto |
| `fecha_vencimiento` | string | SÍ | Vencimiento del producto |
| `serie` | string | SÍ | Serie del producto |
| `modelo` | string | SÍ | Modelo |
| `marca` | string | SÍ | Marca |
| `placa` | string | SÍ | Placa vehicular |
| `partida_arancelaria` | string | SÍ | Partida arancelaria |
| `centro_costo_item` | string | SÍ | Centro de costo del item |
| `cuenta_contable` | string | SÍ | Cuenta contable |
| `proyecto_item` | string | SÍ | Proyecto asociado |
| `orden_item` | string | SÍ | Orden asociada |
| `ubicacion` | string | SÍ | Ubicación/destino |
| `observacion_item` | string | SÍ | Observaciones del item |

### 🔷 SECCIÓN 8: CUOTAS (Array de objetos)

Para facturas a crédito con pago fraccionado:

| Campo | Tipo | Nullable | Descripción |
|-------|------|----------|-------------|
| `numero` | number | NO | Número de cuota |
| `monto` | number | NO | Monto de la cuota |
| `fecha_vencimiento` | string | NO | Fecha de vencimiento |
| `estado` | string | SÍ | Estado de la cuota |

---

## 📝 REGLAS DE EXTRACCIÓN

### ✅ OBLIGATORIO EXTRAER:
1. **Siempre extraer `items`** aunque esté vacío: `"items": []`
2. **Siempre extraer `cuotas`** para facturas a crédito: `"cuotas": []`
3. **Campos númericos**: Usar tipo `number`, no strings
4. **Fechas**: Formato `YYYY-MM-DD` siempre
5. **Campos vacíos**: Usar `null`, no strings vacíos

### ⚠️ VALIDACIONES IMPORTANTES:
1. `valor_venta = cantidad × precio_unitario`
2. `igv_item = valor_venta × 0.18` (para items gravados)
3. `importe_total_item = valor_venta + igv_item - descuento_item`
4. La suma de `valor_venta` de todos los items debe ser cercana al `subtotal`

### 🔄 NORMALIZACIÓN:
1. **Moneda**: 
   - "S/" → "SOLES"
   - "PEN" → "SOLES"
   - "$" → "DOLARES AMERICANOS"
   - "USD" → "DOLARES AMERICANOS"

2. **Tipo de documento**:
   - Estandarizar a mayúsculas
   - Remover tildes: "FACTURA ELECTRÓNICA" → "FACTURA ELECTRONICA"

3. **RUC/DNI**:
   - Remover guiones y espacios
   - Solo dígitos

---

## 🚀 PROMPT PARA EXTRACCIÓN CON GEMINI/CLAUDE

```
Extrae TODOS los datos de esta factura en formato JSON siguiendo exactamente esta estructura:

1. DOCUMENTO: tipo_documento, serie_completa, fecha_emision (formato YYYY-MM-DD), fecha_vencimiento, moneda (SOLES o DOLARES AMERICANOS)

2. EMISOR: Extrae TODOS los campos del emisor incluyendo RUC, razón social, dirección, teléfono, email, web, ubicación (departamento, provincia, distrito), etc.

3. RECEPTOR: Extrae TODOS los campos del receptor incluyendo número de documento, tipo, razón social, dirección, contacto, teléfono, email, ubicación, etc.

4. IMPORTES: subtotal (sin IGV), descuento, IGV, ISC, otros_cargos, importe_total, detracciones (monto y %), retenciones, percepciones, anticipos, tipo de cambio si aplica

5. REFERENCIAS: número de contrato, orden de compra, orden de servicio, guía de remisión, condición de pago, forma de pago, cuentas bancarias

6. INFORMACIÓN ADICIONAL: glosa, observaciones (incluye el monto en letras), centro de costo, proyecto, ubicación de obra, números de vale, placas, referencias adicionales

7. ITEMS (MUY IMPORTANTE): Extrae TODOS los productos/servicios como un array. Cada item debe tener:
   - item: número secuencial (1, 2, 3...)
   - codigo: código del producto (null si no existe)
   - descripcion: descripción COMPLETA
   - cantidad: cantidad numérica
   - unidad_medida: unidad (UND, KG, M, GAL, HRS, ZZ, etc.)
   - precio_unitario: precio sin IGV
   - valor_venta: total línea sin IGV
   - igv_item: IGV de la línea
   - importe_total_item: total con IGV
   - Campos adicionales si existen: lote, serie, marca, modelo, placa, ubicación, etc.

8. CUOTAS: Si es una factura a crédito con pagos fraccionados, extrae las cuotas con: numero, monto, fecha_vencimiento

REGLAS IMPORTANTES:
- Si un campo no existe, usa null
- Mantén el orden de los items como aparecen en la factura
- Los números deben ser tipo number, no string
- Las fechas en formato YYYY-MM-DD
- Si no hay items, usa un array vacío: "items": []
- Si no hay cuotas, usa un array vacío: "cuotas": []
```

---

## 📈 EJEMPLOS DE CASOS ESPECIALES

### Caso 1: Factura sin items detectables
```json
{
  ...otros campos...,
  "items": [],
  "observaciones": "Items no pudieron ser extraídos - requiere revisión manual"
}
```

### Caso 2: Factura con detracción (construcción)
```json
{
  "detraccion_monto": 1907.35,
  "detraccion_porcentaje": 10.0,
  "numero_cuenta_detraccion": "00000347620",
  "detraccion_codigo_bienes": "027",
  "observaciones": "Operación Sujeta al D.L. N° 940..."
}
```

### Caso 3: Item de servicio sin código
```json
{
  "item": 1,
  "codigo": null,
  "descripcion": "Servicio de consultoría en gestión de proyectos",
  "cantidad": 1.0,
  "unidad_medida": "ZZ",
  "precio_unitario": 5000.00,
  ...
}
```

### Caso 4: Factura en dólares con tipo de cambio
```json
{
  "moneda": "DOLARES AMERICANOS",
  "importe_total": 1000.00,
  "tipo_cambio": 3.85,
  "importe_total_moneda_base": 3850.00
}
```

---

## 🔍 CAMPOS CRÍTICOS PARA CONSTRUCCIÓN

Para el sector construcción, asegurar la extracción de:

1. **Detracción**: Obligatoria para servicios de construcción
2. **Ubicación de obra**: Campo importante para proyectos
3. **Número de contrato**: Para trazabilidad de servicios
4. **Placas vehiculares**: En items de transporte
5. **Centro de costo/Proyecto**: Para contabilidad de obra
6. **Guías de remisión**: Para materiales transportados

---

## 📚 NOTAS FINALES

- Esta estructura está alineada con la base de datos v5.5 del sistema
- Incluye 97 campos principales + campos de items ilimitados
- Soporta facturas peruanas con todos sus regímenes tributarios
- Compatible con SUNAT y normativa vigente 2025
- Preparada para futuras extensiones sin romper compatibilidad

---

**Documento generado para**: Sistema InvokeX - FacturasIA  
**Versión Base de Datos**: v5.5  
**Última actualización**: 8 de Noviembre, 2025
