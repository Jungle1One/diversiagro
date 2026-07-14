# -*- coding: utf-8 -*-
"""
==============================================================================
  SCRIPT 10: Descarga y procesamiento de Información Catastral Predial
  Fuentes: Gestor Catastral Departamento del Valle del Cauca (Socrata)
  - Tabular: uu6s-r6u3 (Información catastral)
  - Espacial: ttbg-34sn (Información Cartográfica Catastral a Nivel Terreno)
  Alcance: Valle del Cauca
  Tarea: T-006 (Actualizada a nivel predial)
==============================================================================

Este script reemplaza la descarga de límites municipales generales 
por la descarga a nivel de predios y su clasificación económica, 
permitiendo cruces espaciales mucho más finos con la zonificación agrícola.
"""

import os
import sys
import time
import requests
import pandas as pd
from pathlib import Path
from datetime import datetime

# Configurar encoding para Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# ============================================================================
# CONFIGURACION
# ============================================================================
BASE_DIR = Path(__file__).resolve().parent.parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
REPORTS_DIR = BASE_DIR / "data" / "reports"

for d in [RAW_DIR, PROCESSED_DIR, REPORTS_DIR]:
    d.mkdir(parents=True, exist_ok=True)

APP_TOKEN = "FbcYAmAYgsBJmr4HRkPhngV6X"

TABULAR_DATASET = "uu6s-r6u3"
SPATIAL_DATASET = "ttbg-34sn"

# ============================================================================
# FUNCIONES
# ============================================================================

def download_socrata_dataset(dataset_id, output_file, is_spatial=False):
    """
    Descarga iterativamente un dataset de Socrata en formato CSV (incluye WKT para geometrías).
    """
    print("\n" + "=" * 70)
    print(f"  Descargando dataset: {dataset_id}")
    print("=" * 70)
    
    if output_file.exists():
        print(f"[INFO] El archivo ya existe localmente: {output_file.name}")
        print("[INFO] Saltando descarga. Elimina el archivo si deseas forzar la actualización.")
        return
        
    api_url = f"https://www.datos.gov.co/resource/{dataset_id}.csv"
    headers = {"X-App-Token": APP_TOKEN}
    
    batch_size = 50000
    offset = 0
    all_chunks = []
    
    print(f"[INFO] Iniciando descarga paginada (Lotes de {batch_size})...")
    
    while True:
        params = {
            "$limit": batch_size,
            "$offset": offset,
            "$order": "codigo" if is_spatial else "numero_predial_nacional"
        }
        
        # El order by previene problemas de paginación si se actualiza el dataset mientras se descarga,
        # pero requiere que sepamos la columna. Haremos el order dinámico o no usaremos order.
        if is_spatial:
            params["$order"] = "objectid"
        else:
            params["$order"] = "numero_predial_nacional"
            
        try:
            print(f"  -> Consultando registros {offset} a {offset + batch_size}...")
            response = requests.get(api_url, headers=headers, params=params, timeout=120)
            
            # Si Socrata se queja del $order, reintentamos sin él
            if response.status_code == 400 and 'order' in response.text.lower():
                del params["$order"]
                response = requests.get(api_url, headers=headers, params=params, timeout=120)
                
            response.raise_for_status()
            
            import io
            chunk_df = pd.read_csv(io.StringIO(response.text), low_memory=False)
            
            if chunk_df.empty:
                break
                
            all_chunks.append(chunk_df)
            print(f"     Recibidos {len(chunk_df)} registros.")
            
            if len(chunk_df) < batch_size:
                break
                
            offset += batch_size
            time.sleep(1) # rate limiting
            
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Falló la petición HTTP: {e}")
            break
        except Exception as e:
            print(f"[ERROR] Error inesperado procesando el chunk: {e}")
            break
            
    if all_chunks:
        print("[INFO] Combinando lotes...")
        final_df = pd.concat(all_chunks, ignore_index=True)
        print(f"[INFO] Guardando {len(final_df)} registros totales a disco (puede tardar)...")
        final_df.to_csv(output_file, index=False, encoding='utf-8-sig')
        print(f"[OK] Archivo RAW guardado: {output_file}")
    else:
        print(f"[WARN] No se logró descargar ningún registro de {dataset_id}")


