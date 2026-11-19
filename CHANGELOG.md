# Cambios

## 3.0.0 (sin publicar)

**Agregado**

- `SECURITY.md` (cómo reportar una vulnerabilidad o una filtración) y `metadata/escaneo_seguridad.md` (registro del escaneo de secretos y de vulnerabilidades del 2026-11-19).
- Aguas someras no lineales con fricción de Manning (n = 0,025, sin calibrar) y celda seca, en NumPy y en CPU (`run_nswe` en `notebooks/02-simulation.ipynb`, sección 2b), con arreglos de 32 bits. Las LSWE de la 2.2.2 se conservan como comparación.
- Pruebas del solver no lineal con aserciones (sección 3b del cuaderno 2): reposo exacto en una playa, onda plana, conservación de la masa, cuenco parabólico contra su solución exacta y efecto de la fricción.
- Sensibilidad de las NSWE a la no linealidad y al coeficiente de Manning (sección 6b; `output/sensibilidad_nswe.csv`) y comparación LSWE frente a NSWE en el cuaderno 3 (sección 5).
- Sección «Relación con Madden et al. (2023)» en el artículo: el cuaderno se inspira en ese trabajo pero no usa TPU ni su esquema numérico, no se probó `tsunamiTPUlab` y no se comparó con GeoClaw. Entrada `madden2023` en `references.bib`.

**Cambiado**

- `pillow` 12.3.0 → 13.0.0 en `environment.yml` y en el flujo de despliegue: la versión anterior tenía vulnerabilidades conocidas (`pip-audit`). Como 13.0.0 exige Python 3.11 o superior, el entorno y el flujo pasan de Python 3.10 a 3.11.
- `.github/workflows/deploy.yml`: permisos mínimos por trabajo, `mystmd` con versión fija y Typst con suma de verificación SHA-256. `.gitignore` excluye `.env`.
- Resultado principal (`output/resultados.npz`): ahora son las NSWE; las LSWE van a `output/resultados_lswe.npz`. En la celda de Tumaco η máx. pasa de 4,56 a 3,71 m y el arribo no cambia (21,9 min); en celdas de mar de 10 m o más, de 8,8 a 6,2 m. Las razones η simulada / run-up (artículo) cambian en consecuencia.
- Tiempo de ejecución del cuaderno 2: unos 11 min (antes unos 4); las NSWE a 450 m toman unos 5,5 min.
- `environment.yml` sin cambios; **no se volvió a verificar en un entorno nuevo, ni en Colab ni en Binder** (los cuadernos 2 y 3 se ejecutaron el 2026-11-18 en un entorno existente).

**Pendiente**

- La figura `images/flujo_tsunami.png` sigue describiendo la versión 2 (LSWE, inundación «pendiente»); el pie de figura lo advierte. Falta regenerarla.
- Revisión por una persona experta, versión de `CITATION.cff` y DOI de Zenodo (no se publicó una versión).

## 2.2.2 (2026-11-17)

Archivada en Zenodo: `10.5281/zenodo.24324555`.

**Corregido**

- `data/observaciones_1979.csv` de la 2.2.1 tenía una coma sin comillas en la nota de Guapi y no se podía leer (los cuadernos fallaban). Se pusieron comillas.
- Se añadió `scripts/probar_datos.py` (estructura, duplicados, rangos y valores esperados), que el despliegue ejecuta antes de los cuadernos.

## 2.2.1 (2026-11-17)

**Atención:** esta versión (DOI 10.5281/zenodo.24324157) tiene el CSV de observaciones mal formado; usar la 2.2.2.

**Corregido**

- `data/observaciones_1979.csv`: el hundimiento de Guapi según Herd et al. (1981) es de 25 a 30 cm (figura 1, p. 442), no de 40 a 45 cm (que es el de Bozán). Se contrastaron 13 valores con el artículo; ver `metadata/validacion_herd.md`. No cambia ningún resultado.

**Cambiado**

