# 🚀 Guía de Ejecución – Dataset 1: EVA

## Requisitos previos

1. Tener el entorno virtual `.env-1` activado
2. Tener las dependencias instaladas

## Pasos para ejecutar

### 1. Activar el entorno virtual

```powershell
# En PowerShell, desde la raíz del proyecto:
.\.env-1\Scripts\Activate.ps1
```

Si PowerShell te da error de permisos, usa:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\.env-1\Scripts\Activate.ps1
```

O usa el cmd:
```cmd
.env-1\Scripts\activate.bat
```

### 2. Instalar dependencias (solo la primera vez)

```powershell
pip install -r requirements.txt
```

### 3. Ejecutar el script de descarga y limpieza

```powershell
python scripts/01_download_eva.py
```

Este script:
- ✅ Descarga ~141,000 registros del portal datos.gov.co
- ✅ Explora y genera reporte de calidad
- ✅ Filtra datos del Valle del Cauca
- ✅ Filtra cultivos de interés (Café, Plátano, Caña, Cacao)
- ✅ Limpia, normaliza y valida datos
- ✅ Genera archivos CSV procesados

### 4. Archivos generados

Después de ejecutar el script, encontrarás:

```
data/
├── raw/
│   └── eva_2019_2024_raw.csv          ← Datos crudos nacionales (~141K registros)
├── processed/
│   ├── eva_valle_del_cauca_all.csv    ← Todos los cultivos del Valle
│   ├── eva_valle_cultivos_interes.csv ← Solo café, plátano, caña, cacao (limpio)
│   ├── eva_valle_café.csv             ← Solo café
│   ├── eva_valle_plátano.csv          ← Solo plátano
│   ├── eva_valle_caña.csv             ← Solo caña
│   └── eva_valle_cacao.csv            ← Solo cacao
└── reports/
    ├── 01_eva_exploration_report.md   ← Reporte de exploración
    └── 02_eva_quality_report.md       ← Reporte de calidad
```

### 5. Ejecutar el notebook de análisis

```powershell
jupyter notebook notebooks/01_analisis_eva.ipynb
```

El notebook genera visualizaciones profesionales para presentar al equipo.

### 6. Gráficas generadas (en `data/reports/`)

- `fig_completitud.png` – Completitud de datos
- `fig_distribucion_cultivos.png` – Distribución por cultivo
- `fig_registros_por_anio.png` – Registros por año
- `fig_top_municipios.png` – Top municipios productores
- `fig_heatmap_muni_cultivo.png` – Heatmap municipio × cultivo
- `fig_rendimiento_distribucion.png` – Boxplot/violin de rendimiento
- `fig_rendimiento_evolucion.png` – Tendencia de rendimiento
- `fig_cafe_top_municipios.png` – Top municipios cafeteros
- `fig_radar_comparativo.png` – Radar de comparación entre cultivos
- `fig_correlaciones.png` – Correlaciones por cultivo
- `fig_variabilidad_cafe.png` – Estabilidad del café por municipio


### Script 10: Catastro Predial
El script `10_download_limites_admin.py` ahora descarga predios y atributos catastrales para realizar cruces con zonificación.
- **Nota**: La descarga toma tiempo por el alto volumen de datos (cientos de miles de predios).


### Script 10: Catastro Predial
El script `10_download_limites_admin.py` ahora descarga predios y atributos catastrales para realizar cruces con zonificación.
- **Nota**: La descarga toma tiempo por el alto volumen de datos (cientos de miles de predios).
