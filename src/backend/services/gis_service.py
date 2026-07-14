import pandas as pd
import geopandas as gpd
import rasterio
from shapely.geometry import Point
import unicodedata
from pathlib import Path
import numpy as np

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
DEM_PATH = BASE_DIR / 'data' / 'processed' / 'DEM_Valle_Cauca_Elevacion_y_Pendiente.tif'
GEOJSON_PATH = BASE_DIR / 'data' / 'raw' / 'mmra_conglomerados_valle.geojson'
PRECIP_PATH = BASE_DIR / 'data' / 'processed' / 'ideam_precipitacion_anual_municipio.csv'

dem_dataset = None
gdf_municipios = None
precip_dict = {}

def normalize_text(text):
    if not isinstance(text, str): return ""
    text = text.replace('?', '')
    text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('utf-8')
    return text.upper().strip()

def load_gis_data():
    global dem_dataset, gdf_municipios, precip_dict
    try:
        if DEM_PATH.exists():
            dem_dataset = rasterio.open(DEM_PATH)
            
        if GEOJSON_PATH.exists():
            gdf_municipios = gpd.read_file(GEOJSON_PATH)
            if 'NOMBREMUNICIPIO_CG' in gdf_municipios.columns:
                gdf_municipios['MPIO_NORM'] = gdf_municipios['NOMBREMUNICIPIO_CG'].apply(normalize_text)
                
        if PRECIP_PATH.exists():
            df_precip = pd.read_csv(PRECIP_PATH)
            df_precip['muni_norm'] = df_precip['municipio'].apply(normalize_text)
            precip_dict = dict(zip(df_precip['muni_norm'], df_precip['precipitacion_anual_mm']))
    except Exception as e:
        print(f"[ERROR] Falló la carga GIS: {e}")

async def get_municipio_centroid(municipio: str):
    try:
        texto_norm = normalize_text(municipio).lower()
        if gdf_municipios is not None and 'MPIO_NORM' in gdf_municipios.columns:
            for _, row in gdf_municipios.iterrows():
                if str(row['MPIO_NORM']).lower() in texto_norm:
                    geom = row['geometry']
                    if geom is not None:
                        centro = geom.centroid
                        return {"lat": centro.y, "lon": centro.x}
    except Exception as e:
        print(f"Error centroid: {e}")
    return {"lat": 3.4372, "lon": -76.5225}

def get_gis_features(lat: float, lon: float):
    # 1. Extraer Altitud y Pendiente del DEM
    altitud = 1200.0
    pendiente = 10.0
    if dem_dataset is not None:
        try:
            gen = dem_dataset.sample([(lon, lat)])
            val = next(gen)
            if val[0] != dem_dataset.nodata:
                altitud = float(val[0])
                pendiente = float(val[1]) if len(val) > 1 else 0.0
        except Exception:
            pass
            
    # 2. Extraer Municipio y Lluvia de Geopandas
    municipio_str = "Desconocido"
    lluvia = 2000.0
    if gdf_municipios is not None:
        try:
            pt = Point(lon, lat)
            mask = gdf_municipios.contains(pt)
            if mask.any():
                match = gdf_municipios[mask].iloc[0]
                muni_name = match.get('NOMBREMUNICIPIO_CG', 'Desconocido')
                municipio_str = str(muni_name).title()
                
                muni_norm = normalize_text(muni_name)
                if muni_norm in precip_dict:
                    lluvia = float(precip_dict[muni_norm])
                else:
                    if precip_dict: lluvia = float(np.mean(list(precip_dict.values())))
        except Exception:
            pass
            
    return municipio_str, altitud, pendiente, lluvia
