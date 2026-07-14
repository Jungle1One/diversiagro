# Reporte de Calidad – Zonificación de Caña Panelera (Procesado)

Fecha: 2026-07-08 18:39:46

## Resumen
- **Fuente**: UPRA – datos.gov.co (ID: p9xp-sm4v)
- **Escala**: 1:100.000
- **Departamento**: Valle del Cauca
- **Polígonos procesados**: 5,080
- **Municipios**: 42

## Archivos Generados
| Archivo | Registros | Descripción |
|---------|-----------|-------------|
| zonificacion_cana_panelera_valle_limpio.csv | 5,080 | Polígonos con aptitud y área |
| zonificacion_cana_panelera_valle_municipio.csv | 42 | Resumen por municipio: % aptitud |

## Distribución de Aptitud (Valle del Cauca)
| Aptitud | Área (Ha) | % |
|---------|-----------|---|
| Exclusión legal | 891,451.7 | 42.9% |
| No apta | 786,114.8 | 37.9% |
| Aptitud alta | 263,523.1 | 12.7% |
| Aptitud media | 114,299.1 | 5.5% |
| Aptitud baja | 21,416.1 | 1.0% |
| **TOTAL** | **2,076,804.8** | **100%** |

## Ranking de Municipios por Aptitud
| Municipio | Índice Aptitud | Aptitud Dominante | Área Total (Ha) |
|-----------|---------------|-------------------|-----------------|
| Ulloa | 0.835 | Aptitud Alta | 4,236.2 |
| Alcalá | 0.827 | Aptitud Alta | 6,356.7 |
| Caicedonia | 0.753 | Aptitud Alta | 16,711.2 |
| Candelaria | 0.615 | Aptitud Alta | 29,416.4 |
| Bugalagrande | 0.501 | No Apta | 39,610.2 |
| San Pedro | 0.498 | Aptitud Alta | 21,073.7 |
| Andalucía | 0.469 | No Apta | 11,103.7 |
| Obando | 0.467 | No Apta | 21,479.2 |
| El Águila | 0.437 | Aptitud Alta | 18,699.8 |
| La Victoria | 0.424 | No Apta | 26,498.3 |
| Guacarí | 0.395 | No Apta | 16,319.2 |
| Cartago | 0.368 | No Apta | 24,741.8 |
| Toro | 0.368 | No Apta | 17,820.6 |
| Palmira | 0.360 | Exclusion Legal | 100,446.9 |
| Ansermanuevo | 0.355 | No Apta | 30,432.3 |
| Restrepo | 0.351 | Exclusion Legal | 13,585.9 |
| Sevilla | 0.350 | No Apta | 53,936.7 |
| Riofrío | 0.347 | No Apta | 30,731.1 |
| Florida | 0.346 | No Apta | 40,387.3 |
| Jamundí | 0.331 | No Apta | 62,317.9 |
| Trujillo | 0.326 | No Apta | 30,727.8 |
| Zarzal | 0.324 | No Apta | 36,800.7 |
| Tuluá | 0.249 | No Apta | 90,284.5 |
| El Cerrito | 0.241 | Exclusion Legal | 44,194.1 |
| La Unión | 0.194 | No Apta | 12,009.5 |
| La Cumbre | 0.170 | Exclusion Legal | 25,479.7 |
| Pradera | 0.152 | No Apta | 35,728.7 |
| Roldanillo | 0.146 | No Apta | 23,522.7 |
| Buga | 0.139 | No Apta | 82,180.5 |
| Yotoco | 0.126 | No Apta | 32,752.8 |
| Ginebra | 0.118 | Exclusion Legal | 26,795.0 |
| Yumbo | 0.096 | No Apta | 23,185.6 |
| Vijes | 0.079 | Exclusion Legal | 11,264.9 |
| Cali | 0.067 | Exclusion Legal | 56,741.7 |
| Bolívar | 0.047 | Exclusion Legal | 74,276.9 |
| Dagua | 0.037 | Exclusion Legal | 91,941.6 |
| Versalles | 0.012 | Exclusion Legal | 23,115.9 |
| Argelia | 0.011 | Exclusion Legal | 9,044.1 |
| El Dovio | 0.011 | Exclusion Legal | 20,625.0 |
| El Cairo | 0.008 | Exclusion Legal | 21,233.2 |
| Calima (El Darién) | 0.002 | Exclusion Legal | 79,808.4 |
| Buenaventura | 0.001 | Exclusion Legal | 639,186.4 |

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
- **Uso principal**: Predictor base de aptitud agroecológica para caña panelera
- **Variables derivadas**: % aptitud por municipio + índice de aptitud (0-1)
- **Cruce con EVA**: Por código municipio DANE