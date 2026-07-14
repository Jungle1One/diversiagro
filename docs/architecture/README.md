# 🏗️ Arquitectura del Sistema (DiversIAgro)

DiversIAgro está diseñado utilizando un patrón de arquitectura **desacoplada (Client-Server)** y orientada a microservicios lógicos, lo cual garantiza escalabilidad y facilidad de mantenimiento.

## Diagrama de Arquitectura Global

```mermaid
graph TD
    %% Usuarios
    Campesino[Campesino (Llamada Telefónica)]
    Funcionario[Funcionario / Extensión (Web)]
    
    %% Canales
    Twilio[Twilio Voice API]
    Streamlit[Frontend: Streamlit]
    
    %% Backend
    FastAPI[Backend: FastAPI]
    NLU[NLU: Gemini 2.5 Flash]
    GIS[GIS Service: GeoPandas & Rasterio]
    ML[ML Service: Random Forest + PyKrige]
    
    %% Datos
    DEM[(DEM SRTM 30m)]
    Models[(Modelos .pkl)]
    
    %% Flujo Telefónico
    Campesino --Llamada de voz--> Twilio
    Twilio --HTTP POST /twilio/voice--> FastAPI
    FastAPI --Extraer Lugar (Speech)--> NLU
    
    %% Flujo Web
    Funcionario --Clic en Mapa--> Streamlit
    Streamlit --HTTP POST /api/predict--> FastAPI
    
    %% Procesamiento
    FastAPI --Coordenadas--> GIS
    GIS --Lee TIF--> DEM
    GIS --Elevación, Pendiente, Lluvia--> FastAPI
    
    FastAPI --Features--> ML
    ML --Carga Pesos--> Models
    ML --Retorna Aptitud--> FastAPI
    
    FastAPI --Respuesta XML (TwiML)--> Twilio
    FastAPI --Respuesta JSON--> Streamlit
```

## Componentes Clave

1. **Frontend (Streamlit):**
   - Responsable de la interfaz gráfica e interactiva (Mapa interactivo con Folium).
   - Realiza peticiones asíncronas al backend (REST) permitiendo que las tarjetas de evaluación se dibujen de manera dinámica (en tiempo real) sin bloquear la interfaz.

2. **Capa de Voz (Twilio + NLU):**
   - Twilio intercepta las llamadas de la línea telefónica y convierte la voz a texto (STT).
   - El texto se envía a `nlu_service.py`, donde Gemini extrae la entidad espacial (Municipio y Vereda) y devuelve coordenadas estimadas para alimentar el motor de IA geográfico sin que el campesino tenga que saber qué es una coordenada.

3. **Backend Core (FastAPI):**
   - Sirve como orquestador.
   - Contiene la lógica GIS en memoria (extrae píxeles de elevación e intersecta geometrías en microsegundos).
   - Inyecta los features extraídos al modelo híbrido (Random Forest + Kriging).
