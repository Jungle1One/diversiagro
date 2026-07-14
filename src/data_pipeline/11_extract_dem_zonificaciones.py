import rasterio
import pandas as pd
import geopandas as gpd
from pathlib import Path
import glob

# Configuración de rutas
BASE_DIR = Path(__file__).resolve().parent.parent.parent
PROCESSED_DIR = BASE_DIR / 'data' / 'processed'
RUTA_DEM = PROCESSED_DIR / 'DEM_Valle_Cauca_Elevacion_y_Pendiente.tif'

def extract_dem_for_zonificaciones():
    print("="*60)
    print("🏔️ EXTRACCIÓN DE ELEVACIÓN Y PENDIENTE PARA ZONIFICACIONES")
    print("="*60)
    
    if not RUTA_DEM.exists():
        print(f"❌ No se encontró el archivo DEM en: {RUTA_DEM}")
        return
        
    # Buscar todos los archivos de zonificación procesados
    archivos_zonificacion = glob.glob(str(PROCESSED_DIR / 'zonificacion_*_valle_limpio.geojson'))
    
    if not archivos_zonificacion:
        print("❌ No se encontraron archivos de zonificación (.geojson).")
        return
        
    print(f"Abriendo el modelo de elevación (DEM): {RUTA_DEM.name}")
    with rasterio.open(RUTA_DEM) as src:
        crs_dem = src.crs
        print(f"CRS del DEM: {crs_dem}")
        
        for archivo in archivos_zonificacion:
            nombre_cultivo = Path(archivo).name.split('zonificacion_')[-1].split('_valle')[0].replace('_', ' ').title()
            print(f"\n▶️ Procesando: {nombre_cultivo} ({Path(archivo).name})")
            
            # 1. Cargar datos espaciales de la zonificación
            gdf = gpd.read_file(archivo)
            
            # Asegurarnos de que el CRS coincide con el del DEM para que las coordenadas crucen bien
            if gdf.crs != crs_dem:
                print(f"   Reproyectando datos de {gdf.crs} a {crs_dem}...")
                gdf = gdf.to_crs(crs_dem)
                
            # 2. Extraer las coordenadas de los polígonos (usamos el centroide)
            # Como la zonificación tiene multipolígonos, extraemos sus centros
            print("   Calculando centroides...")
            coordenadas = [(geom.centroid.x, geom.centroid.y) for geom in gdf.geometry]
            
            # 3. Extraer los valores para cada punto desde el raster
            print("   Extrayendo pixeles del DEM...")
            elevaciones = []
            pendientes = []
            
            # src.sample devuelve un generador que iteramos
            for valores_pixel in src.sample(coordenadas):
                elevaciones.append(valores_pixel[0]) # Banda 1: Elevación
                
                # Verificamos si hay una segunda banda (Pendiente)
                if len(valores_pixel) > 1:
                    pendientes.append(valores_pixel[1]) 
                else:
                    pendientes.append(None)
                    
            # 4. Añadir las nuevas columnas al GeoDataFrame
            gdf['altitud_msnm'] = elevaciones
            if any(p is not None for p in pendientes):
                gdf['pendiente_grados'] = pendientes
                
            # Limpiar valores anómalos o "NoData" típicos de DEMs (ej. valores en el mar o bordes)
            gdf.loc[gdf['altitud_msnm'] < -50, 'altitud_msnm'] = None
            if 'pendiente_grados' in gdf.columns:
                gdf.loc[gdf['pendiente_grados'] < 0, 'pendiente_grados'] = None
            
            # 5. Guardar el resultado en un nuevo GeoJSON enriquecido
            output_file = PROCESSED_DIR / f'zonificacion_{nombre_cultivo.lower().replace(" ", "_")}_valle_con_dem.geojson'
            print(f"   Guardando datos enriquecidos: {output_file.name}")
            
            # Reproyectamos a EPSG:4326 estándar para compatibilidad global antes de guardar
            if gdf.crs != "EPSG:4326":
                gdf = gdf.to_crs("EPSG:4326")
                
            gdf.to_file(output_file, driver='GeoJSON')
            print(f"✅ Completado {nombre_cultivo}. Polígonos enriquecidos: {len(gdf)}")

if __name__ == "__main__":
    extract_dem_for_zonificaciones()
