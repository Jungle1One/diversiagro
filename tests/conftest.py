import pytest
from fastapi.testclient import TestClient
from src.backend.main import app

@pytest.fixture
def client():
    # Retorna un cliente de pruebas para FastAPI
    return TestClient(app)

@pytest.fixture(autouse=True)
def mock_ml_service(monkeypatch):
    """
    Mockea run_model_pipeline globalmente para que las pruebas de API
    no requieran cargar los modelos pesados de 130MB.
    """
    def fake_run_model_pipeline(cultivo, lat, lon, altitud, pendiente, lluvia, use_kriging=True):
        # Simulamos que siempre retorna una aptitud alta (3.0) para no romper el flujo
        return 2.5, 0.5, 3.0, "Aptitud alta"
        
    def fake_get_loaded_models():
        # Retorna un dict simulado para pasar la validación del endpoint
        return {"cafe": {"rf": "mock_model"}, "cacao": {"rf": "mock_model"}}
    
    monkeypatch.setattr("src.backend.routers.api.run_model_pipeline", fake_run_model_pipeline)
    monkeypatch.setattr("src.backend.routers.api.get_loaded_models", fake_get_loaded_models)
    
    # También mockeamos en caso de que lo usen otras rutas
    try:
        monkeypatch.setattr("src.backend.routers.twilio.run_model_pipeline", fake_run_model_pipeline)
    except AttributeError:
        pass

@pytest.fixture(autouse=True)
def mock_gis_service(monkeypatch):
    """
    Mockea get_gis_features para evitar cargar el DEM pesado durante los tests de API.
    """
    def fake_get_gis_features(lat, lon):
        return "Palmira", 1500.0, 10.0, 1200.0
        
    monkeypatch.setattr("src.backend.routers.api.get_gis_features", fake_get_gis_features)
    try:
        monkeypatch.setattr("src.backend.routers.twilio.get_gis_features", fake_get_gis_features)
    except AttributeError:
        pass
