import pandas as pd
import geopandas as gpd
from pathlib import Path
import unicodedata

BASE_DIR = Path(__file__).resolve().parent.parent.parent
PROCESSED_DIR = BASE_DIR / 'data' / 'processed'

# Cultivos seleccionados para la Fase 2
CULTIVOS = ['cafe', 'cacao', 'aguacate', 'cana_panelera', 'fresa']

def clean_municipio_name(name):
    if pd.isna(name): return ""
    name = str(name).strip().upper()
    # Remover tildes
    name = ''.join(c for c in unicodedata.normalize('NFD', name) if unicodedata.category(c) != 'Mn')
    return name

def main():
    print("Iniciando Consolidación de Datos para Machine Learning...")
    
    # 1. Cargar Precipitación IDEAM
    precip_file = PROCESSED_DIR / 'ideam_precipitacion_anual_municipio.csv'
    if not precip_file.exists():
        print(f"Error: No se encontró el archivo de precipitación en {precip_file}")
        return
        
    df_precip = pd.read_csv(precip_file)
    # Sanitizar outliers de lluvia (ej. Buenaventura a 283,846 mm) y valores demasiado bajos antes de mapear o promediar
    # El rango natural del Valle del Cauca está entre 500 mm y 8000 mm
    df_precip['precipitacion_anual_mm'] = df_precip['precipitacion_anual_mm'].clip(lower=500.0, upper=8000.0)
    
    # Limpiar nombres para el merge
    df_precip['municipio_clean'] = df_precip['municipio'].apply(clean_municipio_name)
    
    # Crear diccionario de lluvia por municipio
    dict_lluvia = dict(zip(df_precip['municipio_clean'], df_precip['precipitacion_anual_mm']))
    
    for cultivo in CULTIVOS:
        print(f"\nProcesando cultivo: {cultivo.upper()}...")
        geojson_file = PROCESSED_DIR / f'zonificacion_{cultivo}_valle_con_dem.geojson'
        
        if not geojson_file.exists():
            print(f"⚠️ Archivo no encontrado: {geojson_file}. Saltando...")
            continue
            
        print("  Cargando mapa (esto puede tardar unos segundos)...")
        gdf = gpd.read_file(geojson_file)
        
        # 2. Extraer coordenadas X, Y (Centros de los polígonos) para el Kriging
        # Para evitar el UserWarning de operar en grados, reproyectamos a un CRS plano (colombia nacional EPSG:9377),
        # calculamos centroides en metros, y los reproyectamos de vuelta a coordenadas geográficas EPSG:4326.
        print("  Calculando coordenadas geográficas (X, Y) para Kriging (usando proyección métrica)...")
        gdf_projected = gdf.to_crs(epsg=9377)
        centroides_projected = gdf_projected.geometry.centroid
        centroides = gpd.GeoSeries(centroides_projected, crs=9377).to_crs(epsg=4326)
        gdf['lon_x'] = centroides.x
        gdf['lat_y'] = centroides.y
        
        # 3. Limpiar y Cruce de Lluvia
        print("  Cruzando con datos climáticos del IDEAM...")
        gdf['municipio_clean'] = gdf['municipio'].apply(clean_municipio_name)
        gdf['precipitacion_anual_mm'] = gdf['municipio_clean'].map(dict_lluvia)
        
        # Llenar nulos (si un municipio no cruzó, usar la media del departamento ya sanitizada)
        lluvia_media = df_precip['precipitacion_anual_mm'].mean()
        faltantes = gdf['precipitacion_anual_mm'].isna().sum()
        if faltantes > 0:
            print(f"  Aviso: {faltantes} polígonos sin datos de lluvia directa. Usando media departamental ({lluvia_media:.1f} mm).")
            gdf['precipitacion_anual_mm'] = gdf['precipitacion_anual_mm'].fillna(lluvia_media)
            
        # 4. Seleccionar sólo las variables (Features & Targets) para descartar la geometría pesada
        # Variables predictoras (X): altitud_msnm, pendiente_grados, precipitacion_anual_mm, lon_x, lat_y
        # Variable Objetivo (Y): aptitud
        columnas_ml = [
            'municipio', 'aptitud', 'altitud_msnm', 'pendiente_grados', 
            'precipitacion_anual_mm', 'lon_x', 'lat_y', 'area_ha'
        ]
        
        df_ml = pd.DataFrame(gdf[columnas_ml])
        
        # Limpieza final (eliminar polígonos que cayeron en el mar o no tienen altitud)
        df_ml = df_ml.dropna(subset=['altitud_msnm', 'pendiente_grados', 'aptitud'])
        
        # 5. Guardar el CSV consolidado y ligero
        out_file = PROCESSED_DIR / f'dataset_ml_{cultivo}.csv'
        df_ml.to_csv(out_file, index=False)
        print(f"EXITO: Dataset guardado exitosamente! ({len(df_ml):,} registros) -> {out_file.name}")
        
    print("\n¡Consolidacion finalizada! Listos para entrenar en Fase 2.")

if __name__ == "__main__":
    main()
