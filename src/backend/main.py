from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from src.backend.services.gis_service import load_gis_data
from src.backend.services.ml_service import load_models
from src.backend.routers import api, twilio

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("[INFO] Cargando recursos al arrancar...")
    load_gis_data()
    load_models()
    yield
    print("[INFO] Apagando el servidor...")

app = FastAPI(
    title="API de Zonificación Agrícola (Valle del Cauca)",
    description="Motor RFRK para predecir la aptitud agrícola basada en variables topoclimáticas con soporte GIS en tiempo real.",
    version="1.1.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api.router, prefix="/api", tags=["Predictive Models"])
app.include_router(twilio.router, prefix="/twilio", tags=["IVR Voice"])
