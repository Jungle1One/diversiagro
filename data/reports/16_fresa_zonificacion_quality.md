# Reporte de Calidad – Zonificación de Fresa (Procesado)

Fecha: 2026-07-08 18:40:23

## Resumen
- **Fuente**: UPRA – datos.gov.co (ID: emsg-94di)
- **Escala**: 1:100.000
- **Departamento**: Valle del Cauca
- **Polígonos procesados**: 3,491
- **Municipios**: 42

## Archivos Generados
| Archivo | Registros | Descripción |
|---------|-----------|-------------|
| zonificacion_fresa_valle_limpio.csv | 3,491 | Polígonos con aptitud y área |
| zonificacion_fresa_valle_municipio.csv | 42 | Resumen por municipio: % aptitud |

## Distribución de Aptitud (Valle del Cauca)
| Aptitud | Área (Ha) | % |
|---------|-----------|---|
| No apta | 1,099,905.5 | 53.0% |
| Exclusión legal | 891,451.7 | 42.9% |
| Aptitud alta | 37,253.5 | 1.8% |
| Aptitud media | 37,043.9 | 1.8% |
| Aptitud baja | 11,150.1 | 0.5% |
| **TOTAL** | **2,076,804.8** | **100%** |

## Ranking de Municipios por Aptitud
| Municipio | Índice Aptitud | Aptitud Dominante | Área Total (Ha) |
|-----------|---------------|-------------------|-----------------|
| Restrepo | 0.327 | Exclusion Legal | 13,585.9 |
| Tuluá | 0.196 | No Apta | 90,284.5 |
| Sevilla | 0.171 | No Apta | 53,936.7 |
| Caicedonia | 0.166 | No Apta | 16,711.2 |
| Trujillo | 0.147 | No Apta | 30,727.8 |
| Buga | 0.076 | No Apta | 82,180.5 |
| San Pedro | 0.075 | No Apta | 21,073.7 |
| El Águila | 0.066 | No Apta | 18,699.8 |
| Riofrío | 0.060 | No Apta | 30,731.1 |
| Toro | 0.059 | No Apta | 17,820.6 |
| Vijes | 0.049 | Exclusion Legal | 11,264.9 |
| Pradera | 0.046 | No Apta | 35,728.7 |
| Florida | 0.045 | No Apta | 40,387.3 |
| Alcalá | 0.045 | No Apta | 6,356.7 |
| El Cerrito | 0.044 | No Apta | 44,194.1 |
| Yotoco | 0.034 | No Apta | 32,752.8 |
| Ansermanuevo | 0.031 | No Apta | 30,432.3 |
| La Unión | 0.026 | No Apta | 12,009.5 |
| La Cumbre | 0.025 | Exclusion Legal | 25,479.7 |
| Bolívar | 0.018 | Exclusion Legal | 74,276.9 |
| Jamundí | 0.016 | No Apta | 62,317.9 |
| Guacarí | 0.014 | No Apta | 16,319.2 |
| Roldanillo | 0.013 | No Apta | 23,522.7 |
| Yumbo | 0.012 | No Apta | 23,185.6 |
| Bugalagrande | 0.011 | No Apta | 39,610.2 |
| Palmira | 0.010 | No Apta | 100,446.9 |
| Ginebra | 0.008 | Exclusion Legal | 26,795.0 |
| Dagua | 0.006 | Exclusion Legal | 91,941.6 |
| Ulloa | 0.004 | No Apta | 4,236.2 |
| Cali | 0.004 | Exclusion Legal | 56,741.7 |
| Andalucía | 0.002 | No Apta | 11,103.7 |
| Argelia | 0.002 | Exclusion Legal | 9,044.1 |
| Calima (El Darién) | 0.002 | Exclusion Legal | 79,808.4 |
| El Cairo | 0.001 | Exclusion Legal | 21,233.2 |
| Obando | 0.001 | No Apta | 21,479.2 |
| Buenaventura | 0.000 | Exclusion Legal | 639,186.4 |
| Cartago | 0.000 | No Apta | 24,741.8 |
| El Dovio | 0.000 | Exclusion Legal | 20,625.0 |
| La Victoria | 0.000 | No Apta | 26,498.3 |
| Candelaria | 0.000 | No Apta | 29,416.4 |
| Versalles | 0.000 | Exclusion Legal | 23,115.9 |
| Zarzal | 0.000 | No Apta | 36,800.7 |

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
- **Uso principal**: Predictor base de aptitud agroecológica para fresa
- **Variables derivadas**: % aptitud por municipio + índice de aptitud (0-1)
- **Cruce con EVA**: Por código municipio DANE