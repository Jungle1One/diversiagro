# 🌍 Evaluación de Impacto y Ética de la IA

DiversIAgro no es solo un modelo matemático; es una herramienta diseñada para intervenir en realidades sociales vulnerables. Por lo tanto, su diseño técnico está anclado a consideraciones éticas profundas.

## 1. Impacto Social y Económico
- **Mitigación de Pobreza y Riesgo:** Al ayudar al campesino a identificar qué cultivos alternativos (ej. Cacao en lugar de Caña) son óptimos para su finca, se reduce la probabilidad de pérdidas totales de cosecha provocadas por el cambio climático (sequías/inundaciones). La diversificación es la base de la resiliencia financiera rural.
- **Inclusión Digital (La Llamada Telefónica):** El mayor impacto de DiversIAgro es su interfaz. En lugar de requerir que el campesino compre un smartphone, pague un plan de datos 4G, descargue una app y aprenda a leer un mapa GIS, la IA "habla" a través de una red 2G/3G de voz tradicional. Es IA al servicio del marginado digital.

## 2. Mitigación de Sesgos Algorítmicos (Bias Mitigation)
- **Sesgo de Datos Institucionales:** Si un municipio históricamente no ha sembrado Cacao, el modelo tradicional de Random Forest podría sesgarse y decir que "no es apto" simplemente por falta de datos.
  - **Mitigación:** Utilizamos la *Aptitud Multicriterio de la UPRA* como base, la cual es de naturaleza bioclimática (teórica) y no meramente estadística de cosecha pasada.
- **Outliers Climáticos:** El IDEAM a veces reporta estaciones con 0mm o 200,000mm de lluvia por errores humanos al digitar.
  - **Mitigación:** En la fase de preparación (`consolidate_training_data.py`), aplicamos un "Clipping" estricto. La IA nunca verá ni aprenderá de lluvias imposibles que pudieran sesgar el árbol de decisión.

## 3. Transparencia y Explicabilidad
Un campesino no confiará en un robot que simplemente le diga "Siembra Cacao".
- Por ello, el frontend para los extensionistas muestra el **Mapa de Aptitud completo**, no una caja negra.
- A nivel estadístico, extraemos la **Importancia de Variables (Feature Importance)** de Random Forest. Sabemos matemáticamente si fue la altura (Topografía) o la escasez de lluvia (Clima) lo que descartó un cultivo.

## 4. Riesgo de Daño y Advertencias (Disclaimers)
Ningún modelo sustituye a un agrónomo en el terreno evaluando el pH del suelo. DiversIAgro predice **Aptitud Biofísica a Macroescala**, pero no evalúa:
- Condiciones de mercado (precio del Cacao).
- Estructura química del suelo a nivel de lote.
- Por tanto, la respuesta automatizada de Twilio siempre debe invitar al campesino a consultar a la UMATA de su municipio antes de invertir en semillas.
