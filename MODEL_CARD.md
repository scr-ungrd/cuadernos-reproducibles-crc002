# Ficha del modelo: simulación del tsunami de Tumaco de 1979

Conforme al «Estándar de modelos» de la colección de Cuadernos Reproducibles (<https://scr-ungrd.github.io/cuadernos-reproducibles/estandar-modelos>). Describe el modelo de `notebooks/02-simulation.ipynb`.

## 1. Propósito y uso previsto

- **Modelo:** propagación de un tsunami con las ecuaciones de aguas someras lineales (LSWE) en malla escalonada, con una fuente de dislocación elástica de Okada (1985). Es un modelo físico, no de aprendizaje automático.
- **Versión:** 2.1.0 (2026-11-16). **Autoría:** Subdirección para el Conocimiento del Riesgo, UNGRD. **Licencia:** código MIT; texto y figuras CC BY 4.0.
- **Uso previsto:** estimar el tiempo de arribo y comparar escenarios de la propagación del tsunami del 12 de diciembre de 1979 hacia Tumaco, con fines educativos y de método. Por qué un modelo físico: el evento tiene pocas observaciones y no permite entrenar un modelo estadístico.
- **Usos no previstos:** mapas de amenaza o de inundación (las LSWE no calculan inundación en tierra), dimensionar obras o tasas de daño con las amplitudes, y decisiones de evacuación o de ordenamiento territorial.
- **Límites de validez:** Pacífico colombo-ecuatoriano (0,2° S a 4,2° N, 81,2° a 76,9° O); un escenario (Mw 8,3); malla de 450 m; 60 minutos de simulación.
- **Revisión previa a una decisión:** debe revisar el resultado una persona experta en tsunamis de la SCR. <confirmar quién>

## 2. Datos del modelo

- **Batimetría:** mosaico global de DEM de NOAA/NCEI recortado (`data/dem_tumaco_noaa_15s.tif`). Su licencia y la de los modelos que lo componen están por confirmar (`metadata/sources.csv`).
- **Observaciones (solo contraste):** `data/observaciones_1979.csv`, 8 estaciones heredadas de la versión 1. **Contrastadas el 2026-11-16 con la base de NOAA/NGDC y no coinciden** (ver `data/README.md`). No se usan para entrenar ni calibrar: el modelo no tiene parámetros calibrados.
- **Hoja de datos:** `data/README.md` y `metadata/` (fuentes, catálogo, diccionario, RDLS).
- **Sin datos personales** ni de comunidades. Los datos son una batimetría y observaciones de run-up.

## 3. Descripción del método

- **Ecuaciones:** LSWE linealizadas, esquema de diferencias finitas en malla escalonada, sin difusión numérica y sin fricción (sección «Esquema numérico» del artículo).
- **Fuente:** falla rectangular de Okada: Mw 8,3, 200 × 80 km, rumbo 30°, buzamiento 15°, ángulo de desplazamiento 90°, borde superior a 12 km, rigidez 30 GPa, Poisson 0,25, deslizamiento 7,4 m. **La geometría es un supuesto**; la magnitud viene de la literatura.
- **Numérica:** malla de 1 065 × 1 084 celdas de 450 m (UTM 17N), paso de 1 s (CFL = 0,70), 3 600 s, instantáneas cada 120 s.
- **Parámetros ajustados:** ninguno; no hay hiperparámetros ni selección con datos de prueba.
- **Modelos o pesos de terceros:** ninguno. Okada se implementó en el repositorio y se verificó contra `pyrocko`.
- **Formato:** no hay pesos; los resultados se guardan como arreglos de NumPy y GIF.

## 4. Validación y desempeño

- **Verificación numérica:** deformación de Okada contra `pyrocko` (diferencia menor que 1e-5 m en tres geometrías), onda plana contra la solución exacta, estado de reposo exacto y fuente ligada al epicentro (prueba automática).
- **Comparación con observaciones:** cuatro estaciones comparables, sin verificar. Arribos simulados entre −7 y +8 min de los observados; η simulada de 1,2 a 2,0 veces el run-up observado. **No se calcula RMSE ni R²** por la pequeña cantidad y la calidad de los datos.
- **Contraste con la literatura:** 23 min de arribo a Tumaco frente a 22 min de TUNAMI-N2 (Ávila-Guzmán et al., 2026). Las amplitudes son unas cuatro veces las de Escobar et al. (2020).
- **No es una validación independiente.** Línea base simple y *back-testing*: no se hicieron. La revisión por una persona experta del dominio no se ha hecho.
- **Casos de fallo conocidos:** sobreestima amplitudes; no calcula inundación; el arribo en Bocagrande llega antes de lo observado.

## 5. Incertidumbre y sensibilidad

- Fuentes: la geometría de la falla (supuesto), la resolución de la malla y la calidad de las observaciones.
- **Sensibilidad** (un parámetro a la vez, malla de 900 m): la amplitud en Tumaco varía de 4,2 a 8,8 m según la fuente; el arribo es robusto (21 a 26 min). La resolución cambia 7 % la amplitud.
- No se entregan intervalos ni probabilidades: el resultado es determinista y un escenario.

## 6. Reproducibilidad

- Entorno: `environment.yml` (conda-forge). Corre en CPU estándar de Colab; unos 45 s para 60 min simulados en la malla de 450 m.
- El cálculo es determinista y no usa semillas ni aleatoriedad.
- Los tres cuadernos se regeneran con `scripts/construir_cuadernos.py`; `metadata/descargas.csv` guarda las sumas SHA-256 de los datos.
- No hay un registro de experimentos ni pruebas automáticas fuera de las de verificación del cuaderno 2.

## 7. Riesgos, sesgos y uso responsable

- **No hacer daño:** una amplitud simulada de 8 m en Tumaco podría malinterpretarse como una cota de inundación o usarse para fijar zonas seguras. El artículo lo advierte («Alcance: qué se puede y qué no se puede concluir») y el resultado no debe usarse para decisiones.
- **Sesgos:** el escenario usa una sola fuente supuesta y las observaciones son pocas; no hay cobertura de otros eventos.
- **Comunidades:** el área incluye territorios con presencia de comunidades étnicas. <confirmar si se requiere consulta o autorización>
- **Explicabilidad:** el modelo es físico y sus ecuaciones están en el artículo.

## 8. Documentación y ciclo de vida

- `README.md`, `CHANGELOG.md` (versionado semántico), `CITATION.cff`, `DATA_STATEMENT.md` y `AI_USE.md`.
- **Obsolescencia:** el modelo se reemplaza cuando haya una versión no lineal con la distribución de deslizamiento de Poveda y Pulido (2019) y observaciones verificadas. <confirmar quién decide>
- **Uso de IA:** declarado en `AI_USE.md`.
- No se publica en un repositorio de modelos (no hay pesos).
