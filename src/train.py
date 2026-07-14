"""
Pipeline de entrenamiento RFRK (Random Forest + Regression Kriging)
para predicción de aptitud agrícola en el Valle del Cauca, Colombia.

Modelo híbrido:
  1. Random Forest Regressor — captura relación bioclimática (altitud, pendiente, precipitación)
  2. Ordinary Kriging — interpola el residuo espacial (autocorrelación geográfica del error)

Fuentes de datos:
  - Zonificaciones de aptitud UPRA (target ordinal 0-3)
  - DEM SRTM 30m procesado (altitud, pendiente)
  - Precipitación IDEAM agregada por municipio

Uso:
  (.env-1) python src/train.py
"""

import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, confusion_matrix
from pykrige.ok import OrdinaryKriging
import joblib
import warnings
import time

warnings.filterwarnings('ignore')

# --- Configuración ---
BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = BASE_DIR / 'data' / 'processed'
MODELS_DIR = BASE_DIR / 'models'
MODELS_DIR.mkdir(exist_ok=True)

# Cultivos objetivo para diversificación cafetera en Valle del Cauca
CULTIVOS = ['cafe', 'cacao', 'aguacate', 'cana_panelera', 'fresa']

# Codificación ordinal de las categorías UPRA.
# "Exclusión legal" (parques naturales, páramos) se descarta intencionalmente:
# no tiene sentido predecir aptitud agronómica en zonas legalmente restringidas.
APTITUD_MAP = {
    'Aptitud alta': 3,
    'Aptitud media': 2,
    'Aptitud baja': 1,
    'No apta': 0
}

FEATURES = ['altitud_msnm', 'pendiente_grados', 'precipitacion_anual_mm']

# Rango realista de precipitación para Valle del Cauca (mm/año).
# Valores fuera de este rango en los datos IDEAM son errores de agregación.
PRECIP_MIN, PRECIP_MAX = 500.0, 8000.0

# Hiperparámetros RF
RF_N_ESTIMATORS = 200
RF_MAX_DEPTH = 20
RF_RANDOM_STATE = 42

# Kriging: máximo de puntos para ajustar el semivariograma (complejidad O(N³))
MAX_KRIGING_POINTS = 4000


def sanitize_precipitation(df: pd.DataFrame) -> pd.DataFrame:
    """Clip de precipitación a rango físicamente plausible para Valle del Cauca."""
    col = 'precipitacion_anual_mm'
    n_outliers = ((df[col] < PRECIP_MIN) | (df[col] > PRECIP_MAX)).sum()
    if n_outliers > 0:
        print(f"   [SANITIZE] {n_outliers} registros con precipitación fuera de [{PRECIP_MIN}, {PRECIP_MAX}] mm → clipped")
    df[col] = df[col].clip(lower=PRECIP_MIN, upper=PRECIP_MAX)
    return df


def discretize(pred: np.ndarray) -> np.ndarray:
    """Redondea predicción continua del regresor a clase ordinal {0, 1, 2, 3}."""
    return np.clip(np.round(pred), 0, 3).astype(int)


