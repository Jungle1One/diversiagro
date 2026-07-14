# 🚀 Despliegue del Backend (FastAPI + ML)

El backend de **DiversIAgro** ejecuta la Inteligencia Artificial (Random Forest + Kriging), sirve la API REST y maneja los webhooks de voz (Twilio). Debido a las operaciones geoespaciales matriciales, el backend requiere un hardware robusto.

## 1. Requisitos de Hardware (Servidor)

Para manejar las matrices de datos en memoria (DEM de 80MB, modelos serializados ~130MB, y procesamiento concurrente):
*   **Memoria RAM**: 2 GB Mínimo (4 GB Recomendado).
*   **CPU**: 2 vCPUs (Importante para evitar bloqueos del GIL de Python durante inferencias simultáneas).
*   **Almacenamiento**: 20 GB SSD.
*   **OS Sugerido**: Ubuntu 22.04 LTS.

## 2. Variables de Entorno Requeridas

Antes de desplegar, asegúrate de configurar estas variables en tu servidor o archivo `.env`:

```env
GEMINI_API_KEY="AIzaSy..." # Clave para el motor NLU (Twilio Voice)
CORS_ORIGINS="*"           # O restringe a la IP de tu frontend
```

## 3. Opciones de Despliegue

### Opción A: Despliegue con Docker (Recomendado)
Docker encapsula dependencias difíciles como GDAL (necesario para `rasterio` y `geopandas`), asegurando que corra perfecto en cualquier nube.

1. Instalar Docker en el servidor (Ej: DigitalOcean Droplet, AWS EC2).
2. Clona el proyecto y ve a la raíz.
3. Ejecuta el orquestador:
   ```bash
   docker-compose up -d backend
   ```
4. El servidor estará escuchando en el puerto `8000`.

### Opción B: Plataformas PaaS (Render / Heroku)
Si prefieres no administrar el sistema operativo, puedes usar Render (Web Service):
1. Conecta tu repositorio de GitHub.
2. Selecciona **Docker** como el "Environment".
3. **Build Command**: Render detectará automáticamente el `Dockerfile.backend`.
4. **Plan**: Al menos el "Starter" de $7/mes (512MB podría quedarse sin memoria, se sugiere el plan de 2GB por $15/mes).

## 4. Conexión de Twilio en Producción
Una vez el backend esté en vivo (ej: `http://198.51.100.12:8000` o `https://mi-api.render.com`), debes ir a la consola de Twilio y actualizar el Webhook de tu número telefónico:

*   **A CALL COMES IN** -> Webhook -> `https://tu-dominio.com/api/voice` -> HTTP POST.
