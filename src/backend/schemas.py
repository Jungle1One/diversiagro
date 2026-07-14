from pydantic import BaseModel, Field
from typing import List, Dict

class PredictRequest(BaseModel):
    cultivo: str = Field(..., description="Nombre del cultivo (cafe, banano, cacao)")
    lat: float = Field(..., description="Latitud de la coordenada")
    lon: float = Field(..., description="Longitud de la coordenada")
    altitud_msnm: float = Field(..., description="Altitud en metros sobre el nivel del mar")
    pendiente_grados: float = Field(..., description="Pendiente del terreno en grados")
    precipitacion_anual_mm: float = Field(..., description="Lluvia anual en milímetros")

class PredictCoordsRequest(BaseModel):
    cultivo: str = Field(..., description="Nombre del cultivo")
    lat: float = Field(..., description="Latitud de la coordenada")
    lon: float = Field(..., description="Longitud de la coordenada")

class PredictResponse(BaseModel):
    cultivo: str
    rf_score: float
    kriging_correction: float
    final_score: float
    aptitud_label: str

class PredictCoordsResponse(PredictResponse):
    municipio_detectado: str
    altitud_extraida: float
    pendiente_extraida: float
    lluvia_extraida: float

