import os
import requests
import json
import pandas as pd
from pathlib import Path
from tqdm import tqdm
import time

# Configuración
BASE_DIR = Path(__file__).resolve().parent.parent.parent
RAW_DIR = BASE_DIR / 'data' / 'raw'
PROCESSED_DIR = BASE_DIR / 'data' / 'processed'
REPORTS_DIR = BASE_DIR / 'data' / 'reports'

RAW_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

# URL del FeatureServer del MMRA 2025 (Capa 1: Conglomerados)
URL_MMRA = "https://geoportal.dane.gov.co/mparcgis/rest/services/MMRA2025/Serv_CapasMMRA_2025/FeatureServer/1/query"

def download_mmra_valle():
    """Descarga los conglomerados del MMRA para el Valle del Cauca."""
    print("="*60)
    print("  DESCARGA DEL MARCO MAESTRO RURAL AGROPECUARIO (MMRA)")
    print("  Departamento: Valle del Cauca (Código 76)")
    print("="*60)

    # 1. Obtener los IDs (OBJECTID) para el departamento 76
    ids_params = {
        'where': "COD_DEPTO='76'",
        'returnIdsOnly': 'true',
        'f': 'json'
    }
    
    try:
        res_ids = requests.get(URL_MMRA, params=ids_params, timeout=30).json()
        object_ids = res_ids.get('objectIds', [])
        total_records = len(object_ids)
        print(f"[INFO] Total de conglomerados a descargar: {total_records}")
    except Exception as e:
        print(f"[ERROR] No se pudieron obtener los IDs: {e}")
        return
        
    if total_records == 0:
        print("[ERROR] No hay registros para el departamento 76 en el MMRA.")
        return

    # 2. Descargar por lotes de IDs (ya que el servidor no soporta resultOffset)
    chunk_size = 500  # Lote más conservador para URLs largas
    all_features = []
    
    print("[INFO] Iniciando descarga por lotes de OBJECTID...")
    for i in range(0, total_records, chunk_size):
        chunk_ids = object_ids[i:i + chunk_size]
        ids_str = ",".join(map(str, chunk_ids))
        print(f"       -> Descargando lote {i} a {min(i + chunk_size, total_records)}...")
        
        # OJO: Se pasa por POST si la lista es muy larga
        data_params = {
            'where': f"OBJECTID IN ({ids_str})",
            'outFields': '*',
            'outSR': '4326',
            'f': 'geojson'
        }
        
        success = False
        for attempt in range(3):
            try:
                # Usar POST porque el query con IN puede ser un string largo
                response = requests.post(URL_MMRA, data=data_params, timeout=60)
                response.raise_for_status()
                data = response.json()
                
                # Manejar errores del API
                if 'error' in data:
                    print(f"          [ERROR API] {data['error']}")
                    time.sleep(2)
                    continue
                    
                features = data.get('features', [])
                if features:
                    all_features.extend(features)
                    success = True
                    break
            except Exception as e:
                print(f"          [ADVERTENCIA] Intento {attempt+1} falló: {e}")
                time.sleep(2)
                
        if not success:
            print(f"[ERROR] Falló la descarga del lote de IDs {i}.")
            return
            
    print(f"\n[INFO] Descarga completada. Total características: {len(all_features)}")
    
    # 3. Guardar el GeoJSON resultante
    output_geojson = RAW_DIR / 'mmra_conglomerados_valle.geojson'
    feature_collection = {
        "type": "FeatureCollection",
        "name": "MMRA_Valle_del_Cauca",
        "crs": { "type": "name", "properties": { "name": "urn:ogc:def:crs:OGC:1.3:CRS84" } },
        "features": all_features
    }
    
    with open(output_geojson, 'w', encoding='utf-8') as f:
        json.dump(feature_collection, f)
        
    print(f"[ÉXITO] Archivo GeoJSON guardado en: {output_geojson}")
    
    # 4. Generar tabla procesada para reportes rápidos (sin geometría)
    print("\n[INFO] Generando tabla resumen procesada...")
    records = [f['properties'] for f in all_features]
    df = pd.DataFrame(records)
    
    csv_file = PROCESSED_DIR / 'mmra_conglomerados_valle_tabular.csv'
    df.to_csv(csv_file, index=False)
    print(f"[ÉXITO] Tabla guardada en: {csv_file}")
    
    # 5. Generar reporte
    report_file = REPORTS_DIR / '21_mmra_exploration.md'
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("# 🗺️ Exploración del MMRA - Valle del Cauca\n\n")
        f.write(f"**Total de Conglomerados Rurales**: {len(df):,}\n\n")
        f.write("## Municipios Incluidos\n")
        munis = df['NOMBREMUNICIPIO_CG'].value_counts()
        f.write("El MMRA cubre zonas rurales, por lo que aquí están los conglomerados por municipio:\n\n")
        f.write(munis.to_frame().to_markdown())
        f.write("\n\n## Vocación Agropecuaria Predominante\n")
        usos = df['USO_PRED_CONGL'].value_counts()
        f.write(usos.to_frame().to_markdown())
        
    print(f"[ÉXITO] Reporte generado en: {report_file}")

if __name__ == "__main__":
    download_mmra_valle()
