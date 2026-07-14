# Reporte de Calidad - Dataset EVA (Procesado)

Fecha: 2026-07-07 21:10:13

## Resumen de Procesamiento
- **Fuente**: datos.gov.co – EVA 2019-2024 (ID: uejq-wxrr)
- **Departamento**: Valle del Cauca (código 76)
- **Registros Valle del Cauca (todos los cultivos)**: 9,032
- **Registros cultivos de interés (limpio)**: 1,804

## Columnas del Dataset Final
| Columna | Tipo | No Nulos | % Completo |
|---------|------|----------|------------|
| :id | str | 1,804 | 100.0% |
| :version | str | 1,804 | 100.0% |
| :created_at | str | 1,804 | 100.0% |
| :updated_at | str | 1,804 | 100.0% |
| codigo_departamento | str | 1,804 | 100.0% |
| departamento | str | 1,804 | 100.0% |
| codigo_municipio | str | 1,804 | 100.0% |
| municipio | str | 1,804 | 100.0% |
| grupo_cultivo | str | 1,804 | 100.0% |
| subgrupo | str | 1,804 | 100.0% |
| cultivo | str | 1,804 | 100.0% |
| desagregacion_cultivo | str | 1,804 | 100.0% |
| anio | int64 | 1,804 | 100.0% |
| periodo | str | 1,804 | 100.0% |
| area_sembrada_ha | float64 | 1,804 | 100.0% |
| area_cosechada_ha | float64 | 1,804 | 100.0% |
| produccion_ton | float64 | 1,804 | 100.0% |
| rendimiento_ton_ha | float64 | 1,804 | 100.0% |
| ciclo_cultivo | str | 1,804 | 100.0% |
| estado_fisico | str | 1,804 | 100.0% |
| codigo_cultivo | int64 | 1,804 | 100.0% |
| nombre_cientifico | str | 1,804 | 100.0% |

## Distribución por Cultivo
| Cultivo | Registros | Municipios | Años |
|---------|-----------|------------|------|
| Café | 234 | 39 | 2019-2024 |
| Plátano | 242 | 41 | 2019-2024 |
| Caña | 372 | 40 | 2019-2024 |
| Cacao | 202 | 35 | 2019-2024 |
| Papaya | 139 | 23 | 2019-2024 |
| Fresa | 47 | 11 | 2019-2024 |
| Aguacate | 343 | 39 | 2019-2024 |
| Banano | 225 | 38 | 2019-2024 |

## Estadísticas por Cultivo

### Café
| Métrica | Área Sembrada (Ha) | Área Cosechada (Ha) | Producción (Ton) | Rendimiento (Ton/Ha) |
|---------|-------------------|--------------------|-----------------|--------------------|
| mean | 1,317.77 | 1,086.94 | 1,142.82 | 1.04 |
| std | 1,324.99 | 1,059.50 | 1,279.87 | 0.36 |
| min | 76.71 | 62.42 | 40.02 | 0.09 |
| 25% | 473.00 | 407.73 | 397.74 | 0.89 |
| 50% | 809.69 | 645.50 | 683.87 | 1.09 |
| 75% | 1,372.25 | 1,196.63 | 1,227.31 | 1.24 |
| max | 5,320.00 | 5,243.00 | 7,974.44 | 2.96 |

### Plátano
| Métrica | Área Sembrada (Ha) | Área Cosechada (Ha) | Producción (Ton) | Rendimiento (Ton/Ha) |
|---------|-------------------|--------------------|-----------------|--------------------|
| mean | 739.79 | 717.66 | 7,361.59 | 9.82 |
| std | 1,122.26 | 1,105.09 | 12,369.26 | 3.19 |
| min | 5.34 | 0.00 | 0.00 | 0.00 |
| 25% | 80.00 | 74.00 | 640.00 | 8.00 |
| 50% | 215.10 | 210.55 | 2,042.00 | 10.00 |
| 75% | 798.93 | 783.24 | 7,993.55 | 12.00 |
| max | 4,538.00 | 4,325.00 | 77,850.00 | 18.00 |

### Caña
| Métrica | Área Sembrada (Ha) | Área Cosechada (Ha) | Producción (Ton) | Rendimiento (Ton/Ha) |
|---------|-------------------|--------------------|-----------------|--------------------|
| mean | 3,512.23 | 3,320.31 | 400,308.34 | 82.95 |
| std | 6,389.08 | 6,107.49 | 791,109.90 | 39.65 |
| min | 1.50 | 0.00 | 0.00 | 0.00 |
| 25% | 65.88 | 60.00 | 3,000.00 | 50.00 |
| 50% | 345.00 | 345.00 | 21,192.00 | 80.00 |
| 75% | 4,230.27 | 4,183.09 | 465,000.00 | 120.00 |
| max | 33,990.00 | 33,900.00 | 4,776,340.50 | 160.00 |