def train_rfrk(cultivo: str) -> None:
    """Entrena el pipeline RFRK completo para un cultivo y persiste los artefactos."""
    t0 = time.time()
    print(f"\n{'='*60}")
    print(f"  RFRK TRAINING — {cultivo.upper()}")
    print(f"{'='*60}")

    # --- 1. Carga y validación de datos ---
    file_path = PROCESSED_DIR / f'dataset_ml_{cultivo}.csv'
    if not file_path.exists():
        print(f"  [ERROR] Dataset no encontrado: {file_path}")
        print(f"  [HINT] Ejecutar primero: python src/features/consolidate_training_data.py")
        return

    df = pd.read_csv(file_path)

    # Codificar target ordinal. Categorías no mapeadas (ej. "Exclusión legal") → NaN → eliminadas
    df['y_target'] = df['aptitud'].map(APTITUD_MAP)
    n_excluidos = df['y_target'].isna().sum()
    if n_excluidos > 0:
        categorias_desc = df.loc[df['y_target'].isna(), 'aptitud'].value_counts().to_dict()
        print(f"  [FILTER] {n_excluidos} polígonos descartados por categorías no modelables: {categorias_desc}")

    required_cols = ['y_target'] + FEATURES + ['lon_x', 'lat_y']
    df = df.dropna(subset=required_cols)

    # Sanitizar precipitación
    df = sanitize_precipitation(df)

    X = df[FEATURES]
    y = df['y_target']

    # Diagnóstico de distribución de clases
    dist = y.value_counts().sort_index()
    print(f"  [DATA] {len(df):,} muestras válidas. Distribución de clases:")
    for cls_val, count in dist.items():
        label = {3: 'Alta', 2: 'Media', 1: 'Baja', 0: 'No apta'}.get(int(cls_val), '?')
        print(f"         {label} ({int(cls_val)}): {count:,}  ({100*count/len(df):.1f}%)")

    # --- 2. Split estratificado ---
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=RF_RANDOM_STATE, stratify=y
    )

    # --- 3. Random Forest Regressor (componente bioclimático) ---
    print(f"\n  [RF] Entrenando RandomForestRegressor (n={RF_N_ESTIMATORS}, depth={RF_MAX_DEPTH})...")
    rf = RandomForestRegressor(
        n_estimators=RF_N_ESTIMATORS,
        max_depth=RF_MAX_DEPTH,
        random_state=RF_RANDOM_STATE,
        n_jobs=-1
    )
    rf.fit(X_train, y_train)

    # Evaluación
    y_pred = rf.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)
    print(f"  [RF] RMSE={rmse:.4f}  R²={r2:.4f}")

    y_pred_cls = discretize(y_pred)
    cm = confusion_matrix(y_test.values.astype(int), y_pred_cls, labels=[0, 1, 2, 3])
    print(f"  [RF] Confusion Matrix (filas=real, cols=pred):\n{cm}")

    # Feature importance
    importances = dict(zip(FEATURES, rf.feature_importances_))
    print(f"  [RF] Feature importance: {', '.join(f'{k}={v:.3f}' for k, v in importances.items())}")

    # --- 4. Residuos espaciales para Kriging ---
    print(f"\n  [KRIGING] Calculando residuos sobre dataset completo...")
    df['rf_pred'] = rf.predict(X)
    df['residuo'] = df['y_target'] - df['rf_pred']
    print(f"  [KRIGING] Residuo medio={df['residuo'].mean():.4f}, std={df['residuo'].std():.4f}")

    # Muestreo estratificado para Kriging (O(N³) hace inviable usar >5000 puntos)
    if len(df) > MAX_KRIGING_POINTS:
        print(f"  [KRIGING] Submuestreo estratificado: {MAX_KRIGING_POINTS}/{len(df)} puntos")
        try:
            df_krig, _ = train_test_split(
                df, train_size=MAX_KRIGING_POINTS, random_state=RF_RANDOM_STATE, stratify=df['y_target']
            )
        except ValueError:
            # Clases con <2 muestras impiden stratify → fallback aleatorio
            df_krig = df.sample(MAX_KRIGING_POINTS, random_state=RF_RANDOM_STATE)
    else:
        df_krig = df

    # --- 5. Ordinary Kriging sobre residuos ---
    print(f"  [KRIGING] Ajustando semivariograma esférico ({len(df_krig)} puntos)...")
    krige_success = False
    try:
        ok = OrdinaryKriging(
            df_krig['lon_x'].values,
            df_krig['lat_y'].values,
            df_krig['residuo'].values,
            variogram_model='spherical',
            verbose=False,
            enable_plotting=False
        )
        krige_success = True
        print(f"  [KRIGING] Semivariograma ajustado correctamente")
    except Exception as e:
        print(f"  [KRIGING] ERROR en ajuste (posibles duplicados/singularidades): {e}")

    # --- 6. Persistencia de artefactos ---
    rf_path = MODELS_DIR / f'modelo_{cultivo}_rf.pkl'
    joblib.dump(rf, rf_path)
    print(f"\n  [SAVE] RF → {rf_path.name}")

    if krige_success:
        ok_path = MODELS_DIR / f'modelo_{cultivo}_kriging.pkl'
        joblib.dump(ok, ok_path)
        print(f"  [SAVE] Kriging → {ok_path.name}")
    else:
        print(f"  [WARN] Kriging no se guardó. El modelo operará solo con RF (sin corrección espacial).")

    elapsed = time.time() - t0
    print(f"  [DONE] {cultivo.upper()} completado en {elapsed:.1f}s")
    print(f"{'='*60}")


def main():
    print("\n" + "▓"*60)
    print("  DiversIAgro — Entrenamiento RFRK Multicultivo")
    print(f"  Cultivos: {', '.join(c.upper() for c in CULTIVOS)}")
    print("▓"*60)

    t_total = time.time()
    for cultivo in CULTIVOS:
        train_rfrk(cultivo)

    print(f"\n{'▓'*60}")
    print(f"  Pipeline finalizado. Tiempo total: {time.time()-t_total:.1f}s")
    print(f"  Modelos en: {MODELS_DIR}")
    print(f"{'▓'*60}\n")


if __name__ == "__main__":
    main()
