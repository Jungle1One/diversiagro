# Reporte de Calidad – Zonificación de Papaya (Procesado)

Fecha: 2026-07-08 18:40:10

## Resumen
- **Fuente**: UPRA – datos.gov.co (ID: urxm-qzje)
- **Escala**: 1:100.000
- **Departamento**: Valle del Cauca
- **Polígonos procesados**: 7,633
- **Municipios**: 42

## Archivos Generados
| Archivo | Registros | Descripción |
|---------|-----------|-------------|
| zonificacion_papaya_valle_limpio.csv | 7,633 | Polígonos con aptitud y área |
| zonificacion_papaya_valle_municipio.csv | 42 | Resumen por municipio: % aptitud |

## Distribución de Aptitud (Valle del Cauca)
| Aptitud | Área (Ha) | % |
|---------|-----------|---|
| No apta | 912,449.9 | 43.9% |
| Exclusión legal | 891,451.7 | 42.9% |
| Aptitud alta | 143,394.5 | 6.9% |
| Aptitud media | 125,435.2 | 6.0% |
| Aptitud baja | 4,073.5 | 0.2% |
| **TOTAL** | **2,076,804.8** | **100%** |

## Ranking de Municipios por Aptitud
| Municipio | Índice Aptitud | Aptitud Dominante | Área Total (Ha) |
|-----------|---------------|-------------------|-----------------|
| Alcalá | 0.651 | Aptitud Alta | 6,356.7 |
| Ulloa | 0.443 | No Apta | 4,236.2 |
| Guacarí | 0.441 | No Apta | 16,319.2 |
| Cartago | 0.415 | No Apta | 24,741.8 |
| Jamundí | 0.384 | Exclusion Legal | 62,317.9 |
| Caicedonia | 0.382 | No Apta | 16,711.2 |
| Obando | 0.373 | No Apta | 21,479.2 |
| Candelaria | 0.372 | No Apta | 29,416.4 |
| La Victoria | 0.357 | No Apta | 26,498.3 |
| San Pedro | 0.315 | No Apta | 21,073.7 |
| Zarzal | 0.260 | No Apta | 36,800.7 |
| Bugalagrande | 0.252 | No Apta | 39,610.2 |
| Florida | 0.233 | No Apta | 40,387.3 |
| Andalucía | 0.232 | No Apta | 11,103.7 |
| Sevilla | 0.227 | No Apta | 53,936.7 |
| Pradera | 0.215 | No Apta | 35,728.7 |
| El Cerrito | 0.199 | No Apta | 44,194.1 |
| Palmira | 0.194 | No Apta | 100,446.9 |
| Toro | 0.173 | No Apta | 17,820.6 |
| Trujillo | 0.158 | No Apta | 30,727.8 |
| Ansermanuevo | 0.144 | No Apta | 30,432.3 |
| Riofrío | 0.142 | No Apta | 30,731.1 |
| La Cumbre | 0.131 | Exclusion Legal | 25,479.7 |
| Ginebra | 0.123 | Exclusion Legal | 26,795.0 |
| Buga | 0.121 | No Apta | 82,180.5 |
| Yumbo | 0.109 | No Apta | 23,185.6 |
| Roldanillo | 0.107 | No Apta | 23,522.7 |
| Cali | 0.106 | Exclusion Legal | 56,741.7 |
| Tuluá | 0.093 | No Apta | 90,284.5 |
| La Unión | 0.093 | No Apta | 12,009.5 |
| Yotoco | 0.092 | No Apta | 32,752.8 |
| El Águila | 0.068 | No Apta | 18,699.8 |
| Vijes | 0.049 | Exclusion Legal | 11,264.9 |
| Bolívar | 0.010 | Exclusion Legal | 74,276.9 |
| Restrepo | 0.005 | No Apta | 13,585.9 |
| Dagua | 0.003 | Exclusion Legal | 91,941.6 |
| El Dovio | 0.002 | Exclusion Legal | 20,625.0 |
| Argelia | 0.000 | Exclusion Legal | 9,044.1 |
| Buenaventura | 0.000 | Exclusion Legal | 639,186.4 |
| El Cairo | 0.000 | Exclusion Legal | 21,233.2 |
| Calima (El Darién) | 0.000 | Exclusion Legal | 79,808.4 |
| Versalles | 0.000 | Exclusion Legal | 23,115.9 |

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
- **Uso principal**: Predictor base de aptitud agroecológica para papaya
- **Variables derivadas**: % aptitud por municipio + índice de aptitud (0-1)
- **Cruce con EVA**: Por código municipio DANE