### Cacao
| Métrica | Área Sembrada (Ha) | Área Cosechada (Ha) | Producción (Ton) | Rendimiento (Ton/Ha) |
|---------|-------------------|--------------------|-----------------|--------------------|
| mean | 48.40 | 41.92 | 24.75 | 0.56 |
| std | 65.54 | 59.77 | 40.54 | 0.24 |
| min | 1.45 | 0.00 | 0.00 | 0.00 |
| 25% | 9.00 | 6.40 | 3.88 | 0.40 |
| 50% | 20.00 | 19.20 | 8.90 | 0.50 |
| 75% | 65.95 | 51.35 | 22.35 | 0.70 |
| max | 405.00 | 355.00 | 199.00 | 1.50 |

### Papaya
| Métrica | Área Sembrada (Ha) | Área Cosechada (Ha) | Producción (Ton) | Rendimiento (Ton/Ha) |
|---------|-------------------|--------------------|-----------------|--------------------|
| mean | 40.07 | 25.13 | 654.23 | 30.49 |
| std | 84.29 | 51.20 | 902.90 | 20.00 |
| min | 0.50 | 0.00 | 0.00 | 0.00 |
| 25% | 7.00 | 5.00 | 84.74 | 15.00 |
| 50% | 16.40 | 11.40 | 330.00 | 28.00 |
| 75% | 33.05 | 28.30 | 741.74 | 40.00 |
| max | 464.00 | 414.00 | 4,802.00 | 80.00 |

### Fresa
| Métrica | Área Sembrada (Ha) | Área Cosechada (Ha) | Producción (Ton) | Rendimiento (Ton/Ha) |
|---------|-------------------|--------------------|-----------------|--------------------|
| mean | 3.58 | 3.11 | 74.45 | 17.94 |
| std | 4.36 | 3.77 | 106.24 | 12.79 |
| min | 0.20 | 0.00 | 0.00 | 0.00 |
| 25% | 1.00 | 0.72 | 4.75 | 5.00 |
| 50% | 2.00 | 1.50 | 40.00 | 18.00 |
| 75% | 4.00 | 4.00 | 72.00 | 30.00 |
| max | 19.50 | 15.50 | 434.00 | 43.33 |

### Aguacate
| Métrica | Área Sembrada (Ha) | Área Cosechada (Ha) | Producción (Ton) | Rendimiento (Ton/Ha) |
|---------|-------------------|--------------------|-----------------|--------------------|
| mean | 191.02 | 145.90 | 1,408.02 | 9.63 |
| std | 542.37 | 431.06 | 3,698.08 | 4.40 |
| min | 0.18 | 0.00 | 0.00 | 0.00 |
| 25% | 25.40 | 15.04 | 126.00 | 7.00 |
| 50% | 55.00 | 42.50 | 360.00 | 9.00 |
| 75% | 130.50 | 104.50 | 1,100.00 | 11.00 |
| max | 4,329.00 | 4,231.00 | 33,848.00 | 23.50 |

### Banano
| Métrica | Área Sembrada (Ha) | Área Cosechada (Ha) | Producción (Ton) | Rendimiento (Ton/Ha) |
|---------|-------------------|--------------------|-----------------|--------------------|
| mean | 194.81 | 180.59 | 2,166.57 | 12.46 |
| std | 254.02 | 241.35 | 3,497.78 | 5.87 |
| min | 2.00 | 0.00 | 0.00 | 0.00 |
| 25% | 30.00 | 27.00 | 240.00 | 8.00 |
| 50% | 90.00 | 81.00 | 982.00 | 11.49 |
| 75% | 232.00 | 213.88 | 2,760.00 | 16.00 |
| max | 1,314.00 | 1,124.00 | 24,728.00 | 42.00 |

## Distribución por Municipio y Cultivo (Valle del Cauca)

