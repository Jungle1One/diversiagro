"""
=============================================================================
Dataset 4: Zonificación de aptitud para el cultivo comercial de cacao
Fuente: UPRA via datos.gov.co (Socrata API)
ID: jdjx-qer4
Total registros en origen: ~169,266 polígonos
Valle del Cauca: ~5,176 polígonos
=============================================================================

Este script:
1. Descarga datos de zonificación de cacao para Valle del Cauca
2. Explora la estructura y distribución de aptitudes
3. Agrega por municipio: % de área por categoría de aptitud
4. Genera CSVs procesados para modelado

Columnas del dataset:
- the_geom: Geometría multipolygon (excluida de descarga tabular)
- municipio: Nombre del municipio
- departamen: Nombre del departamento
- cod_depart: Código DANE departamento
- cod_dane_m: Código DANE municipio
- gridcode: Valor representativo del pixel (0,1,2,3,8)
- area_ha: Área en hectáreas del polígono
- aptitud: Clasificación (Alta, Media, Baja, No apta, Exclusión legal)
- consecutiv: ID único

Mapeo gridcode -> aptitud:
  0 = No apta
  1 = Aptitud baja
  2 = Aptitud media
  3 = Aptitud alta
  8 = Exclusión legal
"""

import requests
import pandas as pd
import numpy as np
import os
import json
from datetime import datetime

# =============================================================================
# CONFIGURACIÓN
# =============================================================================
BASE_URL = "https://www.datos.gov.co/api/v3/views/jdjx-qer4/query.json"
APP_TOKEN = "FbcYAmAYgsBJmr4HRkPhngV6X"

# Directorio de salida
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_RAW_DIR = os.path.join(PROJECT_DIR, "data", "raw")
DATA_PROCESSED_DIR = os.path.join(PROJECT_DIR, "data", "processed")
DATA_REPORTS_DIR = os.path.join(PROJECT_DIR, "data", "reports")

os.makedirs(DATA_RAW_DIR, exist_ok=True)
os.makedirs(DATA_PROCESSED_DIR, exist_ok=True)
os.makedirs(DATA_REPORTS_DIR, exist_ok=True)

DEPARTAMENTO_INTERES = "Valle del Cauca"
CODIGO_DEPTO = "76"

# =============================================================================
# FUNCIONES
# =============================================================================

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")


def download_data():
    """
    Descarga datos de zonificación de cacao para Valle del Cauca.
    Usa API v3 con POST y paginación.
    """
    log("=" * 60)
    log("PASO 1: DESCARGA DE DATOS DE ZONIFICACIÓN DE CACAO")
    log(f"  Departamento: {DEPARTAMENTO_INTERES}")
    log("=" * 60)
    
    all_records = []
    page_number = 1
    page_size = 50000
    
    headers = {"X-App-Token": APP_TOKEN}
    
    while True:
        payload = {
            "query": f"SELECT the_geom, municipio, departamen, cod_depart, cod_dane_m, gridcode, area_ha, aptitud, consecutiv WHERE cod_depart='{CODIGO_DEPTO}'",
            "page": {
                "pageNumber": page_number,
                "pageSize": page_size
            }
        }
        
        log(f"  Descargando página {page_number}...")
        
        try:
            response = requests.post(BASE_URL, headers=headers, json=payload, timeout=120)
        except requests.exceptions.Timeout:
            log(f"  ⚠️ Timeout, reintentando...")
            try:
                response = requests.post(BASE_URL, headers=headers, json=payload, timeout=180)
            except requests.exceptions.Timeout:
                log(f"  ❌ Timeout persistente. Guardando {len(all_records):,} registros.")
                break
        
        if response.status_code != 200:
            log(f"  ❌ Error HTTP {response.status_code}: {response.text[:300]}")
            break
        
        data = response.json()
        
        # Extraer registros de la respuesta v3
        if isinstance(data, list):
            batch = data
        elif isinstance(data, dict):
            batch = data.get("data", data.get("rows", data.get("results", [])))
            # Si la respuesta tiene columnas + filas (formato v3)
            if "columns" in data and "rows" in data:
                columns = [col.get("fieldName", col.get("name", f"col_{i}")) for i, col in enumerate(data["columns"])]
                batch = [dict(zip(columns, row)) for row in data["rows"]]
            elif not batch and isinstance(data, dict):
                # Intentar interpretar como respuesta directa
                batch = []
        else:
            batch = []
        
        if not batch:
            log(f"  ✅ Descarga completa. Total: {len(all_records):,} registros")
            break
        
        all_records.extend(batch)
        log(f"  ✅ Página {page_number}: {len(batch):,} registros | Acumulado: {len(all_records):,}")
        page_number += 1
        
        # Si el lote fue menor que page_size, ya no hay más datos
        if len(batch) < page_size:
            log(f"  ✅ Último lote recibido. Total: {len(all_records):,} registros")
            break
    
    # Guardar datos crudos
    df_raw = pd.DataFrame(all_records)
    raw_file = os.path.join(DATA_RAW_DIR, "zonificacion_cacao_valle_raw.csv")
    df_raw.to_csv(raw_file, index=False, encoding="utf-8-sig")
    log(f"  💾 Datos crudos guardados: {raw_file}")
    log(f"  📊 Shape: {df_raw.shape}")
    log(f"  📋 Columnas: {df_raw.columns.tolist()}")
    
    return df_raw


