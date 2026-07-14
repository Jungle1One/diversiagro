# Reporte de Exploración - Dataset EVA 2019-2024

Fecha de generación: 2026-07-07 21:10:12

## Información General
- **Total de registros**: 141,073
- **Total de columnas**: 22
- **Columnas**: :id, :version, :created_at, :updated_at, c_digo_dane_departamento, departamento, c_digo_dane_municipio, municipio, grupo_cultivo, subgrupo, cultivo, desagregaci_n_cultivo, a_o, periodo, rea_sembrada, rea_cosechada, producci_n, rendimiento, ciclo_del_cultivo, estado_f_sico_del_cultivo, c_digo_del_cultivo, nombre_cient_fico_del_cultivo

## Tipos de Datos
- `:id`: str
- `:version`: str
- `:created_at`: str
- `:updated_at`: str
- `c_digo_dane_departamento`: int64
- `departamento`: str
- `c_digo_dane_municipio`: int64
- `municipio`: str
- `grupo_cultivo`: str
- `subgrupo`: str
- `cultivo`: str
- `desagregaci_n_cultivo`: str
- `a_o`: int64
- `periodo`: str
- `rea_sembrada`: float64
- `rea_cosechada`: float64
- `producci_n`: float64
- `rendimiento`: float64
- `ciclo_del_cultivo`: str
- `estado_f_sico_del_cultivo`: str
- `c_digo_del_cultivo`: int64
- `nombre_cient_fico_del_cultivo`: str

## Valores Nulos
- `:id`: 0 (0.0%)
- `:version`: 0 (0.0%)
- `:created_at`: 0 (0.0%)
- `:updated_at`: 0 (0.0%)
- `c_digo_dane_departamento`: 0 (0.0%)
- `departamento`: 0 (0.0%)
- `c_digo_dane_municipio`: 0 (0.0%)
- `municipio`: 0 (0.0%)
- `grupo_cultivo`: 0 (0.0%)
- `subgrupo`: 0 (0.0%)
- `cultivo`: 0 (0.0%)
- `desagregaci_n_cultivo`: 0 (0.0%)
- `a_o`: 0 (0.0%)
- `periodo`: 0 (0.0%)
- `rea_sembrada`: 0 (0.0%)
- `rea_cosechada`: 0 (0.0%)
- `producci_n`: 0 (0.0%)
- `rendimiento`: 0 (0.0%)
- `ciclo_del_cultivo`: 0 (0.0%)
- `estado_f_sico_del_cultivo`: 0 (0.0%)
- `c_digo_del_cultivo`: 0 (0.0%)
- `nombre_cient_fico_del_cultivo`: 0 (0.0%)

## Distribución por Departamento (Top 10)
- Boyacá: 14,969 registros
- Cundinamarca: 13,218 registros
- Antioquia: 12,934 registros
- Santander: 11,003 registros
- Huila: 10,036 registros
- Nariño: 9,742 registros
- Valle del Cauca: 9,032 registros ⬅️ **INTERÉS**
- Cauca: 6,356 registros
- Norte de Santander: 6,028 registros
- Tolima: 5,657 registros

## Años Disponibles
- 2019, 2020, 2021, 2022, 2023, 2024
  - 2019: 20,436 registros
  - 2020: 21,511 registros
  - 2021: 23,898 registros
  - 2022: 24,808 registros
  - 2023: 24,908 registros
  - 2024: 25,512 registros

## Cultivos Únicos: 166

### Cultivos de Interés para el Proyecto
- **Café**: 3,807 registros
- **Plátano**: 4,824 registros
- **Caña**: 4,029 registros
- **Cacao**: 3,439 registros
- **Papaya**: 1,139 registros
- **Fresa**: 700 registros
- **Aguacate**: 4,751 registros
- **Banano**: 1,644 registros

## Datos Valle del Cauca
- **Total registros**: 9,032
- **Cultivos distintos**: 78

### Cultivos de Interés en Valle del Cauca
- **Café**: 234 registros
- **Plátano**: 242 registros
- **Caña**: 372 registros
- **Cacao**: 202 registros
- **Papaya**: 139 registros
- **Fresa**: 47 registros
- **Aguacate**: 343 registros
- **Banano**: 225 registros
- **Municipios**: 42

### Municipios del Valle del Cauca (42 únicos)
  - Roldanillo: 397
  - Yumbo: 337
  - Bolívar: 326
  - Tuluá: 314
  - Guadalajara de Buga: 306
  - Palmira: 296
  - Sevilla: 294
  - Florida: 289
  - Santiago de Cali: 278
  - Dagua: 274
  - San Pedro: 264
  - Yotoco: 257
  - La Unión: 255
  - Vijes: 246
  - Restrepo: 242
  - Guacarí: 238
  - Versalles: 236
  - Jamundí: 227
  - Calima: 221
  - Trujillo: 220
  - El Dovio: 215
  - La Cumbre: 199
  - Bugalagrande: 193
  - Pradera: 192
  - El Águila: 190
  - La Victoria: 189
  - Riofrío: 188
  - Ansermanuevo: 185
  - Toro: 181
  - Obando: 175
  - Alcalá: 168
  - Caicedonia: 167
  - Ginebra: 162
  - Candelaria: 150
  - El Cerrito: 148
  - Argelia: 140
  - Cartago: 133
  - El Cairo: 120
  - Andalucía: 116
  - Zarzal: 107
  - Buenaventura: 103
  - Ulloa: 94

## Estadísticas Numéricas (Dataset Completo)

### rea_sembrada
  - count: 141,073.00
  - mean: 230.32
  - std: 1,167.62
  - min: 0.00
  - 25%: 5.78
  - 50%: 20.00
  - 75%: 93.30
  - max: 60,000.00

### rea_cosechada
  - count: 141,073.00
  - mean: 210.58
  - std: 1,104.77
  - min: 0.00
  - 25%: 5.00
  - 50%: 18.00
  - 75%: 82.00
  - max: 61,000.00

### producci_n
  - count: 141,073.00
  - mean: 3,192.23
  - std: 49,055.99
  - min: 0.00
  - 25%: 21.00
  - 50%: 104.00
  - 75%: 559.77
  - max: 4,776,340.50

### rendimiento
  - count: 141,073.00
  - mean: 10.60
  - std: 15.54
  - min: 0.00
  - 25%: 1.80
  - 50%: 6.00
  - 75%: 13.00
  - max: 253.00