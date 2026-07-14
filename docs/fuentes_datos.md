# 📂 Fuentes de Datos e Integración

Para entrenar a DiversIAgro y alimentar el pipeline GIS, los datos crudos provienen de fuentes oficiales y públicas. Estos datos deben ser descargados y almacenados en la carpeta `data/raw/`.

## 1. Topografía: Shuttle Radar Topography Mission (SRTM)
El Modelo de Elevación Digital (DEM) permite obtener la **altitud** y derivar matemáticamente la **pendiente** de las montañas del Valle del Cauca.
- **Formato:** Raster (`.tif`)
- **Resolución:** ~30 metros (1 arco-segundo)
- **Fuente:** NASA / USGS (EarthExplorer)
- **Enlace:** [USGS EarthExplorer](https://earthexplorer.usgs.gov/) (Buscar SRTM 1 Arc-Second Global)

## 2. Metas de Aptitud: Unidad de Planificación Rural Agropecuaria (UPRA)
Estos mapas actúan como la variable objetivo o "Ground Truth" para el Machine Learning. Fueron construidos por agrónomos del gobierno usando álgebra de mapas multicriterio.
- **Formato:** Vectorial vía Socrata API (SODA)
- **Cultivos y Enlaces Socrata (`datos.gov.co`):**
  - **Café:** [SODA API kwvf-nwea](https://www.datos.gov.co/resource/kwvf-nwea)
  - **Cacao:** [SODA API jdjx-qer4](https://www.datos.gov.co/resource/jdjx-qer4)
  - **Aguacate:** [SODA API tx7u-frn2](https://www.datos.gov.co/resource/tx7u-frn2)
  - **Fresa:** [SODA API emsg-94di](https://www.datos.gov.co/resource/emsg-94di)
  - **Caña Panelera:** [SODA API p9xp-sm4v](https://www.datos.gov.co/resource/p9xp-sm4v)

## 3. Climatología: Instituto de Hidrología, Meteorología y Estudios Ambientales (IDEAM)
Datos históricos de precipitación anual recopilados de estaciones meteorológicas en los municipios de Colombia.
- **Formato:** Tabular vía Socrata API (SODA)
- **Fuente:** Datos Abiertos Colombia / IDEAM
- **Enlace:** [Precipitación IDEAM (SODA API s54a-sgyg)](https://www.datos.gov.co/resource/s54a-sgyg)

## 4. Histórico de Cosechas: Evaluaciones Agropecuarias Municipales (EVA)
Datos históricos de producción, rendimiento y área sembrada, utilizados para validar la producción real contra la aptitud teórica.
- **Formato:** Tabular vía Socrata API (SODA)
- **Fuente:** Datos Abiertos Colombia / UPRA
- **Enlace:** [EVA 2019-2024 (SODA API uejq-wxrr)](https://www.datos.gov.co/resource/uejq-wxrr)

> **Nota para Evaluadores:** Dado que los mapas TIF y GeoJSON en conjunto superan los 200MB, no están en el repositorio de GitHub. Deben descargarse del enlace temporal especificado en `data/README.md`.
