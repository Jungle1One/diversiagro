import os
from pathlib import Path

# Definimos la base del proyecto (asumiendo que este script corre dentro de scripts/)
BASE_DIR = Path(__file__).resolve().parent.parent

# Lista de directorios a crear
directories = [
    "RECURSOS",
    "docs/architecture",
    "data/raw",
    "data/processed",
    "data/realtime",
    "data/external",
    "notebooks",
    "src/agents",
    "src/data_pipeline",
    "src/features",
    "models/predictive",
    "models/llm_rag",
    "models/simulation",
    "reports/figures",
    "tests/unit",
    "tests/integration",
    "tests/bias_tests",
    ".github/workflows",
    "config",
    "deployments/docker",
    "deployments/kubernetes",
    "deployments/serverless"
]

# Lista de archivos a crear (si no existen)
files = [
    "RECURSOS/Presentacion.pptx",
    "RECURSOS/presentacion.pdf",
    "RECURSOS/portada.png",
    "README.md",
    "LICENSE",
    ".gitignore",
    "requirements.txt",
    "environment.yml",
    "Changelog.md",
    "docs/api_spec.md",
    "docs/public_impact_assessment.md",
    "docs/data_dictionary.md",
    "docs/planteamiento_problema.md",
    "docs/marco_metodologico.md",
    "docs/fuentes_datos.md",
    "docs/conclusiones.md",
    "docs/validación_guide.md",
    "notebooks/01_EDA_exploracion_datos.ipynb",
    "notebooks/02_limpieza_transformacion.ipynb",
    "notebooks/03_analisis_descriptivo.ipynb",
    "notebooks/04_modelo_predictivo.ipynb",
    "notebooks/05_reportes_automaticos.ipynb",
    "src/__init__.py",
    "src/agents/citizen_agent.py",
    "src/agents/analyst_agent.py",
    "src/data_pipeline/ingest.py",
    "src/data_pipeline/transform.py",
    "src/inference.py",
    "src/train.py",
    "reports/figures/distribuciones.png",
    "reports/figures/correlaciones.png",
    "reports/figures/matriz_confusion.png",
    "reports/reporte_final.pdf",
    ".github/workflows/ci-cd-pipeline.yml",
    ".github/workflows/data-update-cron.yml",
    ".github/CODEOWNERS",
    "config/base_config.yaml",
    "config/model_hyperparams.yaml",
    "config/security_policy.json",
    "deployments/docker/Dockerfile.api",
    "deployments/docker/Dockerfile.inference",
    "deployments/kubernetes/deployment.yaml",
    "deployments/kubernetes/hpa.yaml"
]

def create_structure():
    print(f"Directorio base del proyecto: {BASE_DIR}\n")
    
    print("1. Creando directorios...")
    for d in directories:
        dir_path = BASE_DIR / d
        if not dir_path.exists():
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"  [+] Directorio creado: {d}")
        else:
            print(f"  [=] Directorio ya existe: {d}")
            
    print("\n2. Creando archivos vacíos...")
    for f in files:
        file_path = BASE_DIR / f
        # Asegurarse de que el directorio padre del archivo exista
        file_path.parent.mkdir(parents=True, exist_ok=True)
        if not file_path.exists():
            file_path.touch(exist_ok=True)
            print(f"  [+] Archivo creado: {f}")
        else:
            print(f"  [=] Archivo ya existe: {f}")

    print("\n¡Estructura de repositorio generada exitosamente!")

if __name__ == "__main__":
    create_structure()
