# ✅ Guía de Validación (Peer Review)

Esta guía está diseñada para que evaluadores de la convocatoria, jurados técnicos o pares académicos puedan descargar, configurar y verificar que DiversIAgro funciona tal y como se describe.

## 1. Requisitos Previos (Pre-requisitos)
- Tener **Python 3.10+** instalado.
- Opcional: **Docker** si deseas evaluarlo en contenedor.
- Descargar los datos pesados (Modelos `.pkl` y el DEM `.tif`) siguiendo las instrucciones de los archivos `ESTRUCTURA.md` en las carpetas `data/` y `models/`. (Ver [fuentes_datos.md](fuentes_datos.md) para más detalle).

## 2. Validación Automatizada (Pruebas Unitarias)
Hemos implementado una suite completa para validar la lógica pura sin levantar los servidores.
Abre una terminal en la raíz del proyecto y ejecuta:

```bash
# Crear entorno virtual e instalar todo (incluyendo pytest)
python -m venv .venv
# En Windows: .\.venv\Scripts\activate
# En Linux/Mac: source .venv/bin/activate

pip install -r requirements.txt
pip install pytest httpx

# Ejecutar la suite
pytest tests/
```
> **Resultado Esperado:** 100% de las pruebas deben pasar (color verde), validando la conectividad de la API, el manejo de errores del Machine Learning y la normalización GIS.

## 3. Validación de Inferencia y UX Visual (Streamlit)
Para ver el sistema en vivo:
1. Inicia el sistema orquestador:
   ```bash
   python run.py
   ```
2. Se abrirán dos procesos. El frontend estará en `http://localhost:8501`.
3. Haz clic en cualquier parte del mapa del Valle del Cauca.
4. El sistema calculará en tiempo real tu Elevación, Pendiente y Lluvia Anual usando el DEM, y cargará las tarjetas con la "Aptitud" para Café, Cacao, Aguacate, Caña y Fresa de forma secuencial.

## 4. Validación de Arquitectura
- Revisa el archivo de **Pipeline Principal:** `src/backend/services/ml_service.py` -> Función `run_model_pipeline()`. Ahí podrás validar cómo se cargan los tensores para Random Forest y cómo se aplica la corrección residual por Kriging.
- Revisa el **Flujo Telefónico:** `src/backend/routers/twilio.py`. Analiza cómo recibimos un XML y retornamos TwiML (XML) inyectando la respuesta de nuestra IA.
