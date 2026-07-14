import os
import shutil
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = BASE_DIR / 'scripts'
SRC_DIR = BASE_DIR / 'src'

# Mapeo de origen -> destino (relativo a BASE_DIR)
MAPPING = {
    # Ingestión de Datos -> data_pipeline
    '01_download_eva.py': 'src/data_pipeline/01_download_eva.py',
    '02_download_ideam.py': 'src/data_pipeline/02_download_ideam.py',
    '03_download_zonificacion_cafe.py': 'src/data_pipeline/03_download_zonificacion_cafe.py',
    '04_download_zonificacion_cacao.py': 'src/data_pipeline/04_download_zonificacion_cacao.py',
    '05_download_zonificacion_banano.py': 'src/data_pipeline/05_download_zonificacion_banano.py',
    '06_download_zonificacion_cana_panelera.py': 'src/data_pipeline/06_download_zonificacion_cana_panelera.py',
    '07_download_zonificacion_papaya.py': 'src/data_pipeline/07_download_zonificacion_papaya.py',
    '08_download_zonificacion_fresa.py': 'src/data_pipeline/08_download_zonificacion_fresa.py',
    '09_download_zonificacion_aguacate.py': 'src/data_pipeline/09_download_zonificacion_aguacate.py',
    '10_download_limites_admin.py': 'src/data_pipeline/10_download_limites_admin.py',
    '10_download_mmra_dane.py': 'src/data_pipeline/10_download_mmra_dane.py',
    'run_all_zonificaciones.py': 'src/data_pipeline/run_all_zonificaciones.py',
    
    # Transformación -> data_pipeline
    '11_extract_dem_zonificaciones.py': 'src/data_pipeline/11_extract_dem_zonificaciones.py',
    'fix_ideam_precipitacion.py': 'src/data_pipeline/fix_ideam_precipitacion.py',
    'fix_eva_notebook.py': 'src/data_pipeline/fix_eva_notebook.py',
    'update_eva_notebook.py': 'src/data_pipeline/update_eva_notebook.py',
    
    # Feature Engineering -> features
    '13_consolidate_training_data.py': 'src/features/13_consolidate_training_data.py',
    
    # Entrenamiento -> src/train.py
    '14_train_rfrk.py': 'src/train.py',
    
    # Inferencia/Testeo -> src/inference.py
    '15_test_models.py': 'src/inference.py'
}

def update_paths_in_file(filepath, levels_deep):
    """
    Actualiza la constante BASE_DIR en los scripts para que los paths sigan funcionando.
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Si estaba a 1 nivel (scripts/x.py) tenía .parent.parent
    # Si ahora está a 2 niveles (src/data_pipeline/x.py), necesita .parent.parent.parent
    if levels_deep == 2:
        content = content.replace(
            "BASE_DIR = Path(__file__).resolve().parent.parent",
            "BASE_DIR = Path(__file__).resolve().parent.parent.parent"
        )
    elif levels_deep == 1:
        # Se queda igual, pero por si acaso lo reescribimos
        pass

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    print("Iniciando reorganización de scripts...")
    
    for src_name, dest_rel_path in MAPPING.items():
        src_path = SCRIPTS_DIR / src_name
        dest_path = BASE_DIR / dest_rel_path
        
        if not src_path.exists():
            print(f"⚠️ {src_name} no existe, saltando.")
            continue
            
        print(f"Moviendo {src_name} -> {dest_rel_path}")
        
        # Asegurar directorio de destino
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Mover archivo
        shutil.move(str(src_path), str(dest_path))
        
        # Calcular profundidad (cuántos directorios hay desde root)
        # ej: src/train.py -> 1 carpeta (src)
        # ej: src/data_pipeline/x.py -> 2 carpetas (src, data_pipeline)
        # len(dest_path.parts) - len(BASE_DIR.parts) - 1
        levels = len(dest_path.relative_to(BASE_DIR).parts) - 1
        
        update_paths_in_file(dest_path, levels)
        
    print("\n¡Scripts movidos y actualizados exitosamente!")
    
    # Eliminar scripts/ si está vacía
    if SCRIPTS_DIR.exists() and not any(SCRIPTS_DIR.iterdir()):
        SCRIPTS_DIR.rmdir()
        print("Directorio scripts/ original eliminado por estar vacío.")

if __name__ == "__main__":
    main()
