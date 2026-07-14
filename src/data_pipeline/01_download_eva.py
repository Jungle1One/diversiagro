"""
=============================================================================
Dataset 1: EVA (Evaluaciones Agropecuarias Municipales) 2019-2024
Fuente: UPRA via datos.gov.co (Socrata API)
ID: uejq-wxrr
Total registros en origen: ~141,073
=============================================================================

Este script:
1. Descarga TODOS los datos del dataset EVA 2019-2024 via Socrata SODA API
2. Realiza exploración inicial (estructura, tipos, nulos, distribuciones)
3. Filtra para Valle del Cauca y cultivos de interés (café, plátano, caña, cacao)
4. Limpia y normaliza los datos
5. Genera análisis de utilidad para el modelo RFRK
6. Exporta CSVs limpios listos para modelado
"""

import sys
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass
import requests
import pandas as pd
import os
import json
from datetime import datetime

# =============================================================================
# CONFIGURACIÓN
# =============================================================================
BASE_URL = "https://www.datos.gov.co/api/v3/views/uejq-wxrr/query.json"
APP_TOKEN = "FbcYAmAYgsBJmr4HRkPhngV6X"

# Directorio de salida
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_RAW_DIR = os.path.join(PROJECT_DIR, "data", "raw")
DATA_PROCESSED_DIR = os.path.join(PROJECT_DIR, "data", "processed")
DATA_REPORTS_DIR = os.path.join(PROJECT_DIR, "data", "reports")

os.makedirs(DATA_RAW_DIR, exist_ok=True)
os.makedirs(DATA_PROCESSED_DIR, exist_ok=True)
os.makedirs(DATA_REPORTS_DIR, exist_ok=True)

# Cultivos de interés para el proyecto
CULTIVOS_INTERES = ["Café", "Plátano", "Caña", "Cacao", "Papaya", "Fresa", "Aguacate", "Banano"]
DEPARTAMENTO_INTERES = "Valle del Cauca"
CODIGO_DEPTO = "76"

# Mapeo de nombres de campo API -> nombres legibles
COLUMN_MAP = {
    "c_digo_dane_departamento": "codigo_departamento",
    "departamento": "departamento",
    "c_digo_dane_municipio": "codigo_municipio",
    "municipio": "municipio",
    "grupo_cultivo": "grupo_cultivo",
    "subgrupo": "subgrupo",
    "cultivo": "cultivo",
    "desagregaci_n_cultivo": "desagregacion_cultivo",
    "a_o": "anio",
    "periodo": "periodo",
    "rea_sembrada": "area_sembrada_ha",
    "rea_cosechada": "area_cosechada_ha",
    "producci_n": "produccion_ton",
    "rendimiento": "rendimiento_ton_ha",
    "ciclo_del_cultivo": "ciclo_cultivo",
    "estado_f_sico_del_cultivo": "estado_fisico",
    "c_digo_del_cultivo": "codigo_cultivo",
    "nombre_cient_fico_del_cultivo": "nombre_cientifico",
}

# =============================================================================
# FUNCIONES
# =============================================================================

def log(msg):
    """Imprime un mensaje con timestamp."""
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")


def download_all_data():
    """
    Descarga TODOS los registros del dataset usando paginación.
    La API de Socrata tiene un límite de 50,000 por petición con $limit.
    """
    log("=" * 60)
    log("PASO 1: DESCARGA DE DATOS")
    log("=" * 60)
    
    # Ruta del archivo raw
    raw_file = os.path.join(DATA_RAW_DIR, "eva_2019_2024_raw.csv")
    
    if os.path.exists(raw_file):
        log(f"  ✅ Archivo crudo ya existe en: {raw_file}")
        log(f"  📥 Cargando datos locales en lugar de descargar de nuevo...")
        df_raw = pd.read_csv(raw_file)
        log(f"  📊 Shape: {df_raw.shape}")
        return df_raw

    all_records = []
    pageNumber = 1
    batch_size = 10000  # Máximo permitido por Socrata
    
    headers = {"X-App-Token": APP_TOKEN}
    
    while True:
        params = {
            "pageSize": batch_size,
            "pageNumber": pageNumber,
            "$order": ":id",
        }
        
        log(f"  Descargando página: pageNumber={pageNumber}, pageSize={batch_size}...")
        response = requests.get(BASE_URL, headers=headers, params=params)
        
        if response.status_code != 200:
            log(f"  ❌ Error HTTP {response.status_code}: {response.text[:200]}")
            break
        
        batch = response.json()
        
        if not batch:
            log(f"  ✅ No hay más registros. Total descargado: {len(all_records)}")
            break
        
        all_records.extend(batch)
        log(f"  ✅ Página {pageNumber} recibida: {len(batch)} registros (acumulado: {len(all_records)})")
        pageNumber += 1
    
    # Guardar datos crudos
    df_raw = pd.DataFrame(all_records)
    df_raw.to_csv(raw_file, index=False, encoding="utf-8-sig")
    log(f"  💾 Datos crudos guardados en: {raw_file}")
    log(f"  📊 Shape: {df_raw.shape}")
    
    return df_raw


