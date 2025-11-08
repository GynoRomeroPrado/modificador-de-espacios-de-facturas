# 🚀 Data Augmentation para Facturas

Sistema automático que expande datasets de facturas mediante transformaciones geométricas, multiplicando tus datos para entrenar modelos de detección más robustos.

## 📋 ¿Qué hace este proyecto?

Este sistema toma tus facturas existentes (imagen + JSON con datos extraídos) y **genera múltiples variaciones** mediante desplazamientos de píxeles en diferentes direcciones.

### Resultado:
- **Input:** 10 facturas
- **Output:** 170 facturas (10 originales + 160 variaciones)
- **Multiplicador:** 17x tu dataset

## 🎯 ¿Por qué usar Data Augmentation?

Los desplazamientos de píxeles hacen que los bounding boxes cambien de posición. Cuando entrenes tu modelo, aprenderá a detectar campos de facturas en **diferentes posiciones**, no solo en las posiciones exactas de tus facturas originales.

**Beneficios:**
- Mayor robustez del modelo
- Mejor generalización
- Reducción de overfitting
- Más datos sin necesidad de recolectar más facturas reales

## 📥 Input Requerido

Tu directorio de entrada debe contener pares de archivos:

```
Drive/Facturas/
├── factura_random_name_1.pdf      ← Imagen de factura
├── factura_random_name_1.json     ← JSON con data extraída
├── otra_factura.jpg                ← Imagen de factura
├── otra_factura.json               ← JSON con data extraída
└── ...
```

**Formatos soportados:**
- Imágenes: `.pdf`, `.jpg`, `.jpeg`, `.png`
- Datos: `.json` (debe tener el mismo nombre que la imagen)

**Estructura del JSON:**
```json
{
  "filename": "factura_random_name_1.pdf",
  "datos_extraidos": {
    "emisor_ruc": "20505670443",
    "total": 364.8,
    ...
  }
}
```

## 📤 Output Generado

```
Drive/Facturas_Procesadas/
├── organized/
│   ├── factura_0001.pdf       ← Renombrada
│   ├── factura_0001.json
│   ├── factura_0002.jpg
│   ├── factura_0002.json
│   └── ...
│
├── augmented/
│   ├── factura_0001_aug_01_derecha_small.png
│   ├── factura_0001_aug_01_derecha_small.json
│   ├── factura_0001_aug_02_izquierda_small.png
│   ├── factura_0001_aug_02_izquierda_small.json
│   ... (16 variaciones × N facturas)
│
└── dataset_report.json
```

## ⚙️ Transformaciones Aplicadas

Se generan **16 variaciones** por cada factura:

| Tipo | Transformación | Desplazamiento |
|------|----------------|----------------|
| Horizontal | derecha_small, izquierda_small | ±10px |
| Vertical | abajo_small, arriba_small | ±10px |
| Diagonal | 4 direcciones | ±10px |
| Horizontal | derecha_medium, izquierda_medium | ±20px |
| Vertical | abajo_medium, arriba_medium | ±20px |
| Horizontal | derecha_large, izquierda_large | ±30px |
| Vertical | abajo_large, arriba_large | ±30px |

## 🚀 Uso desde Google Colab

### Opción 1: Notebook (Recomendado)

