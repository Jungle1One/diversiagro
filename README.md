# DiversIAgro: Democratización de la Inteligencia Agroespacial

## Problema abordado
El sector agrícola del Valle del Cauca sufre por la vulnerabilidad climática derivada de los monocultivos tradicionales. Además, existe una **brecha digital severa**: aunque el gobierno publica mapas de aptitud para cultivos alternativos, estos están en formatos GIS pesados inaccesibles para el campesino promedio, quien a menudo carece de internet rural o conocimientos técnicos.

## Justificación (Valor público o empresarial)
DiversIAgro aporta un inmenso valor público al funcionar como un puente de **inclusión digital**. Permite a cualquier campesino consultar la aptitud de su tierra para nuevos cultivos (Café, Cacao, Aguacate, etc.) mediante una simple llamada telefónica. El proyecto empodera económicamente al productor fomentando la diversificación y la mitigación de riesgos climáticos frente a El Niño/La Niña.

## Cantidad de Dataset utilizado
Se utilizaron **3 ecosistemas de datos masivos**. Tras el filtrado espacial (Clipping al Valle del Cauca), el pipeline integró más de **3 millones de registros pluviométricos** (IDEAM) y miles de polígonos vectoriales (UPRA), cruzándolos con una matriz Raster topográfica (DEM).

## Dataset utilizado (datos.gov.co)
- **Precipitación IDEAM:** [SODA API s54a-sgyg](https://www.datos.gov.co/resource/s54a-sgyg)
- **Zonificación UPRA Café:** [SODA API kwvf-nwea](https://www.datos.gov.co/resource/kwvf-nwea)
- **Zonificación UPRA Cacao:** [SODA API jdjx-qer4](https://www.datos.gov.co/resource/jdjx-qer4)
- **Zonificación UPRA Aguacate:** [SODA API tx7u-frn2](https://www.datos.gov.co/resource/tx7u-frn2)
- **Zonificación UPRA Fresa:** [SODA API emsg-94di](https://www.datos.gov.co/resource/emsg-94di)
- **Zonificación UPRA Caña Panelera:** [SODA API p9xp-sm4v](https://www.datos.gov.co/resource/p9xp-sm4v)
- **Histórico de Cosechas (EVA):** [SODA API uejq-wxrr](https://www.datos.gov.co/resource/uejq-wxrr)

## Dataset utilizado Externos
- **Topografía (DEM):** Shuttle Radar Topography Mission (SRTM) de **NASA/USGS** (resolución 30m).

## Variables seleccionadas
1. **Altitud (m.s.n.m)** - Proxy de temperatura.
2. **Pendiente (grados)** - Proxy de erosión y mecanización.
3. **Precipitación Anual (mm)** - Recurso hídrico.
4. **Coordenadas (Lat/Lon)** - Autocorrelación espacial.
5. **Aptitud (Target)** - Alta(3), Media(2), Baja(1), No Apta(0).

## Tipo de análisis
**Predictivo** (Regresión geoespacial que luego se discretiza como clasificación de aptitud).

## Modelo utilizado
**Modelo Híbrido RFRK** (Random Forest Regression Kriging).
Utiliza **Random Forest** (Árboles de Decisión Múltiples) para aprender la relación bioclimática determinística, acoplado con **Kriging Ordinario** para corregir matemáticamente los residuos espaciales en el terreno.

## Resultados clave
- El modelo alcanzó un **R² > 0.85** aislando el componente bioclimático.
- La predicción final (incluyendo el Kriging) logra una continuidad espacial que evita los bordes "pixelados" irreales clásicos del Random Forest puro.
- **Eficiencia:** Logramos optimizar el pipeline de inferencia para responder en **<1 segundo**, haciendo viable la integración con Voice IVR de Twilio.

## Interpretación
El algoritmo aprendió que la *Altitud* actúa como un muro biológico estricto (cortes duros en los árboles de decisión), mientras que la *Precipitación* tiene un comportamiento más gradual. El componente de Kriging demostró ser vital: corrigió el puntaje de aptitud en zonas donde variables "ocultas" (no incluidas en el dataset, como el tipo de suelo) afectaban el mapa real de la UPRA.

## Impacto potencial
DiversIAgro puede escalar a nivel nacional. Tiene el potencial de convertirse en el "asesor agronómico" automático de más de 2 millones de campesinos en Colombia, requiriendo únicamente señal celular de voz (2G) y combatiendo directamente la inseguridad alimentaria mediante siembras informadas por IA.

---

## Solución en Producción (Demo en Vivo)

Para ver y probar la solución funcionando en tiempo real a través de los siguientes accesos:

**Aplicación Web / Producción:** [Visitar la solución en vivo](https://diversiagro-app.onrender.com) *(Reemplazar con tu enlace final)*
**Documentación de la API:** [Explorar Swagger/Postman](https://diversiagro-api.onrender.com/docs) *(Reemplazar con tu enlace final)*

---

## Enlaces de acceso

Enlaces de acceso para GitHub y GitLab:

*   [Descargar archivo original (.PPTX)](recursos/presentacion.pptx) — *Para abrir y editar en PowerPoint.*
*   [Ver presentación en línea (.PDF)](recursos/presentacion.pdf) — *Abre el visor interactivo de GitHub o GitLab.*
*   [Descarga directa (.PDF)](recursos/presentacion.pdf?raw=true&inline=false) — *Fuerza la descarga en ambas plataformas.*
