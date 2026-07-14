import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
RAW_FILE = BASE_DIR / 'data' / 'raw' / 'ideam_precipitacion_valle_raw.csv'
OUT_FILE = BASE_DIR / 'data' / 'processed' / 'ideam_precipitacion_anual_municipio.csv'

def fix_municipio_name(name):
    if pd.isna(name): return name
    name = str(name).strip().upper()
    # Mapeo de errores de codificación conocidos en IDEAM
    mapeo = {
        'JAMUND': 'JAMUNDI',
        'TULU': 'TULUA',
        'ALCAL': 'ALCALA',
        'RIOFRO': 'RIOFRIO',
        'ANDALUCA': 'ANDALUCIA',
        'BUGALAGRANDE': 'BUGALAGRANDE',
        'ZARZAL': 'ZARZAL',
        'BOLVAR': 'BOLIVAR',
        'YUMBO': 'YUMBO',
        'GINEBRA': 'GINEBRA',
        'GUACAR': 'GUACARI',
        'EL DOVIO': 'EL DOVIO',
        'PRADERA': 'PRADERA',
        'FLORIDA': 'FLORIDA',
        'CANDELARIA': 'CANDELARIA',
        'EL CERRITO': 'EL CERRITO',
        'VIJES': 'VIJES',
        'YOTOCO': 'YOTOCO',
        'DARIN': 'DARIEN',
        'CALIMA': 'CALIMA',
        'SAN PEDRO': 'SAN PEDRO',
        'OBANDO': 'OBANDO',
        'LA UNIN': 'LA UNION',
        'EL GUILA': 'EL AGUILA',
        'LA VICTORIA': 'LA VICTORIA',
        'TORO': 'TORO',
        'ULLOA': 'ULLOA',
        'VERSALLES': 'VERSALLES',
        'CARTAGO': 'CARTAGO',
        'ANSERMANUEVO': 'ANSERMANUEVO',
        'ARGELIA': 'ARGELIA',
        'EL CAIRO': 'EL CAIRO',
        'LA CUMBRE': 'LA CUMBRE',
        'RESTREPO': 'RESTREPO',
        'DAGUA': 'DAGUA',
        'BUENAVENTURA': 'BUENAVENTURA',
        'CALI': 'CALI',
        'PALMIRA': 'PALMIRA',
        'BUGA': 'BUGA',
        'TRUJILLO': 'TRUJILLO',
        'CAICEDONIA': 'CAICEDONIA',
        'SEVILLA': 'SEVILLA'
    }
    # Mapear el carácter de reemplazo Unicode ()
    name = name.replace('\ufffd', '')
    # Pero para estar seguros usamos el diccionario para los comunes
    return mapeo.get(name, name)

def main():
    print(f"Cargando {RAW_FILE.name} (esto tomará unos segundos)...")
    df = pd.read_csv(RAW_FILE, usecols=['municipio', 'fechaobservacion', 'valorobservado', 'nombreestacion'])
    
    # Limpiar municipios
    df['municipio'] = df['municipio'].apply(fix_municipio_name)
    
    # Extraer año
    df['anio'] = df['fechaobservacion'].str[:4].astype(float)
    
    # Limpiar nulos
    df = df.dropna(subset=['municipio', 'anio', 'valorobservado'])
    df['valorobservado'] = pd.to_numeric(df['valorobservado'], errors='coerce')
    
    print("Agregando precipitacion anual por estación y año...")
    # Sumar la lluvia (mm) de todos los meses de un año para cada estación
    estacion_anual = df.groupby(['municipio', 'nombreestacion', 'anio'])['valorobservado'].sum().reset_index()
    
    # Promediar esos años para cada estación
    estacion_media = estacion_anual.groupby(['municipio', 'nombreestacion'])['valorobservado'].mean().reset_index()
    
    # Promediar las estaciones para obtener el valor del municipio
    muni_media = estacion_media.groupby('municipio')['valorobservado'].mean().reset_index()
    
    muni_media.rename(columns={'municipio': 'municipio', 'valorobservado': 'precipitacion_anual_mm'}, inplace=True)
    
    # Redondear
    muni_media['precipitacion_anual_mm'] = muni_media['precipitacion_anual_mm'].round(1)
    
    print("\nMuestra de resultados corregidos:")
    print(muni_media.head())
    print("\nMedia de Buenaventura:", muni_media[muni_media['municipio'] == 'BUENAVENTURA']['precipitacion_anual_mm'].values[0])
    
    muni_media.to_csv(OUT_FILE, index=False)
    print(f"\n✅ Archivo corregido guardado en: {OUT_FILE}")

if __name__ == "__main__":
    main()