| Municipio | Aguacate | Banano | Cacao | Café | Caña | Fresa | Papaya | Plátano |
|-----------|---|---|---|---|---|---|---|---|
| Alcalá | 16 | 6 | 6 | 6 | 0 | 0 | 7 | 6 |
| Andalucía | 6 | 6 | 6 | 6 | 6 | 0 | 11 | 6 |
| Ansermanuevo | 16 | 6 | 6 | 6 | 12 | 0 | 0 | 6 |
| Argelia | 16 | 6 | 6 | 6 | 6 | 0 | 0 | 6 |
| Bolívar | 6 | 6 | 6 | 6 | 12 | 0 | 6 | 6 |
| Buenaventura | 0 | 6 | 6 | 0 | 6 | 0 | 0 | 6 |
| Bugalagrande | 16 | 0 | 6 | 6 | 12 | 0 | 0 | 6 |
| Caicedonia | 16 | 6 | 6 | 6 | 7 | 0 | 0 | 6 |
| Calima | 16 | 5 | 5 | 6 | 6 | 0 | 0 | 6 |
| Candelaria | 0 | 0 | 6 | 0 | 12 | 0 | 0 | 6 |
| Cartago | 6 | 6 | 6 | 6 | 12 | 0 | 0 | 6 |
| Dagua | 6 | 6 | 6 | 6 | 6 | 0 | 0 | 6 |
| El Cairo | 16 | 6 | 0 | 6 | 6 | 2 | 0 | 6 |
| El Cerrito | 6 | 6 | 0 | 6 | 6 | 6 | 0 | 0 |
| El Dovio | 11 | 6 | 6 | 6 | 6 | 0 | 0 | 6 |
| El Águila | 11 | 6 | 6 | 6 | 6 | 6 | 0 | 6 |
| Florida | 6 | 6 | 6 | 6 | 6 | 6 | 6 | 6 |
| Ginebra | 5 | 6 | 0 | 6 | 12 | 0 | 6 | 6 |
| Guacarí | 6 | 6 | 6 | 6 | 12 | 0 | 6 | 6 |
| Guadalajara de Buga | 6 | 6 | 6 | 6 | 12 | 6 | 1 | 6 |
| Jamundí | 6 | 6 | 6 | 6 | 12 | 0 | 6 | 6 |
| La Cumbre | 5 | 6 | 0 | 6 | 6 | 0 | 6 | 6 |
| La Unión | 6 | 6 | 6 | 6 | 6 | 0 | 6 | 6 |
| La Victoria | 6 | 6 | 6 | 6 | 12 | 0 | 6 | 6 |
| Obando | 6 | 6 | 1 | 6 | 12 | 0 | 6 | 6 |
| Palmira | 6 | 6 | 5 | 6 | 12 | 1 | 0 | 6 |
| Pradera | 6 | 6 | 6 | 6 | 11 | 0 | 0 | 6 |
| Restrepo | 16 | 6 | 0 | 6 | 6 | 0 | 0 | 3 |
| Riofrío | 6 | 6 | 6 | 6 | 12 | 0 | 0 | 6 |
| Roldanillo | 6 | 6 | 6 | 6 | 12 | 6 | 7 | 6 |
| San Pedro | 6 | 6 | 5 | 6 | 12 | 0 | 6 | 5 |
| Santiago de Cali | 6 | 0 | 0 | 6 | 6 | 0 | 0 | 6 |
| Sevilla | 11 | 6 | 6 | 6 | 12 | 5 | 5 | 6 |
| Toro | 6 | 6 | 6 | 6 | 6 | 0 | 7 | 6 |
| Trujillo | 12 | 6 | 6 | 6 | 12 | 0 | 6 | 6 |
| Tuluá | 6 | 6 | 6 | 6 | 12 | 6 | 6 | 6 |
| Ulloa | 6 | 6 | 6 | 6 | 0 | 0 | 4 | 6 |
| Versalles | 11 | 6 | 6 | 6 | 6 | 2 | 0 | 6 |
| Vijes | 6 | 6 | 0 | 6 | 6 | 0 | 6 | 6 |
| Yotoco | 11 | 0 | 6 | 6 | 12 | 0 | 6 | 6 |
| Yumbo | 6 | 6 | 6 | 6 | 12 | 1 | 11 | 6 |
| Zarzal | 0 | 4 | 6 | 0 | 12 | 0 | 2 | 6 |

## Evaluación de Utilidad para el Modelo RFRK

### ✅ Fortalezas
- Datos de rendimiento (variable objetivo) disponibles 2019-2024
- Cobertura municipal completa del Valle del Cauca
- Los 4 cultivos de interés están presentes
- Datos semestrales para cultivos transitorios

### ⚠️ Limitaciones
- Resolución a nivel municipal (no vereda)
- Algunos registros tienen rendimiento 0 o área cosechada 0
- Es información subjetiva (no medida con instrumentos)

### 🎯 Conclusión
- **¿Es útil para el proyecto?**: ✅ SÍ
- **Uso principal**: Variable objetivo (rendimiento Ton/Ha) para entrenar el modelo RFRK
- **Nivel de resolución**: Municipal (suficiente para prototipo)