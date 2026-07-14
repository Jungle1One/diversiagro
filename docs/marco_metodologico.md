# 📊 Marco Metodológico (CRISP-ML)

El desarrollo de los modelos híbridos (RFRK) de **DiversIAgro** sigue la metodología estándar de la industria **CRISP-ML(Q)** (Cross-Industry Standard Process for Machine Learning with Quality Assurance).

## 1. Comprensión del Negocio (Business Understanding)
El objetivo de negocio es predecir la aptitud agropecuaria de 5 cultivos distintos en cualquier punto del Valle del Cauca, basándonos en variables limitantes físicas (Topografía y Clima). El resultado (Aptitud Alta, Media, Baja, No Apta) sirve para recomendar alternativas de siembra.

## 2. Comprensión de los Datos (Data Understanding)
Trabajamos con dos fuentes primarias:
- **Raster Geoespacial (DEM):** Elevación y pendiente (USGS).
- **Vectores Geoespaciales:** Polígonos de aptitud de la UPRA (Variable Objetivo) y centroides de precipitación del IDEAM.
Se identificó que los datos crudos tenían diferentes proyecciones cartográficas y resolución.

## 3. Preparación de los Datos (Data Preparation)
Automatizado en `src/features/consolidate_training_data.py`.
- **Limpieza:** Se aplicó "Clipping" a la precipitación (500mm a 8000mm) para eliminar outliers (valores absurdos del IDEAM causados por errores humanos).
- **Fusión (Spatial Join):** Se cruzaron los polígonos de aptitud con los puntos de clima y raster topográficos.
- **Muestreo (Stratified Sampling):** Dado que la categoría "Exclusión Legal" dominaba el mapa, se limitó a un máximo de 500 puntos por categoría para evitar desbalance de clases masivo.

## 4. Modelado (Modeling)
Diseñamos un **Modelo Híbrido RFRK (Random Forest Regression Kriging)**.
- **Random Forest:** Aprende la relación determinística entre el Clima/Topografía y la Aptitud.
- **Kriging Ordinario:** Captura los residuos espaciales. Entiende que si un punto falló por +0.5 y otro cercano también, probablemente hay un factor oculto en el suelo que no estamos midiendo, y corrige la predicción.

## 5. Evaluación (Evaluation)
La métrica principal utilizada es el $R^2$ y el **RMSE** del Random Forest, complementada con el análisis de los semivariogramas del Kriging. Si $R^2 > 0.85$, el modelo capta correctamente la bioclimatología.

## 6. Despliegue (Deployment)
Los modelos se serializan en `.pkl` y se levantan en la memoria RAM de un backend `FastAPI`. La arquitectura REST permite que tanto un sistema web (Streamlit) como un sistema IVR (Twilio Voice) consulten el modelo simultáneamente de forma desacoplada.
