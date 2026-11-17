# Ficha del modelo: simulación del tsunami de Tumaco de 1979

Conforme al «Estándar de modelos» de la colección de Cuadernos Reproducibles (<https://scr-ungrd.github.io/cuadernos-reproducibles/estandar-modelos>). Describe el modelo de `notebooks/02-simulation.ipynb`.

## 1. Propósito y uso previsto

- **Modelo:** propagación de un tsunami con las ecuaciones de aguas someras lineales (LSWE) en malla escalonada, con una fuente de dislocación elástica de Okada (1985). Es un modelo físico, no de aprendizaje automático.
- **Versión:** 2.2.1 (2026-11-17; DOI de todas las versiones 10.5281/zenodo.24322477). **Autoría:** Subdirección para el Conocimiento del Riesgo, UNGRD. **Licencia:** código MIT; texto y figuras CC BY 4.0.
- **Uso previsto:** estimar el tiempo de arribo y comparar escenarios de la propagación del tsunami del 12 de diciembre de 1979 hacia Tumaco, con fines educativos y de método. Por qué un modelo físico: el evento tiene pocas observaciones y no permite entrenar un modelo estadístico.
- **Usos no previstos:** mapas de amenaza o de inundación (las LSWE no calculan inundación en tierra), dimensionar obras o tasas de daño con las amplitudes, y decisiones de evacuación o de ordenamiento territorial.
- **Límites de validez:** Pacífico colombo-ecuatoriano (0,2° S a 4,2° N, 81,2° a 76,9° O); un escenario (Mw 8,3); malla de 450 m; 110 minutos de simulación.
- **Revisión previa a una decisión:** debe revisar el resultado una persona experta en tsunamis de la SCR. La revisión la coordina Mauricio Romero Torres (SCR-UNGRD).

## 2. Datos del modelo

- **Batimetría:** mosaico global de DEM de NOAA/NCEI recortado (`data/dem_tumaco_noaa_15s.tif`). Es de dominio público en EE. UU. y NCEI aplica CC0 a nivel internacional; las condiciones de los modelos que lo componen no se verificaron (`metadata/sources.csv`).
- **Observaciones (solo contraste):** `data/observaciones_1979.csv`, 12 lugares con la procedencia de cada valor (Herd et al., 1981 y NOAA/NGDC, que **no coinciden** entre sí; ver `data/README.md`). No se usan para entrenar ni calibrar: el modelo no tiene parámetros calibrados.
- **Hoja de datos:** `data/README.md` y `metadata/` (fuentes, catálogo, diccionario, RDLS).
- **Sin datos personales** ni de comunidades. Los datos son una batimetría y observaciones de run-up.

## 3. Descripción del método

- **Ecuaciones:** LSWE linealizadas, esquema de diferencias finitas en malla escalonada, sin difusión numérica y sin fricción (sección «Esquema numérico» del artículo).
- **Fuente:** falla rectangular de Okada: Mw 8,3, 200 × 80 km, rumbo 30°, buzamiento 15°, ángulo de desplazamiento 90°, borde superior a 12 km, rigidez 30 GPa, Poisson 0,25, deslizamiento 7,4 m. **La geometría es un supuesto**; la magnitud viene de la literatura.
- **Numérica:** malla de 1 065 × 1 084 celdas de 450 m (UTM 17N), paso de 1 s (CFL = 0,70), 6 600 s (110 min), instantáneas cada 240 s.
- **Parámetros ajustados:** ninguno; no hay hiperparámetros ni selección con datos de prueba.
- **Modelos o pesos de terceros:** ninguno. Okada se implementó en el repositorio y se verificó contra `pyrocko`.
- **Formato:** no hay pesos; los resultados se guardan como arreglos de NumPy y GIF.

## 4. Validación y desempeño

- **Verificación numérica:** deformación de Okada contra `pyrocko` (diferencia menor que 1e-5 m en tres geometrías), onda plana contra la solución exacta, estado de reposo exacto y fuente ligada al epicentro (prueba automática).
- **Comparación con observaciones:** siete estaciones comparables. Hay dos tiempos documentados: en Buenaventura la primera ola positiva (99 min) **no aparece en el modelo** (η máx. −0,01 m en la celda de 5 m), y en Esmeraldas el retroceso coincide en signo, no en tiempo. La razón η simulada / run-up va de 0,12 a 5,7 según la estación y la fuente (Tumaco: 5,7 veces el valor de Herd y 1,5 el de NOAA/NGDC). **No se calcula RMSE ni R²**: las fuentes se contradicen.
- **Contraste con la literatura:** 22 min de primer ascenso en Tumaco frente a 22 min de TUNAMI-N2 (Ávila-Guzmán et al., 2026). La amplitud en la celda de Tumaco (4,6 m) es unas dos veces la de Escobar et al. (2020).
- **No es una validación independiente.** Línea base simple y *back-testing*: no se hicieron. La revisión por una persona experta del dominio no se ha hecho.
- **Casos de fallo conocidos:** sobreestima la amplitud en Tumaco y la subestima en San Juan de la Costa, Isla Gorgona y Guapi; no calcula inundación; no reproduce la primera ola positiva observada en Buenaventura.

## 5. Incertidumbre y sensibilidad

- Fuentes: la geometría de la falla (supuesto), la resolución de la malla y la calidad de las observaciones.
- **Sensibilidad** (un parámetro a la vez, malla de 900 m): la amplitud en Tumaco varía de 4,2 a 8,8 m según la fuente; el arribo es robusto (21 a 26 min). La resolución cambia 7 % la amplitud.
- No se entregan intervalos ni probabilidades: el resultado es determinista y un escenario.

## 6. Reproducibilidad

- Entorno: `environment.yml`, con versiones exactas y Python 3.10. Verificado el 2026-11-17 en un clon limpio del repositorio con un entorno nuevo: los tres cuadernos corrieron sin errores en 150 s en un Apple M1 de 8 núcleos (CPU, sin GPU), y los resultados coinciden con los publicados; la simulación de 110 min en la malla de 450 m toma unos 45 s. Binder: el 2026-11-17 la imagen se construyó desde `environment.yml` y arrancó sin errores (no se ejecutaron los cuadernos dentro de Binder). No se probó en Colab.
- El cálculo es determinista y no usa semillas ni aleatoriedad.
- Los tres cuadernos se regeneran con `scripts/construir_cuadernos.py`; `metadata/descargas.csv` guarda las sumas SHA-256 de los datos.
- No hay un registro de experimentos ni pruebas automáticas fuera de las de verificación del cuaderno 2.

## 7. Riesgos, sesgos y uso responsable

- **No hacer daño:** una amplitud simulada de 8 m en Tumaco podría malinterpretarse como una cota de inundación o usarse para fijar zonas seguras. El artículo lo advierte («Alcance: qué se puede y qué no se puede concluir») y el resultado no debe usarse para decisiones.
- **Sesgos:** el escenario usa una sola fuente supuesta y las observaciones son pocas; no hay cobertura de otros eventos.
- **Comunidades:** el área incluye territorios con presencia de comunidades étnicas. Sí se requiere consulta o autorización antes de usar el escenario para decisiones.
- **Explicabilidad:** el modelo es físico y sus ecuaciones están en el artículo.

## 8. Documentación y ciclo de vida

- `README.md`, `CHANGELOG.md` (versionado semántico), `CITATION.cff`, `DATA_STATEMENT.md` y `AI_USE.md`.
- **Obsolescencia:** el modelo se reemplaza cuando haya una versión no lineal con la distribución de deslizamiento de Poveda y Pulido (2019) y observaciones verificadas. Decide Mauricio Romero Torres (SCR-UNGRD).
- **Uso de IA:** declarado en `AI_USE.md`.
- No se publica en un repositorio de modelos (no hay pesos).