def explore_data(df):
    """Exploración inicial del dataset de zonificación."""
    log("")
    log("=" * 60)
    log("PASO 2: EXPLORACIÓN")
    log("=" * 60)
    
    report = []
    report.append("# Reporte de Exploración – Zonificación de Cacao (UPRA)")
    report.append(f"\nFecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"\n## Información General")
    report.append(f"- **Fuente**: UPRA – datos.gov.co (ID: jdjx-qer4)")
    report.append(f"- **Departamento**: {DEPARTAMENTO_INTERES}")
    report.append(f"- **Total registros (polígonos)**: {len(df):,}")
    report.append(f"- **Columnas**: {', '.join(df.columns.tolist())}")
    
    # Distribución de aptitud
    report.append(f"\n## Distribución de Aptitud")
    if "aptitud" in df.columns:
        apt_counts = df["aptitud"].value_counts()
        report.append(f"| Aptitud | Polígonos | % |")
        report.append(f"|---------|-----------|---|")
        for apt, count in apt_counts.items():
            pct = (count / len(df)) * 100
            report.append(f"| {apt} | {count:,} | {pct:.1f}% |")
    
    # Área por aptitud
    if "area_ha" in df.columns:
        df["area_ha"] = pd.to_numeric(df["area_ha"], errors="coerce")
        report.append(f"\n## Área Total por Aptitud")
        area_apt = df.groupby("aptitud")["area_ha"].sum().sort_values(ascending=False)
        area_total = area_apt.sum()
        report.append(f"| Aptitud | Área (Ha) | % del total |")
        report.append(f"|---------|-----------|-------------|")
        for apt, area in area_apt.items():
            pct = (area / area_total) * 100
            report.append(f"| {apt} | {area:,.2f} | {pct:.1f}% |")
        report.append(f"| **TOTAL** | **{area_total:,.2f}** | **100%** |")
    
    # Municipios
    if "municipio" in df.columns:
        report.append(f"\n## Municipios")
        report.append(f"- **Total**: {df['municipio'].nunique()}")
        report.append(f"\n### Distribución por Municipio")
        muni_area = df.groupby("municipio")["area_ha"].sum().sort_values(ascending=False)
        report.append(f"| Municipio | Área total (Ha) | Polígonos |")
        report.append(f"|-----------|----------------|-----------|")
        for muni in muni_area.index:
            area = muni_area[muni]
            n = len(df[df["municipio"] == muni])
            report.append(f"| {muni} | {area:,.2f} | {n:,} |")
    
    # Guardar reporte
    report_text = "\n".join(report)
    report_file = os.path.join(DATA_REPORTS_DIR, "07_cacao_zonificacion_exploration.md")
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(report_text)
    
    log(f"  📄 Reporte guardado: {report_file}")
    print("\n" + report_text[:3000])
    
    return df


def clean_and_aggregate(df):
    """
    Limpia y agrega los datos de zonificación:
    1. Normaliza nombres
    2. Calcula % de área por aptitud para cada municipio
    3. Genera tabla resumen municipal (una fila por municipio)
    """
    log("")
    log("=" * 60)
    log("PASO 3: LIMPIEZA Y AGREGACIÓN")
    log("=" * 60)
    
    # --- 3.1 Renombrar columnas ---
    log("  3.1 Renombrando columnas...")
    rename_map = {
        "departamen": "departamento",
        "cod_depart": "codigo_departamento",
        "cod_dane_m": "codigo_municipio",
        "area_ha": "area_ha",
        "consecutiv": "consecutivo",
    }
    df = df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns})
    
    # --- 3.2 Convertir tipos ---
    log("  3.2 Convirtiendo tipos...")
    if "area_ha" in df.columns:
        df["area_ha"] = pd.to_numeric(df["area_ha"], errors="coerce")
    if "gridcode" in df.columns:
        df["gridcode"] = pd.to_numeric(df["gridcode"], errors="coerce")
    
    # --- 3.3 Validar aptitudes ---
    log("  3.3 Validando categorías de aptitud...")
    aptitudes_validas = ["Aptitud alta", "Aptitud media", "Aptitud baja", "No apta", "Exclusión legal"]
    if "aptitud" in df.columns:
        invalidos = df[~df["aptitud"].isin(aptitudes_validas)]
        if len(invalidos) > 0:
            log(f"      ⚠️ {len(invalidos)} registros con aptitud no reconocida")
            df = df[df["aptitud"].isin(aptitudes_validas)]
    
    # --- 3.4 Eliminar áreas 0 o negativas ---
    log("  3.4 Filtrando áreas inválidas...")
    antes = len(df)
    df = df[df["area_ha"] > 0]
    log(f"      Eliminados: {antes - len(df)} registros con área <= 0")
    
    # --- 3.5 Convertir geometrías y guardar GeoJSON limpio ---
    log("  3.5 Construyendo capa geoespacial (GeoJSON)...")
    if "the_geom" in df.columns:
        try:
            import geopandas as gpd
            from shapely.geometry import shape
            
            # Convertir los diccionarios o strings JSON a objetos de geometría
            def parse_geom(g):
                if pd.isna(g): return None
                if isinstance(g, str): 
                    try:
                        g = json.loads(g)
                    except:
                        return None
                if isinstance(g, dict):
                    return shape(g)
                return None
                
            df["geometry"] = df["the_geom"].apply(parse_geom)
            df = df.drop(columns=["the_geom"])
            
            gdf = gpd.GeoDataFrame(df, geometry="geometry", crs="EPSG:4326")
            clean_file = os.path.join(DATA_PROCESSED_DIR, "zonificacion_cacao_valle_limpio.geojson")
            
            if os.path.exists(clean_file):
                os.remove(clean_file)
                
            gdf.to_file(clean_file, driver="GeoJSON")
            log(f"  💾 Dataset limpio (Geoespacial): {clean_file} ({len(gdf):,} polígonos)")
        except Exception as e:
            log(f"  ❌ Error creando GeoJSON: {e}")
            clean_file = os.path.join(DATA_PROCESSED_DIR, "zonificacion_cacao_valle_limpio.csv")
            df.to_csv(clean_file, index=False, encoding="utf-8-sig")
            log(f"  💾 Dataset limpio guardado como CSV (respaldo): {clean_file}")
    else:
        clean_file = os.path.join(DATA_PROCESSED_DIR, "zonificacion_cacao_valle_limpio.csv")
        df.to_csv(clean_file, index=False, encoding="utf-8-sig")
        log(f"  💾 Dataset limpio guardado: {clean_file}")
    log("  3.6 Agregando por municipio...")
    
    # Área total por municipio y aptitud
    area_pivot = df.pivot_table(
        index=["codigo_municipio", "municipio"],
        columns="aptitud",
        values="area_ha",
        aggfunc="sum",
        fill_value=0
    ).reset_index()
    
    # Calcular área total y porcentajes
    apt_cols = [c for c in area_pivot.columns if c in aptitudes_validas]
    area_pivot["area_total_ha"] = area_pivot[apt_cols].sum(axis=1)
    
    for col in apt_cols:
        pct_col = f"pct_{col.lower().replace(' ', '_').replace('ó', 'o')}"
        area_pivot[pct_col] = (area_pivot[col] / area_pivot["area_total_ha"] * 100).round(2)
    
    # Renombrar columnas de área
    rename_apt = {}
    for col in apt_cols:
        safe_name = f"area_{col.lower().replace(' ', '_').replace('ó', 'o')}_ha"
        rename_apt[col] = safe_name
    area_pivot = area_pivot.rename(columns=rename_apt)
    
    # Calcular aptitud dominante
    area_cols = [v for v in rename_apt.values()]
    area_pivot["aptitud_dominante"] = area_pivot[area_cols].idxmax(axis=1).str.replace("area_", "").str.replace("_ha", "").str.replace("_", " ").str.title()
    
    # Calcular índice de aptitud (ponderado: alta=3, media=2, baja=1, no_apta=0, exclusion=0)
    pesos = {"area_aptitud_alta_ha": 3, "area_aptitud_media_ha": 2, "area_aptitud_baja_ha": 1, 
             "area_no_apta_ha": 0, "area_exclusion_legal_ha": 0}
    numerador = sum(area_pivot.get(col, 0) * peso for col, peso in pesos.items() if col in area_pivot.columns)
    denominador = area_pivot["area_total_ha"] * 3  # Normalizar a 0-1
    area_pivot["indice_aptitud_cacao"] = (numerador / denominador).round(3)
    
    # Guardar
    muni_file = os.path.join(DATA_PROCESSED_DIR, "zonificacion_cacao_valle_municipio.csv")
    area_pivot.to_csv(muni_file, index=False, encoding="utf-8-sig")
    log(f"  💾 Resumen municipal: {muni_file} ({len(area_pivot)} municipios)")
    
    log(f"\n  ✅ Agregación completada: {len(area_pivot)} municipios")
    
    return df, area_pivot