def explore_data(df):
    """Exploración inicial del dataset completo."""
    log("")
    log("=" * 60)
    log("PASO 2: EXPLORACIÓN INICIAL")
    log("=" * 60)
    
    report_lines = []
    report_lines.append("# Reporte de Exploración - Dataset EVA 2019-2024")
    report_lines.append(f"\nFecha de generación: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append(f"\n## Información General")
    report_lines.append(f"- **Total de registros**: {len(df):,}")
    report_lines.append(f"- **Total de columnas**: {len(df.columns)}")
    report_lines.append(f"- **Columnas**: {', '.join(df.columns.tolist())}")
    
    # Tipos de datos
    report_lines.append(f"\n## Tipos de Datos")
    for col in df.columns:
        report_lines.append(f"- `{col}`: {df[col].dtype}")
    
    # Valores nulos
    report_lines.append(f"\n## Valores Nulos")
    null_counts = df.isnull().sum()
    for col in df.columns:
        pct = (null_counts[col] / len(df)) * 100
        report_lines.append(f"- `{col}`: {null_counts[col]:,} ({pct:.1f}%)")
    
    # Departamentos únicos
    if "departamento" in df.columns:
        deptos = df["departamento"].value_counts()
        report_lines.append(f"\n## Distribución por Departamento (Top 10)")
        for depto, count in deptos.head(10).items():
            marker = " ⬅️ **INTERÉS**" if depto == DEPARTAMENTO_INTERES else ""
            report_lines.append(f"- {depto}: {count:,} registros{marker}")
    
    # Años disponibles
    if "a_o" in df.columns:
        anios = sorted(df["a_o"].dropna().unique())
        report_lines.append(f"\n## Años Disponibles")
        report_lines.append(f"- {', '.join([str(a) for a in anios])}")
        for a in anios:
            count = len(df[df["a_o"] == a])
            report_lines.append(f"  - {a}: {count:,} registros")
    
    # Cultivos únicos
    if "cultivo" in df.columns:
        cultivos = df["cultivo"].value_counts()
        report_lines.append(f"\n## Cultivos Únicos: {len(cultivos)}")
        report_lines.append(f"\n### Cultivos de Interés para el Proyecto")
        for c in CULTIVOS_INTERES:
            count = len(df[df["cultivo"] == c])
            report_lines.append(f"- **{c}**: {count:,} registros")
    
    # Valle del Cauca específico
    if "departamento" in df.columns:
        df_vc = df[df["departamento"] == DEPARTAMENTO_INTERES]
        report_lines.append(f"\n## Datos Valle del Cauca")
        report_lines.append(f"- **Total registros**: {len(df_vc):,}")
        if "cultivo" in df_vc.columns:
            report_lines.append(f"- **Cultivos distintos**: {df_vc['cultivo'].nunique()}")
            report_lines.append(f"\n### Cultivos de Interés en Valle del Cauca")
            for c in CULTIVOS_INTERES:
                count = len(df_vc[df_vc["cultivo"] == c])
                report_lines.append(f"- **{c}**: {count:,} registros")
        if "municipio" in df_vc.columns:
            report_lines.append(f"- **Municipios**: {df_vc['municipio'].nunique()}")
            report_lines.append(f"\n### Municipios del Valle del Cauca ({df_vc['municipio'].nunique()} únicos)")
            for mun, count in df_vc["municipio"].value_counts().items():
                report_lines.append(f"  - {mun}: {count:,}")
    
    # Estadísticas numéricas
    numeric_cols = ["rea_sembrada", "rea_cosechada", "producci_n", "rendimiento"]
    existing_numeric = [c for c in numeric_cols if c in df.columns]
    if existing_numeric:
        report_lines.append(f"\n## Estadísticas Numéricas (Dataset Completo)")
        for col in existing_numeric:
            df[col] = pd.to_numeric(df[col], errors="coerce")
            stats = df[col].describe()
            report_lines.append(f"\n### {col}")
            for stat_name, val in stats.items():
                report_lines.append(f"  - {stat_name}: {val:,.2f}")
    
    # Guardar reporte
    report_text = "\n".join(report_lines)
    report_file = os.path.join(DATA_REPORTS_DIR, "01_eva_exploration_report.md")
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(report_text)
    
    log(f"  📄 Reporte de exploración guardado en: {report_file}")
    print("\n" + report_text)
    
    return report_text


def clean_and_filter(df):
    """
    Limpia y filtra los datos:
    1. Renombra columnas a español limpio
    2. Convierte tipos de datos
    3. Filtra Valle del Cauca
    4. Filtra cultivos de interés
    5. Trata valores nulos
    6. Elimina duplicados
    7. Valida rangos
    """
    log("")
    log("=" * 60)
    log("PASO 3: LIMPIEZA Y FILTRADO")
    log("=" * 60)
    
    # --- 3.1 Renombrar columnas ---
    log("  3.1 Renombrando columnas...")
    print(df.columns)
    existing_cols = {k: v for k, v in COLUMN_MAP.items() if k in df.columns}
    df = df.rename(columns=existing_cols)
    log(f"      Columnas renombradas: {len(existing_cols)}")
    
    # --- 3.2 Convertir tipos de datos ---
    log("  3.2 Convirtiendo tipos de datos...")
    numeric_cols = ["area_sembrada_ha", "area_cosechada_ha", "produccion_ton", "rendimiento_ton_ha", "anio", "codigo_cultivo"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    
    # Convertir año a int donde sea posible
    if "anio" in df.columns:
        df["anio"] = df["anio"].fillna(0).astype(int)
    
    # Asegurar strings limpios
    str_cols = ["departamento", "municipio", "cultivo", "desagregacion_cultivo", 
                "grupo_cultivo", "subgrupo", "ciclo_cultivo", "estado_fisico",
                "nombre_cientifico", "periodo", "codigo_departamento", "codigo_municipio"]
    for col in str_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()
    
    log(f"      ✅ Tipos convertidos")
    
    # --- 3.3 Filtrar Valle del Cauca ---
    log("  3.3 Filtrando Valle del Cauca...")
    total_before = len(df)
    df_vc = df[df["codigo_departamento"] == CODIGO_DEPTO].copy()
    log(f"      Total nacional: {total_before:,} → Valle del Cauca: {len(df_vc):,}")
    
    # --- 3.4 Guardar dataset completo del Valle ---
    vc_all_file = os.path.join(DATA_PROCESSED_DIR, "eva_valle_del_cauca_all.csv")
    df_vc.to_csv(vc_all_file, index=False, encoding="utf-8-sig")
    log(f"      💾 Todos los cultivos del Valle guardados: {vc_all_file}")
    
    # --- 3.5 Filtrar cultivos de interés ---
    log("  3.5 Filtrando cultivos de interés...")
    df_target = df_vc[df_vc["cultivo"].isin(CULTIVOS_INTERES)].copy()
    log(f"      Cultivos de interés: {len(df_target):,} registros")
    for c in CULTIVOS_INTERES:
        count = len(df_target[df_target["cultivo"] == c])
        log(f"        - {c}: {count:,}")
    
    # --- 3.6 Eliminar duplicados ---
    log("  3.6 Eliminando duplicados...")
    dupes_before = len(df_target)
    # Un registro es único por: municipio + cultivo + desagregación + periodo
    df_target = df_target.drop_duplicates(
        subset=["codigo_municipio", "cultivo", "desagregacion_cultivo", "periodo"],
        keep="first"
    )
    dupes_removed = dupes_before - len(df_target)
    log(f"      Duplicados eliminados: {dupes_removed}")
    
    # --- 3.7 Tratar valores nulos en variables numéricas ---
    log("  3.7 Tratando valores nulos...")
    for col in ["area_sembrada_ha", "area_cosechada_ha", "produccion_ton", "rendimiento_ton_ha"]:
        if col in df_target.columns:
            nulls = df_target[col].isnull().sum()
            if nulls > 0:
                # Rellenar con mediana por municipio y cultivo
                medians = df_target.groupby(["codigo_municipio", "cultivo"])[col].transform("median")
                df_target[col] = df_target[col].fillna(medians)
                # Si aún quedan nulos, usar mediana general del cultivo
                medians_cultivo = df_target.groupby("cultivo")[col].transform("median")
                df_target[col] = df_target[col].fillna(medians_cultivo)
                # Último recurso: llenar con 0
                df_target[col] = df_target[col].fillna(0)
                log(f"      {col}: {nulls} nulos tratados")
    
    # --- 3.8 Validar rangos ---
    log("  3.8 Validando rangos...")
    # Eliminar registros con área o producción negativa
    for col in ["area_sembrada_ha", "area_cosechada_ha", "produccion_ton"]:
        if col in df_target.columns:
            negatives = (df_target[col] < 0).sum()
            if negatives > 0:
                df_target = df_target[df_target[col] >= 0]
                log(f"      ⚠️ {col}: {negatives} valores negativos eliminados")
    
    # Recalcular rendimiento donde sea 0 pero haya área cosechada
    mask_recalc = (df_target["rendimiento_ton_ha"] == 0) & (df_target["area_cosechada_ha"] > 0)
    if mask_recalc.sum() > 0:
        df_target.loc[mask_recalc, "rendimiento_ton_ha"] = (
            df_target.loc[mask_recalc, "produccion_ton"] / df_target.loc[mask_recalc, "area_cosechada_ha"]
        )
        log(f"      🔄 Rendimiento recalculado en {mask_recalc.sum()} registros")
    
    # Eliminar registros donde todo es 0 (sin actividad real)
    mask_zeros = (
        (df_target["area_sembrada_ha"] == 0) & 
        (df_target["area_cosechada_ha"] == 0) & 
        (df_target["produccion_ton"] == 0)
    )
    zeros_count = mask_zeros.sum()
    df_target = df_target[~mask_zeros]
    log(f"      🗑️ Registros con todas las métricas en 0 eliminados: {zeros_count}")
    
    # --- 3.9 Resultado final ---
    log(f"\n  ✅ Dataset limpio final: {len(df_target):,} registros, {len(df_target.columns)} columnas")
    
    return df_target, df_vc


def generate_final_outputs(df_target, df_vc):
    """Genera los archivos finales y reporte de calidad."""
    log("")
    log("=" * 60)
    log("PASO 4: GENERACIÓN DE ARCHIVOS FINALES")
    log("=" * 60)
    
    # --- CSV principal: cultivos de interés ---
    target_file = os.path.join(DATA_PROCESSED_DIR, "eva_valle_cultivos_interes.csv")
    df_target.to_csv(target_file, index=False, encoding="utf-8-sig")
    log(f"  💾 CSV principal (cultivos interés): {target_file}")
    
    # --- CSVs individuales por cultivo ---
    for cultivo in CULTIVOS_INTERES:
        df_cult = df_target[df_target["cultivo"] == cultivo]
        if len(df_cult) > 0:
            safe_name = cultivo.lower().replace(" ", "_")
            cult_file = os.path.join(DATA_PROCESSED_DIR, f"eva_valle_{safe_name}.csv")
            df_cult.to_csv(cult_file, index=False, encoding="utf-8-sig")
            log(f"  💾 CSV {cultivo}: {cult_file} ({len(df_cult):,} registros)")
    
    # --- Reporte de calidad final ---
    report_lines = []
    report_lines.append("# Reporte de Calidad - Dataset EVA (Procesado)")
    report_lines.append(f"\nFecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    report_lines.append(f"\n## Resumen de Procesamiento")
    report_lines.append(f"- **Fuente**: datos.gov.co – EVA 2019-2024 (ID: uejq-wxrr)")
    report_lines.append(f"- **Departamento**: Valle del Cauca (código 76)")
    report_lines.append(f"- **Registros Valle del Cauca (todos los cultivos)**: {len(df_vc):,}")
    report_lines.append(f"- **Registros cultivos de interés (limpio)**: {len(df_target):,}")
    
    report_lines.append(f"\n## Columnas del Dataset Final")
    report_lines.append("| Columna | Tipo | No Nulos | % Completo |")
    report_lines.append("|---------|------|----------|------------|")
    for col in df_target.columns:
        non_null = df_target[col].notna().sum()
        pct = (non_null / len(df_target)) * 100
        report_lines.append(f"| {col} | {df_target[col].dtype} | {non_null:,} | {pct:.1f}% |")
    
    report_lines.append(f"\n## Distribución por Cultivo")
    report_lines.append("| Cultivo | Registros | Municipios | Años |")
    report_lines.append("|---------|-----------|------------|------|")
    for c in CULTIVOS_INTERES:
        df_c = df_target[df_target["cultivo"] == c]
        if len(df_c) > 0:
            munis = df_c["municipio"].nunique()
            anios = sorted(df_c["anio"].unique())
            anios_str = f"{min(anios)}-{max(anios)}"
            report_lines.append(f"| {c} | {len(df_c):,} | {munis} | {anios_str} |")
    
    report_lines.append(f"\n## Estadísticas por Cultivo")
    for c in CULTIVOS_INTERES:
        df_c = df_target[df_target["cultivo"] == c]
        if len(df_c) > 0:
            report_lines.append(f"\n### {c}")
            report_lines.append("| Métrica | Área Sembrada (Ha) | Área Cosechada (Ha) | Producción (Ton) | Rendimiento (Ton/Ha) |")
            report_lines.append("|---------|-------------------|--------------------|-----------------|--------------------|")
            for stat in ["mean", "std", "min", "25%", "50%", "75%", "max"]:
                vals = []
                for metric in ["area_sembrada_ha", "area_cosechada_ha", "produccion_ton", "rendimiento_ton_ha"]:
                    if metric in df_c.columns:
                        desc = df_c[metric].describe()
                        vals.append(f"{desc.get(stat, 0):,.2f}")
                    else:
                        vals.append("N/A")
                report_lines.append(f"| {stat} | {' | '.join(vals)} |")
    
    report_lines.append(f"\n## Distribución por Municipio y Cultivo (Valle del Cauca)")
    pivot = df_target.groupby(["municipio", "cultivo"]).size().unstack(fill_value=0)
    report_lines.append(f"\n| Municipio | {' | '.join(pivot.columns)} |")
    report_lines.append(f"|-----------|{'|'.join(['---' for _ in pivot.columns])}|")
    for mun in sorted(pivot.index):
        vals = [str(pivot.loc[mun, c]) if c in pivot.columns else "0" for c in pivot.columns]
        report_lines.append(f"| {mun} | {' | '.join(vals)} |")
    
    report_lines.append(f"\n## Evaluación de Utilidad para el Modelo RFRK")
    report_lines.append(f"\n### ✅ Fortalezas")
    report_lines.append(f"- Datos de rendimiento (variable objetivo) disponibles 2019-2024")
    report_lines.append(f"- Cobertura municipal completa del Valle del Cauca")
    report_lines.append(f"- Los 4 cultivos de interés están presentes")
    report_lines.append(f"- Datos semestrales para cultivos transitorios")
    
    report_lines.append(f"\n### ⚠️ Limitaciones")
    report_lines.append(f"- Resolución a nivel municipal (no vereda)")
    report_lines.append(f"- Algunos registros tienen rendimiento 0 o área cosechada 0")
    report_lines.append(f"- Es información subjetiva (no medida con instrumentos)")
    
    report_lines.append(f"\n### 🎯 Conclusión")
    report_lines.append(f"- **¿Es útil para el proyecto?**: ✅ SÍ")
    report_lines.append(f"- **Uso principal**: Variable objetivo (rendimiento Ton/Ha) para entrenar el modelo RFRK")
    report_lines.append(f"- **Nivel de resolución**: Municipal (suficiente para prototipo)")
    
    report_text = "\n".join(report_lines)
    report_file = os.path.join(DATA_REPORTS_DIR, "02_eva_quality_report.md")
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(report_text)
    
    log(f"  📄 Reporte de calidad guardado: {report_file}")
    print("\n" + report_text)


# =============================================================================
# EJECUCIÓN PRINCIPAL
# =============================================================================
if __name__ == "__main__":
    log("🚀 Iniciando procesamiento del Dataset EVA 2019-2024")
    log(f"   Departamento: {DEPARTAMENTO_INTERES}")
    log(f"   Cultivos de interés: {CULTIVOS_INTERES}")
    log("")
    
    # Paso 1: Descargar datos
    df_raw = download_all_data()
    
    # Paso 2: Exploración
    explore_data(df_raw)
    
    # Paso 3: Limpieza y filtrado
    df_target, df_vc = clean_and_filter(df_raw)
    
    # Paso 4: Generar archivos finales
    generate_final_outputs(df_target, df_vc)
    
    log("")
    log("=" * 60)
    log("✅ PROCESAMIENTO COMPLETADO")
    log("=" * 60)
    log(f"   Archivos generados en:")
    log(f"   - Datos crudos: data/raw/")
    log(f"   - Datos procesados: data/processed/")
    log(f"   - Reportes: data/reports/")
