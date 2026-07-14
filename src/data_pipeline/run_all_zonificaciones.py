import os
import subprocess
import time
from pathlib import Path

# Configuración
BASE_DIR = Path(__file__).resolve().parent
ZONIFICACION_SCRIPTS = [
    "03_download_zonificacion_cafe.py",
    "04_download_zonificacion_cacao.py",
    "05_download_zonificacion_banano.py",
    "06_download_zonificacion_cana_panelera.py",
    "07_download_zonificacion_papaya.py",
    "08_download_zonificacion_fresa.py",
    "09_download_zonificacion_aguacate.py"
]

def run_all():
    print("="*60)
    print("🚀 INICIANDO DESCARGA DE TODAS LAS ZONIFICACIONES (GEOMETRÍAS)")
    print("="*60)
    print(f"Total de scripts a ejecutar: {len(ZONIFICACION_SCRIPTS)}\n")

    start_time = time.time()
    successful = []
    failed = []

    for script in ZONIFICACION_SCRIPTS:
        script_path = BASE_DIR / script
        if not script_path.exists():
            print(f"❌ ARCHIVO NO ENCONTRADO: {script}")
            failed.append(script)
            continue

        print(f"\n▶️ Ejecutando: {script} ...")
        
        try:
            # Ejecutar el script usando el mismo intérprete de Python (.env-1)
            import sys
            result = subprocess.run(
                [sys.executable, str(script_path)],
                check=True,
                text=True,
                capture_output=False
            )
            print(f"✅ FINALIZADO CON ÉXITO: {script}")
            successful.append(script)
        except subprocess.CalledProcessError as e:
            print(f"\n❌ ERROR EJECUTANDO: {script}")
            print(f"  El proceso terminó con código de error {e.returncode}")
            failed.append(script)
        except Exception as e:
            print(f"\n❌ ERROR INESPERADO en {script}: {e}")
            failed.append(script)

    end_time = time.time()
    minutes = (end_time - start_time) / 60

    print("\n" + "="*60)
    print("📊 RESUMEN DE EJECUCIÓN")
    print("="*60)
    print(f"Tiempo total: {minutes:.2f} minutos")
    print(f"Scripts exitosos: {len(successful)}")
    print(f"Scripts fallidos: {len(failed)}")
    
    if failed:
        print("\nScripts que fallaron:")
        for f in failed:
            print(f" - {f}")
    
    if len(failed) == 0:
        print("\n¡Todos los archivos GeoJSON fueron generados correctamente!")
        print("Revisa la carpeta 'data/processed/' para los resultados.")

if __name__ == "__main__":
    run_all()
