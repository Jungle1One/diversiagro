# Reporte de Calidad – Precipitación IDEAM (Procesado)

Fecha: 2026-07-07 21:46:43

## Resumen de Procesamiento
- **Fuente**: IDEAM – datos.gov.co (ID: s54a-sgyg)
- **Departamento**: Valle del Cauca
- **Estaciones**: 33
- **Municipios con datos**: 19

## Archivos Generados
| Archivo | Registros | Descripción |
|---------|-----------|-------------|
| ideam_precipitacion_mensual_estacion.csv | 232 | Precipitación mensual acumulada por estación |
| ideam_precipitacion_mensual_municipio.csv | 142 | Precipitación mensual promedio por municipio |
| ideam_precipitacion_anual_municipio.csv | 19 | Precipitación anual por municipio |
| ideam_catalogo_estaciones_valle.csv | 33 | Catálogo de estaciones meteorológicas |

## Cobertura Temporal por Municipio
| Municipio | Años | Estaciones |
|-----------|------|------------|
| ALCALÁ | 2019-2019 | 1 |
| ANSERMANUEVO | 2019-2019 | 1 |
| ARGELIA | 2019-2019 | 1 |
| BUENAVENTURA | 2019-2019 | 5 |
| BUGA | 2019-2019 | 4 |
| BUGALAGRANDE | 2019-2019 | 1 |
| CAICEDONIA | 2019-2019 | 2 |
| CALI | 2019-2019 | 5 |
| CARTAGO | 2019-2019 | 1 |
| DAGUA | 2019-2019 | 1 |
| FLORIDA | 2019-2019 | 1 |
| JAMUNDÍ | 2019-2019 | 3 |
| LA CUMBRE | 2019-2019 | 1 |
| PALMIRA | 2019-2019 | 1 |
| RESTREPO | 2019-2019 | 1 |
| RIOFRÍO | 2019-2019 | 1 |
| SEVILLA | 2019-2019 | 1 |
| TRUJILLO | 2019-2019 | 1 |
| TULUÁ | 2019-2019 | 1 |

## Estadísticas de Precipitación Anual (mm)
- count: 19.0
- mean: 20,077.0
- std: 85,398.9
- min: 30.8
- 25%: 282.9
- 50%: 525.1
- 75%: 779.9
- max: 372,728.2

## Evaluación de Utilidad para el Modelo RFRK

### ✅ Fortalezas
- Datos de alta resolución temporal (cada 10 min) agregados a mensual/anual
- Coordenadas GPS de cada estación (útil para Kriging espacial)
- Múltiples estaciones por municipio (mejor cobertura)

### ⚠️ Limitaciones
- Datos crudos NO validados por IDEAM (control de calidad básico)
- No todos los municipios del Valle tienen estaciones
- Posibles gaps temporales en algunas estaciones

### 🎯 Conclusión
- **¿Es útil para el proyecto?**: ✅ SÍ
- **Uso principal**: Predictor climático (precipitación) para el modelo RFRK
- **Cruce con EVA**: Por municipio y año