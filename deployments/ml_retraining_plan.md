# 🧠 Plan de Re-Entrenamiento (MLOps)

Los modelos híbridos **Random Forest + Kriging** en `DiversIAgro` capturan relaciones espaciales y climáticas. Sin embargo, el clima cambia y la UPRA puede liberar nuevas versiones de sus mapas de aptitud agropecuaria.

Para evitar la "degradación del modelo" (Model Drift), proponemos el siguiente ciclo de vida de Machine Learning (MLOps).

## 1. ¿Cuándo re-entrenar? (Triggers)

No se requiere entrenamiento en tiempo real. Se sugiere una de las siguientes políticas:
1. **Trigger Basado en Tiempo:** Ejecutar el pipeline de re-entrenamiento una vez al año (ej. Enero) para absorber las nuevas anomalías climáticas registradas por el IDEAM.
2. **Trigger Basado en Datos:** Re-entrenar de inmediato si la **UPRA** publica un nuevo shapefile/geojson con zonificaciones actualizadas para los cultivos objetivo en el Valle del Cauca.

## 2. Pipeline de Actualización (El Paso a Paso)

Si ocurre un Trigger, el Administrador del Sistema debe seguir esta receta:

### Paso A: Adquisición de Nuevos Datos
- Descargar el archivo más reciente del IDEAM de precipitación.
- Reemplazar el archivo `data/processed/ideam_precipitacion_anual_municipio.csv`.
- (Si aplica) Descargar los nuevos mapas de zonificación de la UPRA y reemplazar los `.geojson` en `data/processed/`.

### Paso B: Consolidación
El Administrador debe cruzar los datos espacialmente utilizando el script automatizado:
```bash
python src/features/consolidate_training_data.py
```
> [!IMPORTANT]
> El script incluye un sistema de seguridad (Clipping) que evita que valores atípicos absurdos (ej. 280,000 mm de lluvia por un error de tipeo en IDEAM) corrompan el modelo. Los datos se restringen automáticamente a un rango de 500-8000mm.

### Paso C: Entrenamiento
Entrenar los 5 cultivos:
```bash
python src/train.py
```
Esto sobrescribirá los `.pkl` en la carpeta `models/`. El script mostrará automáticamente el **RMSE** y **R²** de Random Forest, así como la Importancia de Variables (Feature Importance).

## 3. Criterios de Aceptación (Rollback)
Al entrenar, observa el **R² (R-Cuadrado)** en la consola:
- Si el R² de Random Forest es **mayor a 0.85**, el modelo está listo para producción.
- Si cae drásticamente (ej. < 0.70), hubo una ruptura en la calidad de los datos de entrada (Data Quality Issue). **No lo despliegues** y revisa los CSV/GeoJSON.

## 4. Despliegue de los Nuevos Modelos (Zero-Downtime)
1. Commit de los nuevos `.pkl` al repositorio.
2. Hacer `git pull` en el servidor de producción.
3. El backend recargará los modelos en memoria si se reinicia el servicio o el contenedor de Docker:
   ```bash
   docker restart diversiagro-backend
   ```
