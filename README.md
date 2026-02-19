# Proyecto-mineria-streamlit
# Dashboard – Siniestros viales fatales en Argentina (2017–2023)

Dashboard interactivo desarrollado en **Streamlit** como Proyecto Final de la materia **Minería de Datos** (Tecnicatura en Ciencia de Datos e IA).
## Dashboard online
Link: https://proyecto-mineria-app-3vp9gtvopaaecwapp9w8clb.streamlit.app/ 

**Fuente de datos:** datos.gob.ar (Sistema de Alerta Temprana – SAT)  
**Unidad de análisis:** víctimas fatales (registros)

---

## Objetivo
Explorar patrones temporales, geográficos y por tipo de vehículo en siniestros viales fatales en Argentina durante el período 2017–2023, aplicando el flujo **KDD**:
1. Selección/obtención del dataset  
2. Limpieza y transformación  
3. Minería de datos (series temporales: tendencia y estacionalidad)  
4. Visualización e interpretación de resultados

---

- ## Cómo usar el dashboard
Use los filtros (Año y Provincia) para actualizar KPIs, gráficos y mapa.

---

## Notas metodológicas y limitaciones
- Los resultados se presentan como **frecuencias** (conteos). Para comparar riesgo relativo por provincia/vehículo sería necesario normalizar por población, parque automotor o exposición al tránsito.
- El análisis temporal identifica **patrones y asociaciones** (por ejemplo, quiebre en 2020), pero **no permite afirmar causalidad**.
- El mapa utiliza únicamente registros con coordenadas válidas; por eso se muestra la **cobertura geográfica** (% con latitud/longitud).
- Para mejorar la interpretabilidad, se utiliza `victima_vehiculo_ampliado` en distribuciones generales y `victima_vehiculo` (versión resumida) en cruces, evitando fragmentación excesiva de categorías.