- `metadata/sources.csv`: Herd et al. (1981) y la base de run-ups de NOAA/NGDC son dos insumos con su fila, URL y licencia; los run-ups se citan con su DOI (10.7289/V5PN93H7) en `references.bib` y el artículo.
- El RDLS archivado en la v2.2.0 traía el `id` antiguo; esta versión lleva el actual.
- Binder: la imagen se construyó desde el `environment.yml` con versiones exactas y arrancó sin errores el 2026-11-17.

- `environment.yml` con versiones exactas y Python 3.10, verificado con una ejecución completa en un entorno limpio (150 s). Se quitaron `xarray`, `netcdf4`, `gdal`, `scipy` y `ipywidgets`, que los cuadernos no usan, y se añadieron `pandas` y `pillow`, que sí usan.
- Las 24 funciones de los cuadernos tienen *docstring* (12 antes).
- `LICENSE-CC-BY-4.0` para el texto y las figuras; el README y el catálogo de datos ya no dicen «por confirmar» en las licencias del DEM y de Herd et al.
- RDLS: el archivo de observaciones describe las 12 filas, la licencia y la procedencia, y incluye `data/noaa_runups_1979.csv`.

## 2.2.0 (2026-11-17)

**Cambiado**

- `data/observaciones_1979.csv` se reconstruyó: 12 lugares con la procedencia de cada valor (`runup_herd_m`, `runup_noaa_m`, `t_obs_min`, `t_obs_tipo`, `id_noaa`). Se eliminaron Bocagrande y Salinas (ninguna fuente los respalda), el run-up de Esmeraldas y la hora de llegada de Tumaco (el mareógrafo quedó destruido). Se corrigieron las atribuciones a Herd et al. (1981): en Tumaco la ola más alta fue de 0,8 m y no de 5,0 y 4,5 m, y la llegada a Buenaventura fue a 1 h 39 min y no a 45 min.
- Epicentro: 1,584° N, 79,386° O (tabla 1 de Herd et al., 1981) en lugar de 1,598° N, 79,359° O.
- Simulación de 110 min (antes 60) para alcanzar la primera ola positiva observada en Buenaventura (99 min); 28 cuadros en la animación.
- Cuaderno 3: la comparación usa el rango entre Herd et al. y NOAA/NGDC; los tiempos se comparan solo donde hay un tiempo del mismo tipo. Resultado: el modelo no reproduce la primera ola de Buenaventura; la razón η simulada / run-up va de 0,12 a 5,7 según la estación y la fuente.
- Artículo, `DATA_STATEMENT.md`, `MODEL_CARD.md`, diccionario, catálogo, `sources.csv` y RDLS actualizados con lo anterior.
- Licencia del DEM de NOAA/NCEI registrada según la política abierta de NCEI (CC0 para uso internacional); las condiciones de los modelos que lo componen no se verificaron.

**Agregado**

- `data/noaa_runups_1979.csv`: registros de NOAA/NGDC consultados el 2026-11-16.

**Pendiente**

- Informes detrás de los registros de NOAA (referencia vertical, tipo de medición), el informe de Pararas-Carayannis (1980) y registros mareográficos para reducir el rango entre fuentes.
- DOI de Zenodo, prueba CARE y licencia de los valores de Herd et al.

## 2.1.0 (2026-11-16)

**Agregado**

- `MODEL_CARD.md` (Estándar de modelos).
- Contraste de `observaciones_1979.csv` con la base de run-ups de NOAA/NGDC (2026-11-16): las cifras no coinciden (`data/README.md`).
- `DATA_STATEMENT.md`, `MODEL_CARD.md`, el diccionario, `AI_USE.md` y este historial como documentos de apoyo del sitio.
- Carpeta `metadata/`: `sources.csv`, `data_catalog.csv`, `DATA_DICTIONARY.md`, `descargas.csv` (sumas SHA-256) y el archivo RDLS 1.0.0 de las observaciones.
- `README.md`, `DATA_STATEMENT.md`, `CITATION.cff`, `AI_USE.md` y `scripts/registrar_descargas.py`.
- Secciones de disponibilidad de datos y declaración de uso de IA en el artículo.

