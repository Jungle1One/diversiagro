# 🏁 Conclusiones, Hallazgos y Trabajo Futuro

## 1. Hallazgos Clave
- **El Modelo Híbrido RFRK supera al Estándar:** Usar Random Forest de forma aislada generaba mapas con cortes abruptos y pixelados. La integración matemática de los residuos espaciales mediante Kriging Suavizado (PyKrige) permitió que el modelo "entendiera" que los lugares cercanos se parecen entre sí (Primera Ley de la Geografía de Tobler). El resultado son predicciones continuas y más realistas.
- **La IA como Puente Social, no solo como Oráculo:** El hallazgo más importante del proyecto es a nivel de UX (User Experience). Un LLM (Gemini 2.5) fue capaz de transcribir audios de baja calidad de campesinos, normalizar veredas mal pronunciadas e inyectar automáticamente esos datos a un modelo geoespacial estricto, sin que el campesino notara la complejidad de fondo.

## 2. Limitaciones Actuales
- **Resolución Topográfica:** El DEM de la NASA tiene una resolución de ~30 metros por píxel. Esto es excelente para macro-planificación municipal, pero insuficiente para la micro-zonificación de una finca de media hectárea.
- **Ausencia de Variables Edáficas:** El modelo actual es bioclimático (Temperatura vía Altitud + Precipitación + Pendiente). No incluye mapas de pH del suelo, textura o profundidad efectiva. Esto se debe a que la información cartográfica de suelos de alta resolución en Colombia es escasa.
- **Límites de Twilio API:** El proceso de Kriging toma cerca de 3-4 segundos. Las llamadas telefónicas sincrónicas exigen respuestas inmediatas o colapsan por `Timeout`. Tuvimos que crear un flag `use_kriging=False` para la línea telefónica, sacrificando un pequeño margen de precisión por velocidad en tiempo real.

## 3. Próximos Pasos (Escalabilidad)
1. **Despliegue Nacional:** Ampliar el dataset (DEM, UPRA) desde el Valle del Cauca hacia toda Colombia. Requerirá migrar el modelo en memoria RAM a bases de datos vectoriales especializadas (PostGIS) o clusters como Apache Spark.
2. **Alertas Tempranas Climáticas:** Integrar una alerta automática que envíe mensajes de texto SMS a los campesinos (Twilio Programmable SMS) advirtiendo sobre sequías pronosticadas para sus cultivos específicos en la próxima semana (consumiendo OpenMeteo a futuro).
3. **Múltiples Idiomas y Lenguas Nativas:** Usar la API de voz para atender no solo en Español, sino en dialectos indígenas (Nasa Yuwe), cerrando aún más la brecha de inclusión.
