# Reporte de Calidad – Zonificación de Cacao (Procesado)

Fecha: 2026-07-08 18:39:14

## Resumen
- **Fuente**: UPRA – datos.gov.co (ID: jdjx-qer4)
- **Escala**: 1:100.000
- **Departamento**: Valle del Cauca
- **Polígonos procesados**: 5,176
- **Municipios**: 42

## Archivos Generados
| Archivo | Registros | Descripción |
|---------|-----------|-------------|
| zonificacion_cacao_valle_limpio.csv | 5,176 | Polígonos con aptitud y área |
| zonificacion_cacao_valle_municipio.csv | 42 | Resumen por municipio: % aptitud |

## Distribución de Aptitud (Valle del Cauca)
| Aptitud | Área (Ha) | % |
|---------|-----------|---|
| Exclusión legal | 891,451.7 | 42.9% |
| No apta | 861,674.7 | 41.5% |
| Aptitud alta | 200,849.9 | 9.7% |
| Aptitud media | 96,978.5 | 4.7% |
| Aptitud baja | 25,850.0 | 1.2% |
| **TOTAL** | **2,076,804.8** | **100%** |

## Ranking de Municipios por Aptitud
| Municipio | Índice Aptitud | Aptitud Dominante | Área Total (Ha) |
|-----------|---------------|-------------------|-----------------|
| Candelaria | 0.746 | Aptitud Alta | 29,416.4 |
| Guacarí | 0.539 | Aptitud Alta | 16,319.2 |
| Caicedonia | 0.451 | No Apta | 16,711.2 |
| Alcalá | 0.437 | Aptitud Media | 6,356.7 |
| Jamundí | 0.376 | Aptitud Alta | 62,317.9 |
| Bugalagrande | 0.358 | No Apta | 39,610.2 |
| Palmira | 0.336 | Exclusion Legal | 100,446.9 |
| El Cerrito | 0.334 | Exclusion Legal | 44,194.1 |
| Pradera | 0.328 | No Apta | 35,728.7 |
| Cartago | 0.303 | No Apta | 24,741.8 |
| Andalucía | 0.294 | No Apta | 11,103.7 |
| San Pedro | 0.279 | No Apta | 21,073.7 |
| Sevilla | 0.276 | No Apta | 53,936.7 |
| La Victoria | 0.272 | No Apta | 26,498.3 |
| Florida | 0.263 | No Apta | 40,387.3 |
| Ulloa | 0.244 | No Apta | 4,236.2 |
| Ginebra | 0.244 | Exclusion Legal | 26,795.0 |
| Trujillo | 0.206 | No Apta | 30,727.8 |
| La Cumbre | 0.173 | Exclusion Legal | 25,479.7 |
| Ansermanuevo | 0.162 | No Apta | 30,432.3 |
| Cali | 0.158 | Exclusion Legal | 56,741.7 |
| Toro | 0.158 | No Apta | 17,820.6 |
| Riofrío | 0.152 | No Apta | 30,731.1 |
| Tuluá | 0.149 | No Apta | 90,284.5 |
| Buga | 0.149 | No Apta | 82,180.5 |
| El Águila | 0.116 | No Apta | 18,699.8 |
| Obando | 0.113 | No Apta | 21,479.2 |
| Zarzal | 0.089 | No Apta | 36,800.7 |
| La Unión | 0.076 | No Apta | 12,009.5 |
| Yotoco | 0.073 | No Apta | 32,752.8 |
| Roldanillo | 0.052 | No Apta | 23,522.7 |
| Yumbo | 0.050 | No Apta | 23,185.6 |
| Vijes | 0.045 | Exclusion Legal | 11,264.9 |
| Dagua | 0.033 | Exclusion Legal | 91,941.6 |
| Bolívar | 0.024 | Exclusion Legal | 74,276.9 |
| Restrepo | 0.010 | No Apta | 13,585.9 |
| El Dovio | 0.003 | Exclusion Legal | 20,625.0 |
| Argelia | 0.002 | Exclusion Legal | 9,044.1 |
| Buenaventura | 0.002 | Exclusion Legal | 639,186.4 |
| El Cairo | 0.002 | Exclusion Legal | 21,233.2 |
| Versalles | 0.002 | Exclusion Legal | 23,115.9 |
| Calima (El Darién) | 0.000 | Exclusion Legal | 79,808.4 |

## Evaluación de Utilidad para el Modelo RFRK

### ✅ Fortalezas
- Clasificación oficial de aptitud a escala 1:100.000
- Cubre los municipios del Valle del Cauca
- Incluye área (Ha) por polígono → permite cálculos de superficie
- El índice de aptitud calculado es directamente usable como feature

### ⚠️ Limitaciones
- Datos estáticos (no cambian en el tiempo)
- Geometrías excluidas de la descarga tabular

### 🎯 Conclusión
- **¿Es útil?**: ✅ SÍ
- **Uso principal**: Predictor base de aptitud agroecológica para cacao
- **Variables derivadas**: % aptitud por municipio + índice de aptitud (0-1)
- **Cruce con EVA**: Por código municipio DANE