1. Abre el notebook en Colab:
   - Sube `notebooks/Invoice_Dataset_Augmentation.ipynb` a Colab
   - O usa: [Open in Colab](https://colab.research.google.com/)

2. Monta tu Google Drive

3. Configura las rutas:
   ```python
   INPUT_DIR = "/content/drive/MyDrive/Facturas"
   OUTPUT_DIR = "/content/drive/MyDrive/Facturas_Procesadas"
   ```

4. Ejecuta todas las celdas

### Opción 2: Script Python

```bash
# En Colab
!git clone https://github.com/GynoRomeroPrado/modificador-de-espacios-de-facturas.git
%cd modificador-de-espacios-de-facturas

# Instalar dependencias
!pip install -r requirements.txt
!apt-get install poppler-utils

# Ejecutar
!python src/main.py /content/drive/MyDrive/Facturas /content/drive/MyDrive/Facturas_Procesadas
```

## 💻 Uso Local

### Instalación

```bash
# Clonar repositorio
git clone https://github.com/GynoRomeroPrado/modificador-de-espacios-de-facturas.git
cd modificador-de-espacios-de-facturas

# Crear entorno virtual (opcional)
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Instalar poppler (necesario para PDFs)
# Ubuntu/Debian:
sudo apt-get install poppler-utils

# macOS:
brew install poppler

# Windows:
# Descargar desde: https://github.com/oschwartz10612/poppler-windows/releases/
```

### Ejecución

```bash
python src/main.py <input_dir> <output_dir>
```

**Ejemplo:**
```bash
python src/main.py ./facturas ./facturas_procesadas
```

## 📊 Ejemplo de Ejecución

```
============================================================
🚀 INICIANDO DATA AUGMENTATION DE FACTURAS
============================================================

📁 Creando estructura de directorios...

🔍 Buscando facturas en: /Drive/Facturas
✅ Se encontraron 10 facturas

============================================================
📋 PROCESANDO FACTURAS
============================================================

[1/10] Procesando: factura_random_name_1
  📥 Cargando imagen y JSON...
  💾 Guardando factura original renombrada...
  🔄 Generando 16 variaciones augmentadas...
  💾 Guardando variaciones...
  ✅ Completado: 1 original + 16 augmentadas

[2/10] Procesando: otra_factura
  ...

============================================================
✅ PROCESO COMPLETADO
============================================================

📊 RESUMEN:
  • Facturas originales:     10
  • Facturas augmentadas:    160
  • Total de facturas:       170

🚀 Dataset expandido 17.0x
============================================================
```

## 📁 Estructura del Proyecto

```
modificador-de-espacios-de-facturas/
├── src/
│   ├── main.py                 # Script principal
│   ├── utils.py                # Utilidades
│   ├── image_processor.py      # Procesamiento de imágenes
│   └── augmentation.py         # Lógica de augmentation
├── notebooks/
│   └── Invoice_Dataset_Augmentation.ipynb
├── examples/
├── requirements.txt
├── .gitignore
└── README.md
```

## 🔧 Personalización

### Modificar los desplazamientos

Edita `src/augmentation.py`:

```python
class AugmentationConfig:
    SHIFT_SMALL = 10   # Cambiar valores aquí
    SHIFT_MEDIUM = 20
    SHIFT_LARGE = 30
```

### Modificar transformaciones

Edita la lista `TRANSFORMATIONS` en `src/augmentation.py` para agregar/quitar transformaciones.

### Cambiar DPI para PDFs

```python
augmenter = InvoiceDatasetAugmenter(
    input_dir=INPUT_DIR,
    output_dir=OUTPUT_DIR,
    dpi=300  # Mayor calidad, archivos más grandes
)
```

## 📝 Formato del JSON Augmentado

Cada factura augmentada tiene un JSON con:

```json
{
  "filename": "factura_0001_aug_01_derecha_small.png",
  "datos_extraidos": {
    "emisor_ruc": "20505670443",
    "total": 364.8,
    ...
  },
  "archivo_factura": "factura_0001_aug_01_derecha_small.png",
  "augmentation": {
    "original_filename": "factura_0001.pdf",
    "transformation": "derecha_small",
    "shift_x": 10,
    "shift_y": 0,
    "augmentation_index": 1
  },
  "is_augmented": true
}
```

## ⚠️ Limitaciones

- Solo procesa la **primera página** de archivos PDF
- No extrae datos de las facturas (debes proporcionar los JSONs)
- No genera bounding boxes (eso es un paso posterior)
- No entrena modelos (solo prepara el dataset)

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama: `git checkout -b feature/nueva-funcionalidad`
3. Commit: `git commit -am 'Agregar nueva funcionalidad'`
4. Push: `git push origin feature/nueva-funcionalidad`
5. Abre un Pull Request

## 📄 Licencia

MIT License - ver [LICENSE](LICENSE) para más detalles

## 🆘 Soporte

Si encuentras algún problema:
1. Revisa que tus facturas tengan sus JSONs correspondientes
2. Verifica que las rutas sean correctas
3. Revisa los logs de error en el reporte
4. Abre un [Issue](https://github.com/GynoRomeroPrado/modificador-de-espacios-de-facturas/issues)

## 🎯 Próximos Pasos

Después de usar este sistema:
1. ✅ Dataset expandido
2. 🔲 Generar bounding boxes para cada campo
3. 🔲 Entrenar modelo de detección
4. 🔲 Evaluar y optimizar

---

**Hecho con ❤️ para facilitar el entrenamiento de modelos de detección en facturas**
