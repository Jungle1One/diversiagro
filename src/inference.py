import joblib
import numpy as np
import pandas as pd
from pathlib import Path
import warnings

warnings.filterwarnings('ignore')

BASE_DIR = Path(__file__).resolve().parent.parent
MODELS_DIR = BASE_DIR / 'models'

# Diccionario para traducir el número predicho de vuelta a texto
INV_APTITUD_MAP = {
    3: 'Aptitud alta',
    2: 'Aptitud media',
    1: 'Aptitud baja',
    0: 'No apta'
}

def clasificar_prediccion(pred_val):
    # Redondea el número continuo a la clase más cercana [0, 1, 2, 3]
    return int(np.clip(np.round(pred_val), 0, 3))

def test_modelo(cultivo, altitud, pendiente, lluvia, lon, lat):
    print(f"\n{'-'*50}\nPRUEBA DE MODELO: {cultivo.upper()}\n{'-'*50}")
    
    rf_path = MODELS_DIR / f'modelo_{cultivo}_rf.pkl'
    kriging_path = MODELS_DIR / f'modelo_{cultivo}_kriging.pkl'
    
    if not rf_path.exists() or not kriging_path.exists():
        print(f"ERROR: No se encontraron los modelos para {cultivo} en {MODELS_DIR}")
        return
        
    print("1. Cargando modelos...")
    rf_model = joblib.load(rf_path)
    ok_model = joblib.load(kriging_path)
    
    print("\n2. Parámetros de la simulación:")
    print(f"   Coordenadas: Lon {lon}, Lat {lat}")
    print(f"   Altitud: {altitud} msnm | Pendiente: {pendiente}°")
    print(f"   Precipitación Anual: {lluvia} mm")
    
    # Predecir con Random Forest
    # El modelo espera un DataFrame con los mismos nombres de columnas con los que se entrenó
    X_input = pd.DataFrame([{
        'altitud_msnm': altitud,
        'pendiente_grados': pendiente,
        'precipitacion_anual_mm': lluvia
    }])
    
    rf_pred = rf_model.predict(X_input)[0]
    
    # Predecir con Kriging (Residual espacial)
    # execute() devuelve (prediccion, varianza)
    krige_pred, krige_var = ok_model.execute('points', [lon], [lat])
    residuo = krige_pred.data[0]
    
    # Predicción Final Híbrida = RF (Bioclimático) + Kriging (Ajuste Espacial)
    pred_final_numerica = rf_pred + residuo
    
    # Convertir número a categoría
    categoria_final = INV_APTITUD_MAP[clasificar_prediccion(pred_final_numerica)]
    
    print("\n3. Resultados del Modelo RFRK:")
    print(f"   Predicción Bioclimática pura (RF): {rf_pred:.2f} / 3.0")
    print(f"   Corrección Espacial (Kriging): {residuo:+.2f} puntos")
    print(f"   =================================================")
    print(f"   Puntuación Final: {pred_final_numerica:.2f} / 3.0")
    print(f"   CLASIFICACIÓN FINAL: {categoria_final.upper()}")

def main():
    print("Iniciando suite de pruebas para los modelos generados...")
    
    # PRUEBA 1: Condiciones Ideales para Café (Altitud media, lluvia moderada)
    # Usaremos una coordenada cerca a la cordillera central en el Valle
    test_modelo(
        cultivo='cafe',
        altitud=1400,          # Altitud perfecta para café
        pendiente=15,          # Laderas
        lluvia=1800,           # Lluvia ideal
        lon=-76.2,             # Longitud Valle del Cauca (aprox Buga loma)
        lat=3.9                # Latitud Valle del Cauca
    )
    
    # PRUEBA 2: Condiciones Extremas (Páramo) - Debería ser No Apto
    test_modelo(
        cultivo='cafe',
        altitud=3800,          # Páramo helado
        pendiente=45,          # Precipicio
        lluvia=3000,           # Exceso de lluvia
        lon=-76.0,
        lat=3.8
    )
    
    # PRUEBA 3: Banano en zona plana y cálida
    test_modelo(
        cultivo='banano',
        altitud=900,           # Clima cálido
        pendiente=2,           # Terreno plano
        lluvia=1500,
        lon=-76.3,
        lat=3.5
    )

if __name__ == "__main__":
    main()