**Cambiado**

- Título: «Simulación del Tsunami de Tumaco de 1979 con Google Colab».
- `environment.yml`: se quita el canal `defaults`; todos los paquetes están en `conda-forge`.

**Pendiente**

- Ninguno de los pendientes de DOI: la versión 2.2.0 está archivada en Zenodo (`10.5281/zenodo.24322478`).

## 2.0.0 (2026-11-02)

**Correcciones**

- **Animación espejada y fuente desligada del epicentro.** El DEM se guardaba con el eje X invertido y el mapa salía con el oeste a la derecha. Además la onda en N se colocaba en `x_coast − 60 km`
  (la celda de mar más oriental del dominio) y no en el epicentro: nacía a unos 200 km de la estrella. Ahora el mapa tiene el oeste a la izquierda y la falla se ancla al epicentro, con una
  prueba automática (el máximo de η inicial debe quedar a menos de 150 km de él).
- **Atribución del DEM.** El enlace de GEBCO 2023 responde 404 y el servicio entregaba el mosaico global de DEM de NOAA/NCEI, no GEBCO ni ETOPO 2022. Se corrige el texto y se versiona una copia del recorte (`data/dem_tumaco_noaa_15s.tif`).
- **Amplitud inicial.** La versión 1 declaraba `A = 8 m`, pero la fórmula `2·(A·e − A/3·e)` daba un pico inicial de 16 m. Ya no hay parámetro de calibración.
- **Estaciones.** Esmeraldas, Buenaventura y Salinas quedaban fuera del dominio (o recortadas al borde) y San Juan y El Charco caen tierra adentro. Se amplía el dominio, se lee cada estación en una celda de mar de ≥ 10 m y se excluyen y declaran las que no se pueden comparar.
- **Validación.** Se retiran el RMSE y el R² (comparaban η en el mar con run-up de una tabla sin verificar). Se agrega el control de calidad de las observaciones (profundidad equivalente) y el contraste con resultados publicados.
- **Magnitud y licencia.** Mw 8,3 (Yoshimoto et al., 2017) en lugar de 8,2; la licencia del código es MIT (el `myst.yml` decía Apache-2.0).

**Métodos**

- Fuente: deformación de Okada (1985) de una falla rectangular, verificada contra pyrocko (3 geometrías, error < 1e-5 m), en lugar de una onda en N calibrada.
- Solver: malla escalonada *forward-backward* en lugar de Lax-Friedrichs (conserva el 99,96 % de la amplitud de una onda plana frente al 43 %), con fronteras abiertas.
- Dominio ampliado (0,2° S–4,2° N, 81,2–76,9° O), UTM 17N, 60 minutos.
- Análisis de sensibilidad (resolución, Mw, rumbo, buzamiento, longitud, profundidad y los parámetros de la versión 1).

**Texto**

- Marco teórico nuevo (cadena de modelación, dislocación de Okada, ondas largas, LSWE y NSWE, esquema numérico, determinista frente a probabilista), sección «Alcance» con lo que los resultados sí y no sustentan, y limitaciones actualizadas.
- Bibliografía: se agregan Escobar et al. (2020), Ávila-Guzmán et al. (2026), Sánchez et al. (2023), Paez-Ramirez et al. (2021), el Atlas de 2019 y el mosaico de NOAA; se retiran Carrier et al. (2003), GEBCO y ETOPO.

**Pendiente** (ver «Limitaciones» del artículo): distribución de deslizamiento de Poveda y Pulido (2019), NSWE con inundación, verificación de las observaciones contra Herd et al. (1981) y NOAA/NGDC.

## 1.0.0 (2026-05-11)

Versión inicial: LSWE con Lax-Friedrichs y onda en N calibrada (A = 8 m).
