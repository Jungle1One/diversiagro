# 🌐 Despliegue del Frontend (Streamlit)

El frontend de **DiversIAgro** está construido en Streamlit. Es ligero y no requiere una gran capacidad de procesamiento, ya que toda la carga pesada (Machine Learning y GIS) la realiza el Backend.

## 1. Requisitos de Hardware

*   **Memoria RAM**: 512 MB a 1 GB.
*   **CPU**: 1 vCPU.
*   **Almacenamiento**: 5 GB.

## 2. Variables de Entorno Requeridas

El frontend necesita saber dónde está alojado el backend para enviarle las peticiones.
Debes configurar esta variable antes de lanzar la app o cambiarla directamente en `app.py`:

```env
API_URL="https://mi-backend.com/api" # Cambiar por la IP/Dominio de tu servidor Backend
```
*(Si no se define, por defecto usa `http://127.0.0.1:8000/api` que solo sirve para desarrollo local)*

## 3. Opciones de Despliegue

### Opción A: Streamlit Community Cloud (¡Gratis y Recomendado!)
Esta es la forma más fácil y gratuita de alojar el Frontend si tu código está en GitHub.

1. Sube tu código a un repositorio público (o privado) en GitHub.
2. Ve a [share.streamlit.io](https://share.streamlit.io/) e inicia sesión con GitHub.
3. Haz clic en **"New app"**.
4. Selecciona tu repositorio, la rama (`main`) y el archivo principal: `src/frontend/app.py`.
5. Haz clic en **"Deploy"**.
6. Una vez desplegada, ve a la configuración de la app ("Settings" -> "Secrets") y agrega la URL de tu backend:
   ```toml
   API_URL = "https://tu-backend-produccion.com/api"
   ```

### Opción B: Despliegue con Docker (Mismo servidor que el Backend)
Si rentaste un servidor potente (ej. 4GB RAM) para el backend, puedes alojar el frontend ahí mismo usando Docker Compose.

1. En tu servidor, edita el archivo `docker-compose.yml` para incluir el servicio de frontend.
2. Levanta todo:
   ```bash
   docker-compose up -d
   ```
3. El frontend estará disponible en el puerto `8501`. (Asegúrate de abrir este puerto en el Firewall de tu servidor/nube).