def process_catastro_data():
    tabular_file = RAW_DIR / "catastro_tabular_valle_raw.csv"
    spatial_file = RAW_DIR / "catastro_espacial_valle_raw.csv"
    
    # 1. Descargar ambos datasets
    download_socrata_dataset(TABULAR_DATASET, tabular_file, is_spatial=False)
    download_socrata_dataset(SPATIAL_DATASET, spatial_file, is_spatial=True)
    
    if not tabular_file.exists() or not spatial_file.exists():
        print("[ERROR] No se pueden procesar los datos porque faltan los archivos RAW.")
        return
        
    print("\n" + "=" * 70)
    print("  Procesamiento y Cruce de Datos (Espacial + Tabular)")
    print("=" * 70)
    
    # 2. Cargar en Pandas
    print("[INFO] Leyendo archivo tabular...")
    df_tab = pd.read_csv(tabular_file, low_memory=False)
    
    print("[INFO] Leyendo archivo espacial (WKT)...")
    df_sp = pd.read_csv(spatial_file, low_memory=False)
    
    # 3. Limpiar claves primarias para cruce
    print("[INFO] Reconstruyendo NPN de 30 dígitos para el cruce...")
    
    if 'codigo' in df_sp.columns:
        df_sp['codigo_clean'] = df_sp['codigo'].astype(str).str.strip().str.zfill(30)
    else:
        print("[ERROR] No se encontró la columna 'codigo' en los datos espaciales.")
        return
        
    required_tab = ['codigo_departamento', 'codigo_municipio', 'numero_predial_nacional']
    if all(c in df_tab.columns for c in required_tab):
        df_tab['npn_clean'] = (
            df_tab['codigo_departamento'].astype(str).str.strip().str.zfill(2) +
            df_tab['codigo_municipio'].astype(str).str.strip().str.zfill(3) +
            df_tab['numero_predial_nacional'].astype(str).str.strip().str.zfill(25)
        )
    else:
        print(f"[ERROR] Faltan columnas en los datos tabulares. Requeridas: {required_tab}")
        return
        
    # Eliminar duplicados espaciales si los hay
    df_sp = df_sp.drop_duplicates(subset=['codigo_clean'])
    
    # Eliminar duplicados tabulares, nos quedamos con el último
    df_tab = df_tab.drop_duplicates(subset=['npn_clean'], keep='last')
    
    # 4. Hacer Merge (Left Join: Mantenemos todos los predios espaciales y les pegamos atributos)
    print(f"[INFO] Cruzando {len(df_sp)} predios espaciales con atributos de {len(df_tab)} registros tabulares...")
    
    df_merged = pd.merge(
        df_sp, 
        df_tab, 
        left_on='codigo_clean', 
        right_on='npn_clean', 
        how='left'
    )
    
    # Eliminar columnas redundantes
    cols_to_drop = ['codigo_clean', 'npn_clean', 'numero_predial_nacional']
    df_merged = df_merged.drop(columns=[c for c in cols_to_drop if c in df_merged.columns])
    
    # 5. Guardar CSV procesado
    output_csv = PROCESSED_DIR / "catastro_predial_valle_procesado.csv"
    print(f"[INFO] Guardando CSV procesado con geometría WKT (puede tardar)...")
    df_merged.to_csv(output_csv, index=False, encoding='utf-8-sig')
    print(f"[OK] Archivo guardado: {output_csv}")
    
    # Opcional: Generar Geopackage si geopandas está disponible
    try:
        import geopandas as gpd
        from shapely import wkt
        
        print("\n[INFO] GeoPandas detectado. Generando Geopackage optimizado...")
        # Tomar solo los que tienen geometría
        df_geo = df_merged.dropna(subset=['the_geom']).copy()
        
        print("[INFO] Convirtiendo texto WKT a geometrías Shapely...")
        # Esto puede ser lento para 360k registros
        df_geo['geometry'] = df_geo['the_geom'].apply(lambda x: wkt.loads(x) if pd.notnull(x) else None)
        df_geo = df_geo.drop(columns=['the_geom'])
        
        gdf = gpd.GeoDataFrame(df_geo, geometry='geometry')
        gdf.set_crs(epsg=4326, inplace=True)
        
        output_gpkg = PROCESSED_DIR / "catastro_predial_valle.gpkg"
        print(f"[INFO] Escribiendo GeoPackage: {output_gpkg}")
        gdf.to_file(output_gpkg, driver="GPKG")
        print(f"[OK] GeoPackage guardado correctamente.")
        
    except ImportError:
        print("\n[INFO] (Opcional) GeoPandas no instalado. Se omitió la creación del archivo GeoPackage.")
        print("       Puedes abrir el CSV procesado en QGIS directamente usando 'the_geom' como campo WKT.")
        print("       Para instalar geopandas: pip install geopandas")
    except Exception as e:
        print(f"\n[WARN] Hubo un problema al crear el Geopackage: {e}")
        
    # 6. Reporte
    generate_report(df_sp, df_tab, df_merged)


