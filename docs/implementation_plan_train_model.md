# Plan de Implementación: Fase 2 (Desarrollo del Modelo de IA)

Este plan detalla la consolidación de datos finales y la arquitectura del modelo de Machine Learning, asegurando que sirva perfectamente para los dos componentes finales del proyecto: **La Línea de Voz (IVR)** y el **Tablero Web (Streamlit)**.

## 🎯 Objetivo de la Fase 2
Construir un modelo predictivo híbrido (Random Forest + Kriging Espacial - RFRK) capaz de:
1. **Predecir la Aptitud Agroecológica** de cualquier coordenada para Café y cultivos alternativos (Banano, Cacao, etc.).
2. **Predecir el Rendimiento Estimado (Ton/Ha)** basado en los históricos.

## 📊 1. Definición del Espacio de Variables (Features & Targets)

Para entrenar el modelo, crearemos un gran `dataset_consolidado_ml.csv` fusionando las fuentes de la Fase 1.

### Variables Predictoras (X)
Estas son las variables de entrada que el usuario (o el mapa web) le pasará al modelo:
- `altitud_msnm` *(Numérica)*: Extraída del DEM SRTM 30m.
- `pendiente_grados` *(Numérica)*: Extraída del DEM SRTM 30m.
- `precipitacion_anual_mm` *(Numérica)*: Cruzada espacialmente desde las estaciones del IDEAM.
- `municipio` / `coordenadas` *(Espacial)*: Para el cálculo de Kriging (autocorrelación espacial).

### Variables Objetivo (Y)
- **Y1 (Clasificación)** -> `aptitud`: ["Aptitud alta", "Aptitud media", "Aptitud baja", "No apta"]. Obtenida de la UPRA.
- **Y2 (Regresión)** -> `rendimiento_ton_ha`: Obtenido del histórico de las Evaluaciones Agropecuarias (EVA).

### Filtro de Inferencia (Post-Procesamiento por API)
- `cobertura_tierra`: No se usará para entrenar, sino como un **filtro restrictivo en tiempo real**. Si el modelo dice "Aptitud Alta", pero la API del IDEAM dice "Bosque Denso", la predicción final se sobrescribe a "Inviable legalmente".

---

## 🏗️ 2. Arquitectura del Modelo a Desarrollar

Desarrollaremos un **Random Forest Regression Kriging (RFRK)**, el cual consta de dos pasos:

### Paso A: Random Forest (El componente Bioclimático)
Aprenderá las reglas complejas y no lineales de la agricultura. Por ejemplo, descubrirá automáticamente que el café necesita entre 1,200 y 1,800 msnm y lluvias entre 1,500 y 2,500 mm.
*Librería: `scikit-learn`*

### Paso B: Kriging Ordinario (El componente Espacial)
Como no tenemos variables de calidad del suelo (PH, nutrientes), el Random Forest tendrá "errores" (residuos). El Kriging analizará esos errores en el mapa. Si en el norte de Palmira el modelo siempre subestima la aptitud, el Kriging aplicará un ajuste positivo a los vecinos basándose en la Primera Ley de la Geografía de Tobler.
*Librería: `pykrige` o `gstat`*

---

## 🚀 3. Conexión con los Componentes del Proyecto

Los modelos entrenados se exportarán como archivos `.pkl` (Pickle/Joblib) para ser consumidos por:

### Componente 1: Servicio de Voz (Twilio)
- **Input**: El campesino marca el 0800, el IVR detecta su municipio por código postal o voz.
- **Proceso**: El servidor (Flask/FastAPI) carga el `.pkl`, toma las variables promedio del municipio, corre el modelo, y consulta la cobertura en la API del gobierno.
- **Output**: Transforma el resultado en texto: *"Su zona en Palmira es de Aptitud Alta para Café, y como alternativa le sugerimos Banano."*

### Componente 2: Tablero Web (Dashboard Streamlit)
- **Input**: El usuario dibuja un polígono o hace clic en el mapa.
- **Proceso**: Streamlit extrae la lat/lon, consulta el DEM, pasa los datos por el `.pkl` y genera la predicción.
- **Simulador**: El alcalde puede mover un slider de precipitación (-20% por El Niño). El modelo vuelve a predecir y repinta el mapa mostrando cómo se reduce la aptitud del café.

---

## 💻 4. Requerimientos de Hardware y Alternativas Cloud

Entrenar un modelo de Machine Learning espacial (Kriging sobre miles de puntos) requiere consideraciones de infraestructura.

### Escenario Ideal (Local)
Para entrenar los 3 cultivos (Café, Banano, Cacao) sin tiempos de espera excesivos:
- **CPU**: Procesador multi-núcleo (ej. Intel Core i7 / AMD Ryzen 7 o superior) dado que Random Forest paraleliza muy bien (`n_jobs=-1`).
- **RAM**: Mínimo 16 GB (Recomendado 32 GB) para cargar la matriz espacial en memoria sin usar archivo de paginación.
- **GPU**: No es estrictamente requerida para Random Forest o Kriging Ordinario, ya que dependen principalmente de CPU y RAM.

### Alternativas en la Nube (Reducción drástica de tiempos)
Si tu equipo local es limitado, usar la nube te ahorrará horas de entrenamiento. Dado que el objetivo final es la API y la web, entrenar en la nube y descargar el `.pkl` es la mejor práctica:
1. **Google Colab Pro**: La opción más rápida y económica. Por ~$10 USD/mes te da acceso a máquinas con +50 GB de RAM y CPUs potentes. Entrenar el RFRK aquí tomaría una fracción del tiempo local.
2. **Kaggle Notebooks (Gratis)**: Ofrece hasta 30 GB de RAM y CPUs potentes. Excelente para ejecutar el script de entrenamiento sin costo alguno y exportar los modelos.
3. **AWS SageMaker / Azure ML**: Ideal para producción a gran escala (los 7 cultivos o a nivel nacional), pero requieren configuración de cuentas y pago por minuto de cómputo.

*Recomendación*: Codificaremos todo localmente con una muestra pequeña para asegurar que funciona (Debug). Para el entrenamiento final pesado de todo el Valle del Cauca, subiremos el notebook y el CSV consolidado a **Google Colab (versión gratuita o Pro)** para generar los `.pkl` finales en minutos.

---

## Verification Plan
1. **Consolidación**: Script que una Zonificaciones + Precipitación (T-014).
2. **Entrenamiento**: Script que separe datos de train/test y entrene el Random Forest (T-018).
3. **Métricas**: Validaremos con matriz de confusión (Aptitud) y RMSE/R2 (Rendimiento).
4. **Kriging**: Visualización de los residuos espaciales en un mapa de calor (T-020).
