# 📖 Diccionario de Datos

Los datos de entrenamiento procesados (`data/processed/consolidated_training_*.csv`) consisten en matrices estructuradas donde cada fila representa una coordenada geográfica en el Valle del Cauca, y cada columna es una variable física.

| Columna | Tipo | Descripción | Fuente Original |
| :--- | :--- | :--- | :--- |
| **lat** | numérico | Latitud de la muestra geolocalizada en grados decimales (EPSG:4326). | UPRA (Polígono) |
| **lon** | numérico | Longitud de la muestra geolocalizada en grados decimales (EPSG:4326). | UPRA (Polígono) |
| **altitud** | numérico | Elevación en metros sobre el nivel del mar (m.s.n.m). Variable crítica para el umbral térmico. | NASA SRTM (DEM) |
| **pendiente** | numérico | Inclinación del terreno en grados. Vital para estimar riesgo de erosión y mecanización. | NASA SRTM (Derivado) |
| **lluvia** | numérico | Precipitación anual promedio (en milímetros). Acotada artificialmente entre 500 y 8000 para evitar errores. | IDEAM (Meteorología) |
| **aptitud** | numérico | Variable Objetivo (Target). Nivel de aptitud para el cultivo. <br> `3.0`: Aptitud Alta <br> `2.0`: Aptitud Media <br> `1.0`: Aptitud Baja <br> `0.0`: No Apta / Exclusión Legal | UPRA (Mapas 1:100.000) |