def generate_report(df_sp, df_tab, df_merged):
    print("\n[INFO] Generando reporte de exploración...")
    
    report_file = REPORTS_DIR / "20_catastro_predial_exploration.md"
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("# Reporte de Exploración: Catastro Predial Valle del Cauca\n\n")
        f.write(f"**Fecha de generación**: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        f.write("**Fuentes**: Gestor Catastral Valle del Cauca (Socrata `uu6s-r6u3` y `ttbg-34sn`)\n\n")
        
        f.write("## 1. Resumen de Cruce de Datos\n\n")
        f.write(f"- **Predios Espaciales Totales**: {len(df_sp):,}\n")
        f.write(f"- **Registros Tabulares Totales**: {len(df_tab):,}\n")
        
        match_count = df_merged['destinacion_economica'].notna().sum()
        match_pct = (match_count / len(df_merged)) * 100
        f.write(f"- **Predios con atributos cruzados con éxito**: {match_count:,} ({match_pct:.1f}%)\n\n")
        
        f.write("## 2. Destinación Económica de Predios\n\n")
        f.write("La siguiente tabla muestra cómo están clasificados los predios en el Valle del Cauca (útil para descartar áreas urbanas y enfocarse en rurales/agrícolas).\n\n")
        
        f.write("| Código Destinación | Descripción Común | Cantidad de Predios |\n")
        f.write("|-------------------|------------------|----------------------|\n")
        
        if 'destinacion_economica' in df_merged.columns:
            counts = df_merged['destinacion_economica'].value_counts()
            for cat, count in counts.items():
                f.write(f"| {cat} | (Ver Diccionario Catastral) | {count:,} |\n")
        else:
            f.write("| N/A | No se encontró columna destinacion_economica | 0 |\n")
            
        f.write("\n## 3. Cobertura por Municipio\n\n")
        f.write("Distribución de predios según municipio (código):\n\n")
        
        f.write("| Código Municipio | Cantidad Predios |\n")
        f.write("|------------------|------------------|\n")
        if 'cod_muni' in df_merged.columns:
            mun_counts = df_merged['cod_muni'].value_counts().head(20)
            for mun, count in mun_counts.items():
                f.write(f"| {mun} | {count:,} |\n")
            f.write(f"| ... | (Mostrando Top 20) |\n")
            
    print(f"[OK] Reporte guardado en: {report_file}")
    
    # Actualizar README
    readme_file = BASE_DIR / "scripts" / "README_ejecucion.md"
    if readme_file.exists():
        with open(readme_file, 'a', encoding='utf-8') as f:
            f.write("\n\n### Script 10: Catastro Predial\n")
            f.write("El script `10_download_limites_admin.py` ahora descarga predios y atributos catastrales para realizar cruces con zonificación.\n")
            f.write("- **Nota**: La descarga toma tiempo por el alto volumen de datos (cientos de miles de predios).\n")

# ============================================================================
# MAIN
# ============================================================================
if __name__ == "__main__":
    process_catastro_data()
    print("\n[OK] Proceso catastral finalizado exitosamente.")
