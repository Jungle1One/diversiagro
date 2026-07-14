"""
=============================================================================
Dataset 2: Precipitación IDEAM
Fuente: IDEAM via datos.gov.co (Socrata API)
ID: s54a-sgyg
Total registros en origen: ~165,294,457 (mediciones cada 10 min)
Valle del Cauca: ~7,189,339 registros
=============================================================================

Este script:
1. Descarga datos de precipitación SOLO del Valle del Cauca via Socrata SODA API
2. Agrega los datos cada-10-min a nivel MENSUAL por estación
3. Realiza exploración y validación
4. Genera dataset limpio con precipitación mensual acumulada por estación
5. Genera promedios mensuales por municipio (para cruzar con EVA)
6. Exporta CSVs listos para modelado

NOTA IMPORTANTE: El dataset original tiene 165M+ registros (mediciones cada 10 min).
Filtramos en la API directamente por departamento = "VALLE DEL CAUCA" para
descargar solo ~7.2M registros, y luego los agregamos a nivel mensual.
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
BASE_URL = "https://www.datos.gov.co/api/v3/views/s54a-sgyg/query.json"
APP_TOKEN = "FbcYAmAYgsBJmr4HRkPhngV6X"

# Directorio de salida
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_RAW_DIR = os.path.join(PROJECT_DIR, "data", "raw")
DATA_PROCESSED_DIR = os.path.join(PROJECT_DIR, "data", "processed")
DATA_REPORTS_DIR = os.path.join(PROJECT_DIR, "data", "reports")

os.makedirs(DATA_RAW_DIR, exist_ok=True)
os.makedirs(DATA_PROCESSED_DIR, exist_ok=True)
os.makedirs(DATA_REPORTS_DIR, exist_ok=True)

DEPARTAMENTO_INTERES = "VALLE DEL CAUCA"

# =============================================================================
# FUNCIONES
# =============================================================================

def log(msg):
    """Imprime un mensaje con timestamp."""
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")


def download_valle_data():
    """
    Descarga datos de precipitación SOLO del Valle del Cauca.
    Usa el filtro $where en la API Socrata para filtrar en servidor.
    El dataset tiene ~7.2M registros para Valle del Cauca, 
    los descargamos en lotes de 50,000.
    """
    log("=" * 60)
    log("PASO 1: DESCARGA DE DATOS DE PRECIPITACIÓN")
    log(f"  Departamento: {DEPARTAMENTO_INTERES}")
    log("  ⚠️  Este proceso puede tardar varios minutos (~7.2M registros)")
    log("=" * 60)
    
    all_records = []
    offset = 1
    batch_size = 50000
    
    headers = {"X-App-Token": APP_TOKEN}
    
    while True:
        # params = {
        #     "pageNumber": offset,
        #     "pageSize": batch_size,
        #     "query": f"SELECT * WHERE departamento='{DEPARTAMENTO_INTERES}'"
        # }
        payload = {
            "query": f"SELECT codigoestacion, codigosensor, fechaobservacion, valorobservado, nombreestacion, departamento, municipio, zonahidrografica, latitud, longitud, descripcionsensor, unidadmedida WHERE departamento='{DEPARTAMENTO_INTERES}' AND fechaobservacion BETWEEN '2019-01-01T00:00:00' :: floating_timestamp AND '2024-07-07T23:45:00' :: floating_timestamp",
            "page": {
            "pageNumber": offset,
            "pageSize": batch_size
            }
        }

    
        log(f"  Descargando lote: offset={offset:,}...")
        
        try:
            response = requests.post(BASE_URL, headers=headers, json=payload, timeout=120)
        except requests.exceptions.Timeout:
            log(f"  ⚠️  Timeout en offset={offset:,}, reintentando...")
            try:
                response = requests.post(BASE_URL, headers=headers, json=payload, timeout=180)
            except requests.exceptions.Timeout:
                log(f"  ❌ Timeout persistente. Guardando {len(all_records):,} registros descargados hasta ahora.")
                break
        
        if response.status_code != 200:
            log(f"  ❌ Error HTTP {response.status_code}: {response.text[:200]}")
            if response.status_code == 429:  # Rate limit
                log("  ⏳ Rate limit alcanzado, esperando 10 segundos...")
                import time
                time.sleep(10)
                continue
            break
        
        batch = response.json()
        
        if not batch:
            log(f"  ✅ Descarga completa. Total: {len(all_records):,} registros")
            break
        
        all_records.extend(batch)
        log(f"  ✅ Lote: {len(batch):,} | Acumulado: {len(all_records):,}")
        offset += 1
        
        # Guardar checkpoint cada 500,000 registros
        if len(all_records) % 500000 < batch_size:
            log(f"  💾 Checkpoint: guardando progreso parcial...")
            df_temp = pd.DataFrame(all_records)
            df_temp.to_csv(
                os.path.join(DATA_RAW_DIR, "ideam_precipitacion_valle_checkpoint.csv"),
                index=False, encoding="utf-8-sig"
            )
    
    # Guardar datos crudos completos
    df_raw = pd.DataFrame(all_records)
    raw_file = os.path.join(DATA_RAW_DIR, "ideam_precipitacion_valle_raw.csv")
    df_raw.to_csv(raw_file, index=False, encoding="utf-8-sig")
    log(f"  💾 Datos crudos guardados: {raw_file}")
    log(f"  📊 Shape: {df_raw.shape}")
    
    return df_raw


def explore_data(df):
    """Exploración inicial del dataset de precipitación."""
    log("")
    log("=" * 60)
    log("PASO 2: EXPLORACIÓN INICIAL")
    log("=" * 60)
    
    report = []
    report.append("# Reporte de Exploración – Precipitación IDEAM")
    report.append(f"\nFecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"\n## Información General")
    report.append(f"- **Fuente**: IDEAM – datos.gov.co (ID: s54a-sgyg)")
    report.append(f"- **Departamento**: {DEPARTAMENTO_INTERES}")
    report.append(f"- **Total registros descargados**: {len(df):,}")
    report.append(f"- **Columnas**: {', '.join(df.columns.tolist())}")
    
    # Tipos de datos
    report.append(f"\n## Tipos de Datos")
    for col in df.columns:
        report.append(f"- `{col}`: {df[col].dtype}")
    
    # Valores nulos
    report.append(f"\n## Valores Nulos")
    for col in df.columns:
        nulls = df[col].isnull().sum()
        pct = (nulls / len(df)) * 100
        report.append(f"- `{col}`: {nulls:,} ({pct:.1f}%)")
    
    # Estaciones
    report.append(f"\n## Estaciones Meteorológicas")
    report.append(f"- **Total estaciones**: {df['codigoestacion'].nunique()}")
    report.append(f"\n### Estaciones disponibles")
    estaciones = df.groupby(['codigoestacion', 'nombreestacion', 'municipio']).size().reset_index(name='registros')
    estaciones = estaciones.sort_values('registros', ascending=False)
    report.append(f"| Código | Nombre | Municipio | Registros |")
    report.append(f"|--------|--------|-----------|-----------|")
    for _, row in estaciones.iterrows():
        report.append(f"| {row['codigoestacion']} | {row['nombreestacion']} | {row['municipio']} | {row['registros']:,} |")
    
    # Municipios
    report.append(f"\n## Municipios con estaciones")
    report.append(f"- **Total municipios**: {df['municipio'].nunique()}")
    muni_counts = df['municipio'].value_counts()
    for muni, count in muni_counts.items():
        report.append(f"  - {muni}: {count:,} registros")
    
    # Rango temporal
    if 'fechaobservacion' in df.columns:
        df['fechaobservacion'] = pd.to_datetime(df['fechaobservacion'], errors='coerce')
        fecha_min = df['fechaobservacion'].min()
        fecha_max = df['fechaobservacion'].max()
        report.append(f"\n## Rango Temporal")
        report.append(f"- **Desde**: {fecha_min}")
        report.append(f"- **Hasta**: {fecha_max}")
    
    # Estadísticas de precipitación
    df['valorobservado'] = pd.to_numeric(df['valorobservado'], errors='coerce')
    report.append(f"\n## Estadísticas de Precipitación (mm cada 10 min)")
    stats = df['valorobservado'].describe()
    for stat_name, val in stats.items():
        report.append(f"- {stat_name}: {val:,.4f}")
    
    # Valores > 0 (lluvia real)
    lluvia = df[df['valorobservado'] > 0]
    pct_lluvia = (len(lluvia) / len(df)) * 100
    report.append(f"\n## Registros con lluvia (valor > 0)")
    report.append(f"- {len(lluvia):,} de {len(df):,} ({pct_lluvia:.1f}%)")
    report.append(f"- Precipitación promedio cuando llueve: {lluvia['valorobservado'].mean():.2f} mm")
    
    # Coordenadas de las estaciones
    report.append(f"\n## Coordenadas de estaciones (para mapas)")
    coords = df.groupby(['codigoestacion', 'nombreestacion', 'municipio']).agg(
        latitud=('latitud', 'first'),
        longitud=('longitud', 'first')
    ).reset_index()
    report.append(f"| Estación | Municipio | Latitud | Longitud |")
    report.append(f"|----------|-----------|---------|----------|")
    for _, row in coords.iterrows():
        report.append(f"| {row['nombreestacion']} | {row['municipio']} | {row['latitud']} | {row['longitud']} |")
    
    # Guardar reporte
    report_text = "\n".join(report)
    report_file = os.path.join(DATA_REPORTS_DIR, "03_ideam_exploration_report.md")
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(report_text)
    
    log(f"  📄 Reporte guardado: {report_file}")
    print("\n" + report_text[:3000] + "\n... [reporte completo en archivo]")
    
    return df


def aggregate_and_clean(df):
    """
    Agrega datos cada-10-min a nivel mensual y limpia.
    
    Para el modelo RFRK necesitamos precipitación a nivel mensual/anual
    por municipio, no cada 10 minutos.
    
    Genera:
    1. Precipitación mensual acumulada por estación
    2. Precipitación mensual promedio por municipio
    3. Precipitación anual acumulada por municipio
    """
    log("")
    log("=" * 60)
    log("PASO 3: AGREGACIÓN Y LIMPIEZA")
    log("=" * 60)
    
    # --- 3.1 Convertir tipos ---
    log("  3.1 Convirtiendo tipos...")
    df['fechaobservacion'] = pd.to_datetime(df['fechaobservacion'], errors='coerce')
    df['valorobservado'] = pd.to_numeric(df['valorobservado'], errors='coerce')
    df['latitud'] = pd.to_numeric(df['latitud'], errors='coerce')
    df['longitud'] = pd.to_numeric(df['longitud'], errors='coerce')
    
    # --- 3.2 Eliminar registros sin fecha o valor ---
    log("  3.2 Eliminando registros inválidos...")
    antes = len(df)
    df = df.dropna(subset=['fechaobservacion', 'valorobservado'])
    log(f"      Eliminados: {antes - len(df):,} registros sin fecha/valor")
    
    # --- 3.3 Filtrar valores negativos (errores de sensor) ---
    log("  3.3 Filtrando valores negativos...")
    negativos = (df['valorobservado'] < 0).sum()
    df = df[df['valorobservado'] >= 0]
    log(f"      Valores negativos eliminados: {negativos:,}")
    
    # --- 3.4 Filtrar valores extremos (>30mm en 10 min = posible error) ---
    log("  3.4 Filtrando valores extremos...")
    # 30mm en 10 minutos es el máximo registrado en el dataset
    # Valores mayores podrían ser errores de sensor
    extremos = (df['valorobservado'] > 50).sum()
    df = df[df['valorobservado'] <= 50]
    log(f"      Valores > 50mm/10min eliminados: {extremos:,}")
    
    # --- 3.5 Extraer año y mes ---
    log("  3.5 Extrayendo componentes temporales...")
    df['anio'] = df['fechaobservacion'].dt.year
    df['mes'] = df['fechaobservacion'].dt.month
    df['dia'] = df['fechaobservacion'].dt.day
    
    # --- 3.6 Agregar a nivel MENSUAL por estación ---
    log("  3.6 Agregando a nivel mensual por estación...")
    monthly_station = df.groupby(
        ['codigoestacion', 'nombreestacion', 'municipio', 'latitud', 'longitud', 'anio', 'mes']
    ).agg(
        precipitacion_acumulada_mm=('valorobservado', 'sum'),
        n_mediciones=('valorobservado', 'count'),
        dias_con_lluvia=('valorobservado', lambda x: (x > 0).sum()),
        max_precipitacion_10min=('valorobservado', 'max'),
        precipitacion_promedio_10min=('valorobservado', 'mean'),
    ).reset_index()
    
    log(f"      Resultado: {len(monthly_station):,} registros mensuales por estación")
    
    # Guardar mensual por estación
    station_file = os.path.join(DATA_PROCESSED_DIR, "ideam_precipitacion_mensual_estacion.csv")
    monthly_station.to_csv(station_file, index=False, encoding="utf-8-sig")
    log(f"      💾 Guardado: {station_file}")
    
    # --- 3.7 Agregar a nivel MENSUAL por municipio ---
    log("  3.7 Agregando a nivel mensual por municipio...")
    monthly_muni = monthly_station.groupby(['municipio', 'anio', 'mes']).agg(
        precipitacion_promedio_mm=('precipitacion_acumulada_mm', 'mean'),
        precipitacion_max_mm=('precipitacion_acumulada_mm', 'max'),
        precipitacion_min_mm=('precipitacion_acumulada_mm', 'min'),
        n_estaciones=('codigoestacion', 'nunique'),
        dias_con_lluvia_promedio=('dias_con_lluvia', 'mean'),
    ).reset_index()
    
    log(f"      Resultado: {len(monthly_muni):,} registros mensuales por municipio")
    
    muni_file = os.path.join(DATA_PROCESSED_DIR, "ideam_precipitacion_mensual_municipio.csv")
    monthly_muni.to_csv(muni_file, index=False, encoding="utf-8-sig")
    log(f"      💾 Guardado: {muni_file}")
    
    # --- 3.8 Agregar a nivel ANUAL por municipio ---
    log("  3.8 Agregando a nivel anual por municipio...")
    annual_muni = monthly_muni.groupby(['municipio', 'anio']).agg(
        precipitacion_anual_mm=('precipitacion_promedio_mm', 'sum'),
        precipitacion_mensual_max_mm=('precipitacion_promedio_mm', 'max'),
        precipitacion_mensual_min_mm=('precipitacion_promedio_mm', 'min'),
        meses_con_datos=('mes', 'count'),
        dias_lluvia_total=('dias_con_lluvia_promedio', 'sum'),
    ).reset_index()
    
    # Calcular variabilidad intra-anual
    variabilidad = monthly_muni.groupby(['municipio', 'anio'])['precipitacion_promedio_mm'].std().reset_index()
    variabilidad.columns = ['municipio', 'anio', 'variabilidad_mensual_mm']
    annual_muni = annual_muni.merge(variabilidad, on=['municipio', 'anio'], how='left')
    
    log(f"      Resultado: {len(annual_muni):,} registros anuales por municipio")
    
    annual_file = os.path.join(DATA_PROCESSED_DIR, "ideam_precipitacion_anual_municipio.csv")
    annual_muni.to_csv(annual_file, index=False, encoding="utf-8-sig")
    log(f"      💾 Guardado: {annual_file}")
    
    # --- 3.9 Catálogo de estaciones ---
    log("  3.9 Generando catálogo de estaciones...")
    catalogo = df.groupby(['codigoestacion', 'nombreestacion', 'municipio']).agg(
        latitud=('latitud', 'first'),
        longitud=('longitud', 'first'),
        fecha_inicio=('fechaobservacion', 'min'),
        fecha_fin=('fechaobservacion', 'max'),
        total_mediciones=('valorobservado', 'count'),
        precipitacion_total_mm=('valorobservado', 'sum'),
    ).reset_index()
    
    catalogo_file = os.path.join(DATA_PROCESSED_DIR, "ideam_catalogo_estaciones_valle.csv")
    catalogo.to_csv(catalogo_file, index=False, encoding="utf-8-sig")
    log(f"      💾 Catálogo de estaciones guardado: {catalogo_file}")
    
    return monthly_station, monthly_muni, annual_muni, catalogo


def generate_quality_report(monthly_station, monthly_muni, annual_muni, catalogo):
    """Genera reporte de calidad final."""
    log("")
    log("=" * 60)
    log("PASO 4: REPORTE DE CALIDAD")
    log("=" * 60)
    
    report = []
    report.append("# Reporte de Calidad – Precipitación IDEAM (Procesado)")
    report.append(f"\nFecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    report.append(f"\n## Resumen de Procesamiento")
    report.append(f"- **Fuente**: IDEAM – datos.gov.co (ID: s54a-sgyg)")
    report.append(f"- **Departamento**: Valle del Cauca")
    report.append(f"- **Estaciones**: {len(catalogo)}")
    report.append(f"- **Municipios con datos**: {monthly_muni['municipio'].nunique()}")
    
    report.append(f"\n## Archivos Generados")
    report.append(f"| Archivo | Registros | Descripción |")
    report.append(f"|---------|-----------|-------------|")
    report.append(f"| ideam_precipitacion_mensual_estacion.csv | {len(monthly_station):,} | Precipitación mensual acumulada por estación |")
    report.append(f"| ideam_precipitacion_mensual_municipio.csv | {len(monthly_muni):,} | Precipitación mensual promedio por municipio |")
    report.append(f"| ideam_precipitacion_anual_municipio.csv | {len(annual_muni):,} | Precipitación anual por municipio |")
    report.append(f"| ideam_catalogo_estaciones_valle.csv | {len(catalogo):,} | Catálogo de estaciones meteorológicas |")
    
    report.append(f"\n## Cobertura Temporal por Municipio")
    report.append(f"| Municipio | Años | Estaciones |")
    report.append(f"|-----------|------|------------|")
    for muni in sorted(annual_muni['municipio'].unique()):
        data = annual_muni[annual_muni['municipio'] == muni]
        anios = f"{data['anio'].min()}-{data['anio'].max()}"
        n_est = catalogo[catalogo['municipio'] == muni]['codigoestacion'].nunique()
        report.append(f"| {muni} | {anios} | {n_est} |")
    
    report.append(f"\n## Estadísticas de Precipitación Anual (mm)")
    stats_anual = annual_muni['precipitacion_anual_mm'].describe()
    for stat, val in stats_anual.items():
        report.append(f"- {stat}: {val:,.1f}")
    
    report.append(f"\n## Evaluación de Utilidad para el Modelo RFRK")
    report.append(f"\n### ✅ Fortalezas")
    report.append(f"- Datos de alta resolución temporal (cada 10 min) agregados a mensual/anual")
    report.append(f"- Coordenadas GPS de cada estación (útil para Kriging espacial)")
    report.append(f"- Múltiples estaciones por municipio (mejor cobertura)")
    report.append(f"\n### ⚠️ Limitaciones")
    report.append(f"- Datos crudos NO validados por IDEAM (control de calidad básico)")
    report.append(f"- No todos los municipios del Valle tienen estaciones")
    report.append(f"- Posibles gaps temporales en algunas estaciones")
    report.append(f"\n### 🎯 Conclusión")
    report.append(f"- **¿Es útil para el proyecto?**: ✅ SÍ")
    report.append(f"- **Uso principal**: Predictor climático (precipitación) para el modelo RFRK")
    report.append(f"- **Cruce con EVA**: Por municipio y año")
    
    report_text = "\n".join(report)
    report_file = os.path.join(DATA_REPORTS_DIR, "04_ideam_quality_report.md")
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(report_text)
    
    log(f"  📄 Reporte guardado: {report_file}")
    print("\n" + report_text)


# =============================================================================
# EJECUCIÓN PRINCIPAL
# =============================================================================
if __name__ == "__main__":
    log("🚀 Iniciando procesamiento del Dataset Precipitación IDEAM")
    log(f"   Departamento: {DEPARTAMENTO_INTERES}")
    log(f"   ⚠️  Este proceso puede tardar 10-30 minutos (millones de registros)")
    log("")
    
    # Paso 1: Descargar datos del Valle del Cauca
    df_raw = download_valle_data()
    
    # Paso 2: Exploración
    explore_data(df_raw)
    
    # Paso 3: Agregación y limpieza
    monthly_station, monthly_muni, annual_muni, catalogo = aggregate_and_clean(df_raw)
    
    # Paso 4: Reporte de calidad
    generate_quality_report(monthly_station, monthly_muni, annual_muni, catalogo)
    
    log("")
    log("=" * 60)
    log("✅ PROCESAMIENTO COMPLETADO")
    log("=" * 60)
    log(f"   Archivos generados en:")
    log(f"   - Datos crudos: data/raw/ideam_precipitacion_valle_raw.csv")
    log(f"   - Mensual/estación: data/processed/ideam_precipitacion_mensual_estacion.csv")
    log(f"   - Mensual/municipio: data/processed/ideam_precipitacion_mensual_municipio.csv")
    log(f"   - Anual/municipio: data/processed/ideam_precipitacion_anual_municipio.csv")
    log(f"   - Catálogo estaciones: data/processed/ideam_catalogo_estaciones_valle.csv")
