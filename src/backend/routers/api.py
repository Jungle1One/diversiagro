from fastapi import APIRouter, HTTPException
from src.backend.schemas import PredictRequest, PredictCoordsRequest, PredictResponse, PredictCoordsResponse
from src.backend.services.ml_service import run_model_pipeline, get_loaded_models
from src.backend.services.gis_service import get_gis_features

router = APIRouter()

@router.post("/predict", response_model=PredictResponse)
async def predict_suitability(request: PredictRequest):
    cultivo = request.cultivo.lower()
    models = get_loaded_models()
    if cultivo not in models or models[cultivo]['rf'] is None:
        raise HTTPException(status_code=404, detail=f"Modelos para el cultivo '{cultivo}' no están disponibles.")
    
    try:
        rf, krig, final, apt = run_model_pipeline(
            cultivo, request.lat, request.lon, 
            request.altitud_msnm, request.pendiente_grados, request.precipitacion_anual_mm
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
    return PredictResponse(
        cultivo=cultivo, rf_score=rf, kriging_correction=krig, 
        final_score=final, aptitud_label=apt
    )

@router.post("/predict_from_coords", response_model=PredictCoordsResponse)
async def predict_from_coords(request: PredictCoordsRequest):
    cultivo = request.cultivo.lower()
    models = get_loaded_models()
    if cultivo not in models or models[cultivo]['rf'] is None:
        raise HTTPException(status_code=404, detail="Modelo no disponible.")
        
    lat, lon = request.lat, request.lon
    municipio_str, altitud, pendiente, lluvia = get_gis_features(lat, lon)
    
    try:
        rf, krig, final, apt = run_model_pipeline(cultivo, lat, lon, altitud, pendiente, lluvia)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
    return PredictCoordsResponse(
        cultivo=cultivo,
        lat=lat, lon=lon,
        municipio_detectado=municipio_str,
        altitud_extraida=altitud,
        pendiente_extraida=pendiente,
        lluvia_extraida=lluvia,
        rf_score=rf,
        kriging_correction=krig,
        final_score=final,
        aptitud_label=apt
    )

@router.get("/health")
async def health_check():
    return {"status": "ok", "message": "Motor de IA Agrícola Operativo"}

@router.get("/municipio/{nombre}")
async def get_municipio_location(nombre: str):
    from src.backend.services.gis_service import gdf_municipios, normalize_text
    from fastapi import HTTPException
    
    if gdf_municipios is None:
        raise HTTPException(status_code=500, detail="Datos GIS no cargados")
        
    nombre_norm = normalize_text(nombre)
    if nombre_norm == "TODOS":
        return {"lat": 3.4372, "lon": -76.5225, "zoom": 8}
        
    if 'MPIO_NORM' in gdf_municipios.columns:
        match = gdf_municipios[gdf_municipios['MPIO_NORM'] == nombre_norm]
        if not match.empty:
            geom = match.iloc[0].geometry
            centroid = geom.centroid
            return {"lat": centroid.y, "lon": centroid.x, "zoom": 11}
            
    return {"lat": 3.4372, "lon": -76.5225, "zoom": 8}
