import pytest
from src.backend.services.ml_service import clasificar_prediccion, run_model_pipeline

def test_clasificar_prediccion():
    # Valores negativos o muy bajos
    assert clasificar_prediccion(-1.5) == 0
    assert clasificar_prediccion(0.2) == 0
    
    # Valores medios
    assert clasificar_prediccion(1.1) == 1
    assert clasificar_prediccion(1.8) == 2
    
    # Valores altos o excesivos
    assert clasificar_prediccion(2.9) == 3
    assert clasificar_prediccion(5.0) == 3

def test_run_model_pipeline_missing_model():
    # Limpiamos el estado global si estuviera cargado
    from src.backend.services.ml_service import models
    # Simulamos que no está el modelo de una fruta inventada
    models['manzana'] = {'rf': None, 'kriging': None}
    
    with pytest.raises(ValueError) as excinfo:
        run_model_pipeline('manzana', 3.5, -76.2, 1000, 5, 1500)
        
    assert "no está disponible" in str(excinfo.value)
