# Reporte de Calidad – Zonificación de Banano (Procesado)

Fecha: 2026-07-08 18:39:28

## Resumen
- **Fuente**: UPRA – datos.gov.co (ID: rcfj-3e57)
- **Escala**: 1:100.000
- **Departamento**: Valle del Cauca
- **Polígonos procesados**: 4,074
- **Municipios**: 42

## Archivos Generados
| Archivo | Registros | Descripción |
|---------|-----------|-------------|
| zonificacion_banano_valle_limpio.csv | 4,074 | Polígonos con aptitud y área |
| zonificacion_banano_valle_municipio.csv | 42 | Resumen por municipio: % aptitud |

## Distribución de Aptitud (Valle del Cauca)
| Aptitud | Área (Ha) | % |
|---------|-----------|---|
| No apta | 951,530.4 | 45.8% |
| Exclusión legal | 891,451.7 | 42.9% |
| Aptitud alta | 135,382.1 | 6.5% |
| Aptitud media | 85,693.6 | 4.1% |
| Aptitud baja | 12,747.0 | 0.6% |
| **TOTAL** | **2,076,804.8** | **100%** |

## Ranking de Municipios por Aptitud
| Municipio | Índice Aptitud | Aptitud Dominante | Área Total (Ha) |
|-----------|---------------|-------------------|-----------------|
| Candelaria | 0.692 | Aptitud Media | 29,416.4 |
| Andalucía | 0.465 | No Apta | 11,103.7 |
| Guacarí | 0.446 | No Apta | 16,319.2 |
| Palmira | 0.392 | Exclusion Legal | 100,446.9 |
| El Cerrito | 0.382 | Exclusion Legal | 44,194.1 |
| Pradera | 0.253 | No Apta | 35,728.7 |
| Zarzal | 0.241 | No Apta | 36,800.7 |
| San Pedro | 0.239 | No Apta | 21,073.7 |
| Florida | 0.234 | No Apta | 40,387.3 |
| Jamundí | 0.230 | No Apta | 62,317.9 |
| Bugalagrande | 0.218 | No Apta | 39,610.2 |
| Ginebra | 0.194 | Exclusion Legal | 26,795.0 |
| Obando | 0.180 | No Apta | 21,479.2 |
| Caicedonia | 0.126 | No Apta | 16,711.2 |
| La Unión | 0.119 | No Apta | 12,009.5 |
| Roldanillo | 0.119 | No Apta | 23,522.7 |
| Riofrío | 0.110 | No Apta | 30,731.1 |
| Tuluá | 0.107 | No Apta | 90,284.5 |
| Yotoco | 0.105 | No Apta | 32,752.8 |
| Toro | 0.103 | No Apta | 17,820.6 |
| Yumbo | 0.087 | No Apta | 23,185.6 |
| Cartago | 0.086 | No Apta | 24,741.8 |
| Buga | 0.084 | No Apta | 82,180.5 |
| La Victoria | 0.040 | No Apta | 26,498.3 |
| Cali | 0.037 | Exclusion Legal | 56,741.7 |
| Sevilla | 0.027 | No Apta | 53,936.7 |
| Trujillo | 0.019 | No Apta | 30,727.8 |
| Bolívar | 0.018 | Exclusion Legal | 74,276.9 |
| Vijes | 0.015 | Exclusion Legal | 11,264.9 |
| Ansermanuevo | 0.011 | No Apta | 30,432.3 |
| Alcalá | 0.010 | No Apta | 6,356.7 |
| La Cumbre | 0.010 | Exclusion Legal | 25,479.7 |
| Buenaventura | 0.000 | Exclusion Legal | 639,186.4 |
| Argelia | 0.000 | Exclusion Legal | 9,044.1 |
| Dagua | 0.000 | Exclusion Legal | 91,941.6 |
| El Águila | 0.000 | No Apta | 18,699.8 |
| El Cairo | 0.000 | Exclusion Legal | 21,233.2 |
| Calima (El Darién) | 0.000 | Exclusion Legal | 79,808.4 |
| El Dovio | 0.000 | Exclusion Legal | 20,625.0 |
| Restrepo | 0.000 | No Apta | 13,585.9 |
| Versalles | 0.000 | Exclusion Legal | 23,115.9 |
| Ulloa | 0.000 | No Apta | 4,236.2 |

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
- **Uso principal**: Predictor base de aptitud agroecológica para banano
- **Variables derivadas**: % aptitud por municipio + índice de aptitud (0-1)
- **Cruce con EVA**: Por código municipio DANE