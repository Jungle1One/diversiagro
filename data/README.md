# 📂 Estructura de Datos (GIS y Tabulares)

Los archivos de datos crudos (`raw/`) y procesados (`processed/`) han sido excluidos del repositorio mediante `.gitignore`. Algunos de estos archivos, como el DEM (Modelo de Elevación Digital), pesan más de 80 MB, lo cual satura innecesariamente el historial de Git.

## Estructura de este directorio:

```text
data/
├── README.md
├── processed/
│   ├── consolidated_training_aguacate.csv       (Descargar)
│   ├── consolidated_training_cacao.csv          (Descargar)
│   ├── consolidated_training_cafe.csv           (Descargar)
│   ├── consolidated_training_cana_panelera.csv  (Descargar)
│   ├── consolidated_training_fresa.csv          (Descargar)
│   └── ideam_precipitacion_anual_municipio.csv  (Descargar)
└── raw/
    ├── DEM_Valle_Cauca.tif                      (Descargar)
    ├── municipios_valle.geojson                 (Descargar)
    ├── Zonificacion_Aguacate_Valle.geojson      (Descargar)
    ├── Zonificacion_Cacao_Valle.geojson         (Descargar)
    ├── Zonificacion_Cafe_Valle.geojson          (Descargar)
    ├── Zonificacion_Cana_Panelera_Valle.geojson (Descargar)
    └── Zonificacion_Fresa_Valle.geojson         (Descargar)
```

## 🔗 Enlaces de Descarga Externos

Para poder ejecutar la extracción de características GIS (`gis_service.py`) o re-entrenar los modelos (`train.py`), debes descargar los datos desde nuestra nube externa y colocarlos respetando la estructura superior.

*   📥 [https://drive.google.com/drive/folders/1_MJXntVBgj3QEEr5rNg91dKJ5I9-b0b3?usp=sharing](#)

> **Nota para el desarrollador:** Si solo vas a ejecutar la aplicación (`run.py`), asegúrate al menos de tener los archivos `DEM_Valle_Cauca.tif` y `municipios_valle.geojson`, que son obligatorios para extraer las coordenadas de latitud/longitud en tiempo real.
