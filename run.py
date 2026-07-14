import subprocess
import time
import sys
import webbrowser

def main():
    print("=====================================")
    print("Iniciando infraestructura desacoplada DiversIAgro...")
    print("=====================================")
    
    # Arrancar FastAPI en segundo plano
    api_process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "src.backend.main:app", "--host", "127.0.0.1", "--port", "8000"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Darle un par de segundos a la API para cargar los modelos pesados
    time.sleep(3)
    
    # Comprobar si falló rápido
    if api_process.poll() is not None:
        print("Error al iniciar FastAPI. Logs:")
        print(api_process.stderr.read().decode())
        sys.exit(1)
        
    print("EXITO: Backend operativo en http://127.0.0.1:8000")
    print("2. Arrancando Frontend (Streamlit)...")
    
    # Arrancar Streamlit
    streamlit_process = subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", "src/frontend/app.py", "--server.port", "8501", "--server.headless", "true"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    time.sleep(3)
    if streamlit_process.poll() is not None:
        print("Error al iniciar Streamlit. Logs:")
        print(streamlit_process.stderr.read().decode())
        api_process.terminate()
        sys.exit(1)
        
    print("EXITO: Frontend operativo en http://localhost:8501")
    print("Abriendo el navegador...")
    webbrowser.open("http://localhost:8501")
    
    print("\n" + "="*50)
    print("SERVICIOS EN EJECUCIÓN (Presiona Ctrl+C para detener ambos)")
    print("="*50)
    
    try:
        # Mantener el script vivo
        api_process.wait()
        streamlit_process.wait()
    except KeyboardInterrupt:
        print("\nApagando infraestructura...")
        api_process.terminate()
        streamlit_process.terminate()
        print("Sistemas detenidos. ¡Hasta pronto!")

if __name__ == "__main__":
    main()
