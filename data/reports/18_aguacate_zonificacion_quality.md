# Reporte de Calidad – Zonificación de Aguacate Hass (Procesado)

Fecha: 2026-07-08 18:40:48

## Resumen
- **Fuente**: UPRA – datos.gov.co (ID: tx7u-frn2)
- **Escala**: 1:100.000
- **Departamento**: Valle del Cauca
- **Polígonos procesados**: 3,792
- **Municipios**: 42

## Archivos Generados
| Archivo | Registros | Descripción |
|---------|-----------|-------------|
| zonificacion_aguacate_valle_limpio.csv | 3,792 | Polígonos con aptitud y área |
| zonificacion_aguacate_valle_municipio.csv | 42 | Resumen por municipio: % aptitud |

## Distribución de Aptitud (Valle del Cauca)
| Aptitud | Área (Ha) | % |
|---------|-----------|---|
| No apta | 1,089,738.6 | 52.5% |
| Exclusión legal | 891,451.7 | 42.9% |
| Aptitud media | 44,299.6 | 2.1% |
| Aptitud alta | 41,731.2 | 2.0% |
| Aptitud baja | 9,583.7 | 0.5% |
| **TOTAL** | **2,076,804.8** | **100%** |

## Ranking de Municipios por Aptitud
| Municipio | Índice Aptitud | Aptitud Dominante | Área Total (Ha) |
|-----------|---------------|-------------------|-----------------|
| Restrepo | 0.390 | Exclusion Legal | 13,585.9 |
| Caicedonia | 0.241 | No Apta | 16,711.2 |
| Sevilla | 0.185 | No Apta | 53,936.7 |
| Tuluá | 0.155 | No Apta | 90,284.5 |
| El Águila | 0.144 | No Apta | 18,699.8 |
| Riofrío | 0.120 | No Apta | 30,731.1 |
| Florida | 0.119 | No Apta | 40,387.3 |
| Pradera | 0.104 | No Apta | 35,728.7 |
| San Pedro | 0.087 | No Apta | 21,073.7 |
| Trujillo | 0.075 | No Apta | 30,727.8 |
| Buga | 0.070 | No Apta | 82,180.5 |
| Alcalá | 0.061 | No Apta | 6,356.7 |
| Vijes | 0.059 | Exclusion Legal | 11,264.9 |
| Ansermanuevo | 0.056 | No Apta | 30,432.3 |
| El Cerrito | 0.049 | No Apta | 44,194.1 |
| Toro | 0.043 | No Apta | 17,820.6 |
| Yotoco | 0.037 | No Apta | 32,752.8 |
| La Cumbre | 0.031 | Exclusion Legal | 25,479.7 |
| La Unión | 0.030 | No Apta | 12,009.5 |
| Bugalagrande | 0.026 | No Apta | 39,610.2 |
| Guacarí | 0.025 | No Apta | 16,319.2 |
| Palmira | 0.020 | No Apta | 100,446.9 |
| Jamundí | 0.020 | No Apta | 62,317.9 |
| Bolívar | 0.015 | Exclusion Legal | 74,276.9 |
| Roldanillo | 0.015 | No Apta | 23,522.7 |
| Dagua | 0.011 | Exclusion Legal | 91,941.6 |
| Yumbo | 0.008 | No Apta | 23,185.6 |
| Ginebra | 0.008 | Exclusion Legal | 26,795.0 |
| Ulloa | 0.006 | No Apta | 4,236.2 |
| Andalucía | 0.005 | No Apta | 11,103.7 |
| Cali | 0.004 | Exclusion Legal | 56,741.7 |
| Argelia | 0.003 | Exclusion Legal | 9,044.1 |
| Versalles | 0.003 | Exclusion Legal | 23,115.9 |
| Calima (El Darién) | 0.003 | Exclusion Legal | 79,808.4 |
| Obando | 0.003 | No Apta | 21,479.2 |
| El Cairo | 0.002 | Exclusion Legal | 21,233.2 |
| El Dovio | 0.002 | Exclusion Legal | 20,625.0 |
| Buenaventura | 0.000 | Exclusion Legal | 639,186.4 |
| La Victoria | 0.000 | No Apta | 26,498.3 |
| Candelaria | 0.000 | No Apta | 29,416.4 |
| Cartago | 0.000 | No Apta | 24,741.8 |
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
- **Uso principal**: Predictor base de aptitud agroecológica para aguacate Hass
- **Variables derivadas**: % aptitud por municipio + índice de aptitud (0-1)
- **Cruce con EVA**: Por código municipio DANE