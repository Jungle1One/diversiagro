# 🧠 Estructura de Modelos de Machine Learning

Los archivos `.pkl` de los modelos entrenados han sido excluidos de Git mediante `.gitignore` debido a su gran tamaño (Total ~130 MB). Subirlos al repositorio haría que clonarlo fuera lento e ineficiente.

## Estructura de este directorio:

```text
models/
├── README.md
├── modelo_aguacate_rf.pkl          
├── modelo_aguacate_kriging.pkl     
├── modelo_cacao_rf.pkl             
├── modelo_cacao_kriging.pkl        
├── modelo_cafe_rf.pkl              
├── modelo_cafe_kriging.pkl         
├── modelo_cana_panelera_rf.pkl     
├── modelo_cana_panelera_kriging.pkl
├── modelo_fresa_rf.pkl             
└── modelo_fresa_kriging.pkl        
```

## 🔗 Enlaces de Descarga Externos

Para que la aplicación funcione en tu entorno local o de producción, debes descargar los modelos pre-entrenados y ubicarlos en esta misma carpeta.

*   📥 [https://drive.google.com/drive/folders/15x0qaQHqCcbIV6GuPG4pRjVPa2LsrECY?usp=sharing](#)

> **Nota para el desarrollador:** Si ejecutas `python src/train.py`, estos archivos se generarán automáticamente en tu máquina local. No necesitas descargarlos si decides reentrenar.
