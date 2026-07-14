# Reporte de Calidad – Zonificación de Café (Procesado)

Fecha: 2026-07-08 18:38:45

## Resumen
- **Fuente**: UPRA – datos.gov.co (ID: kwvf-nwea)
- **Escala**: 1:100.000
- **Departamento**: Valle del Cauca
- **Polígonos procesados**: 15,980
- **Municipios**: 42

## Archivos Generados
| Archivo | Registros | Descripción |
|---------|-----------|-------------|
| zonificacion_cafe_valle_limpio.csv | 15,980 | Polígonos con aptitud y área |
| zonificacion_cafe_valle_municipio.csv | 42 | Resumen por municipio: % aptitud |

## Distribución de Aptitud (Valle del Cauca)
| Aptitud | Área (Ha) | % |
|---------|-----------|---|
| Exclusión legal | 901,089.3 | 43.4% |
| No apta | 732,195.1 | 35.3% |
| Aptitud alta | 195,482.2 | 9.4% |
| Aptitud media | 146,465.3 | 7.1% |
| Aptitud baja | 101,572.9 | 4.9% |
| **TOTAL** | **2,076,804.8** | **100%** |

## Ranking de Municipios por Aptitud
| Municipio | Índice Aptitud | Aptitud Dominante | Área Total (Ha) |
|-----------|---------------|-------------------|-----------------|
| Alcalá | 0.876 | Aptitud Alta | 6,356.7 |
| Ulloa | 0.823 | Aptitud Alta | 4,236.2 |
| Caicedonia | 0.780 | Aptitud Alta | 16,711.2 |
| El Águila | 0.561 | Aptitud Alta | 18,699.8 |
| Ansermanuevo | 0.536 | Aptitud Alta | 30,432.3 |
| Restrepo | 0.515 | Aptitud Alta | 13,585.9 |
| Trujillo | 0.501 | Aptitud Alta | 30,727.8 |
| Riofrío | 0.451 | Aptitud Alta | 30,731.1 |
| Sevilla | 0.390 | No Apta | 53,936.7 |
| Bugalagrande | 0.371 | No Apta | 39,610.2 |
| Toro | 0.368 | No Apta | 17,820.6 |
| San Pedro | 0.350 | No Apta | 21,073.7 |
| Florida | 0.346 | No Apta | 40,387.3 |
| Pradera | 0.323 | Aptitud Media | 35,728.7 |
| Obando | 0.323 | No Apta | 21,479.2 |
| La Unión | 0.322 | No Apta | 12,009.5 |
| La Victoria | 0.309 | No Apta | 26,498.3 |
| Guacarí | 0.304 | No Apta | 16,319.2 |
| Jamundí | 0.277 | No Apta | 62,317.9 |
| Yumbo | 0.273 | Exclusion Legal | 23,185.6 |
| Cartago | 0.260 | No Apta | 24,741.8 |
| Vijes | 0.260 | Exclusion Legal | 11,264.9 |
| Ginebra | 0.251 | Exclusion Legal | 26,795.0 |
| La Cumbre | 0.243 | Exclusion Legal | 25,479.7 |
| Andalucía | 0.235 | No Apta | 11,103.7 |
| El Cerrito | 0.230 | Exclusion Legal | 44,194.1 |
| Yotoco | 0.226 | No Apta | 32,752.8 |
| Tuluá | 0.215 | No Apta | 90,284.5 |
| Palmira | 0.183 | Exclusion Legal | 100,446.9 |
| Roldanillo | 0.178 | No Apta | 23,522.7 |
| Candelaria | 0.173 | No Apta | 29,416.4 |
| Zarzal | 0.149 | No Apta | 36,800.7 |
| Buga | 0.116 | No Apta | 82,180.5 |
| Cali | 0.083 | Exclusion Legal | 56,741.7 |
| Bolívar | 0.073 | Exclusion Legal | 74,276.9 |
| Dagua | 0.036 | Exclusion Legal | 91,941.6 |
| Argelia | 0.014 | Exclusion Legal | 9,044.1 |
| El Dovio | 0.013 | Exclusion Legal | 20,625.0 |
| Versalles | 0.013 | Exclusion Legal | 23,115.9 |
| El Cairo | 0.008 | Exclusion Legal | 21,233.2 |
| Calima (El Darién) | 0.002 | Exclusion Legal | 79,808.4 |
| Buenaventura | 0.000 | Exclusion Legal | 639,186.4 |

## Evaluación de Utilidad para el Modelo RFRK

### ✅ Fortalezas
- Clasificación oficial de aptitud a escala 1:100.000
- Cubre todos los municipios del Valle del Cauca
- Incluye área (Ha) por polígono → permite cálculos de superficie
- El índice de aptitud calculado es directamente usable como feature

### ⚠️ Limitaciones
- Datos estáticos (no cambian en el tiempo)
- No incluye variables biofísicas detalladas (temperatura, altitud específica)
- Geometrías excluidas de la descarga tabular

### 🎯 Conclusión
- **¿Es útil?**: ✅ SÍ
- **Uso principal**: Predictor base de aptitud agroecológica para café
- **Variables derivadas**: % aptitud por municipio + índice de aptitud (0-1)
- **Cruce con EVA**: Por código municipio DANE