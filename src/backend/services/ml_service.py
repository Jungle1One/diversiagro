import joblib
import pandas as pd
import numpy as np
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
MODELS_DIR = BASE_DIR / 'models'

models = {
    'cafe': {'rf': None, 'kriging': None},
    'cacao': {'rf': None, 'kriging': None},
    'aguacate': {'rf': None, 'kriging': None},
    'cana_panelera': {'rf': None, 'kriging': None},
    'fresa': {'rf': None, 'kriging': None},
}

INV_APTITUD_MAP = {
    3: 'Aptitud alta',
    2: 'Aptitud media',
    1: 'Aptitud baja',
    0: 'No apta'
}

def load_models():
    for cultivo in models.keys():
        rf_path = MODELS_DIR / f"modelo_{cultivo}_rf.pkl"
        ok_path = MODELS_DIR / f"modelo_{cultivo}_kriging.pkl"
        try:
            if rf_path.exists(): models[cultivo]['rf'] = joblib.load(rf_path)
            if ok_path.exists(): models[cultivo]['kriging'] = joblib.load(ok_path)
        except Exception as e:
            print(f"Error cargando modelos para {cultivo}: {e}")

def clasificar_prediccion(pred_val):
    return int(np.clip(np.round(pred_val), 0, 3))

def run_model_pipeline(cultivo, lat, lon, altitud, pendiente, lluvia, use_kriging=True):
    rf_model = models[cultivo]['rf']
    ok_model = models[cultivo]['kriging']
    
    if rf_model is None:
        raise ValueError(f"Modelo para el cultivo '{cultivo}' no está disponible.")
    
    X_input = pd.DataFrame([{
        'altitud_msnm': altitud,
        'pendiente_grados': pendiente,
        'precipitacion_anual_mm': lluvia
    }])
    
    rf_pred = rf_model.predict(X_input)[0]
    
    if ok_model is not None and use_kriging:
        try:
            krige_pred, _ = ok_model.execute('points', [lon], [lat])
            residuo = krige_pred.data[0]
        except Exception:
            residuo = 0.0
    else:
        residuo = 0.0
        
    pred_final = float(rf_pred + residuo)
    aptitud = INV_APTITUD_MAP[clasificar_prediccion(pred_final)]
    
    return float(rf_pred), float(residuo), pred_final, aptitud

def get_loaded_models():
    return models