def generate_quality_report(df, area_pivot):
    """Genera reporte de calidad final."""
    log("")
    log("=" * 60)
    log("PASO 4: REPORTE DE CALIDAD")
    log("=" * 60)
    
    report = []
    report.append("# Reporte de Calidad – Zonificación de Cacao (Procesado)")
    report.append(f"\nFecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    report.append(f"\n## Resumen")
    report.append(f"- **Fuente**: UPRA – datos.gov.co (ID: jdjx-qer4)")
    report.append(f"- **Escala**: 1:100.000")
    report.append(f"- **Departamento**: Valle del Cauca")
    report.append(f"- **Polígonos procesados**: {len(df):,}")
    report.append(f"- **Municipios**: {area_pivot['municipio'].nunique()}")
    
    report.append(f"\n## Archivos Generados")
    report.append(f"| Archivo | Registros | Descripción |")
    report.append(f"|---------|-----------|-------------|")
    report.append(f"| zonificacion_cacao_valle_limpio.csv | {len(df):,} | Polígonos con aptitud y área |")
    report.append(f"| zonificacion_cacao_valle_municipio.csv | {len(area_pivot)} | Resumen por municipio: % aptitud |")
    
    report.append(f"\n## Distribución de Aptitud (Valle del Cauca)")
    area_by_apt = df.groupby("aptitud")["area_ha"].sum().sort_values(ascending=False)
    total = area_by_apt.sum()
    report.append(f"| Aptitud | Área (Ha) | % |")
    report.append(f"|---------|-----------|---|")
    for apt, area in area_by_apt.items():
        report.append(f"| {apt} | {area:,.1f} | {(area/total*100):.1f}% |")
    report.append(f"| **TOTAL** | **{total:,.1f}** | **100%** |")
    
    report.append(f"\n## Ranking de Municipios por Aptitud")
    report.append(f"| Municipio | Índice Aptitud | Aptitud Dominante | Área Total (Ha) |")
    report.append(f"|-----------|---------------|-------------------|-----------------|")
    sorted_munis = area_pivot.sort_values("indice_aptitud_cacao", ascending=False)
    for _, row in sorted_munis.iterrows():
        report.append(f"| {row['municipio']} | {row['indice_aptitud_cacao']:.3f} | {row['aptitud_dominante']} | {row['area_total_ha']:,.1f} |")
    
    report.append(f"\n## Evaluación de Utilidad para el Modelo RFRK")
    report.append(f"\n### ✅ Fortalezas")
    report.append(f"- Clasificación oficial de aptitud a escala 1:100.000")
    report.append(f"- Cubre los municipios del Valle del Cauca")
    report.append(f"- Incluye área (Ha) por polígono → permite cálculos de superficie")
    report.append(f"- El índice de aptitud calculado es directamente usable como feature")
    report.append(f"\n### ⚠️ Limitaciones")
    report.append(f"- Datos estáticos (no cambian en el tiempo)")
    report.append(f"- Geometrías excluidas de la descarga tabular")
    report.append(f"\n### 🎯 Conclusión")
    report.append(f"- **¿Es útil?**: ✅ SÍ")
    report.append(f"- **Uso principal**: Predictor base de aptitud agroecológica para cacao")
    report.append(f"- **Variables derivadas**: % aptitud por municipio + índice de aptitud (0-1)")
    report.append(f"- **Cruce con EVA**: Por código municipio DANE")
    
    report_text = "\n".join(report)
    report_file = os.path.join(DATA_REPORTS_DIR, "08_cacao_zonificacion_quality.md")
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(report_text)
    
    log(f"  📄 Reporte guardado: {report_file}")
    print("\n" + report_text)


# =============================================================================
# EJECUCIÓN PRINCIPAL
# =============================================================================
if __name__ == "__main__":
    log("🚀 Iniciando procesamiento de Zonificación de Cacao")
    log(f"   Departamento: {DEPARTAMENTO_INTERES}")
    log("")
    
    # Paso 1: Descargar
    df_raw = download_data()
    
    # Paso 2: Explorar
    explore_data(df_raw)
    
    # Paso 3: Limpiar y agregar
    df_clean, area_pivot = clean_and_aggregate(df_raw)
    
    # Paso 4: Reporte
    generate_quality_report(df_clean, area_pivot)
    
    log("")
    log("=" * 60)
    log("✅ PROCESAMIENTO COMPLETADO")
    log("=" * 60)
    log(f"   Archivos generados:")
    log(f"   - data/raw/zonificacion_cacao_valle_raw.csv")
    log(f"   - data/processed/zonificacion_cacao_valle_limpio.csv")
    log(f"   - data/processed/zonificacion_cacao_valle_municipio.csv")
    log(f"   - data/reports/07_cacao_zonificacion_exploration.md")
    log(f"   - data/reports/08_cacao_zonificacion_quality.md")
