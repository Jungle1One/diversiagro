# 🔌 API Specification (DiversIAgro)

Este documento detalla los endpoints RESTful expuestos por el Backend (FastAPI).

## 1. Predicción desde Coordenadas

Evalúa la aptitud de un cultivo específico calculando variables climáticas topográficas al vuelo.

**URL:** `/api/predict_from_coords`
**Method:** `POST`
**Content-Type:** `application/json`

### Payload de Ejemplo
```json
{
  "cultivo": "cafe",
  "lat": 3.48,
  "lon": -76.23
}
```

### Respuesta de Ejemplo (200 OK)
```json
{
  "cultivo": "cafe",
  "rf_score": 2.45,
  "kriging_correction": -0.1,
  "final_score": 2.35,
  "aptitud_label": "Aptitud media",
  "municipio_detectado": "Palmira",
  "altitud_extraida": 1500.5,
  "pendiente_extraida": 12.3,
  "lluvia_extraida": 1800.0
}
```

### Errores Comunes
- `404 Not Found`: Si el modelo del cultivo solicitado no existe o no ha sido entrenado.

---

## 2. Búsqueda de Municipios

Encuentra el centroide (latitud y longitud central) de cualquier municipio normalizado para centrar el mapa.

**URL:** `/api/municipio/{nombre_municipio}`
**Method:** `GET`

### Respuesta de Ejemplo (200 OK)
```json
{
  "lat": 3.4372,
  "lon": -76.5225,
  "zoom": 11
}
```

---

## 3. Webhooks de Twilio (Voice)

Estos endpoints no devuelven JSON, devuelven XML estructurado en formato **TwiML** para dictar instrucciones de voz.

- **`POST /twilio/voice`**: Recibe la llamada entrante e inicia el módulo de recolección de voz pidiendo al campesino su municipio.
- **`POST /twilio/process_speech_redirect`**: Recibe el texto transcrito de la voz, usa el NLU de Gemini para extraer la vereda y redirecciona al menú de acciones.
- **`POST /twilio/menu_action`**: Según la tecla presionada (1 o 2), evalúa el clima actual (OpenMeteo) o corre los modelos de aptitud agrícola (desactivando Kriging para cumplir con el timeout de <15 segundos de Twilio).
