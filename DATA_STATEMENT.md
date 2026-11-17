# Declaración de disponibilidad de datos y de código

Cuaderno CRC002: simulación del tsunami de Tumaco de 1979 con Google Colab. Conforme al «Estándar de datos» de la colección de Cuadernos Reproducibles (<https://scr-ungrd.github.io/cuadernos-reproducibles/estandar-de-datos>).

## Datos de entrada

Las dos fuentes, con su dirección exacta, versión o consulta y restricciones, están en [`metadata/sources.csv`](metadata/sources.csv). Ambas se obtienen sin credenciales y sin pago.

- **Mosaico global de DEM de NOAA/NCEI** (`DEM_mosaics/DEM_global_mosaic`): se pidió el 2026-11-02 y una copia del recorte se versiona en `data/dem_tumaco_noaa_15s.tif`. Es un mosaico de modelos de distinta resolución y procedencia. **Su licencia y la de los modelos que lo componen están por confirmar.**
- **Observaciones del tsunami de 1979** (Herd et al., 1981, `10.1126/science.211.4481.441`; base de tsunamis de NOAA/NGDC): 8 estaciones en `data/observaciones_1979.csv`. **El contraste del 2026-11-16 con la base de run-ups de NOAA/NGDC muestra que las cifras no coinciden** (tabla en `data/README.md`) y no se han verificado contra Herd et al. (1981); la licencia está por confirmar.

## Datos derivados publicados

Los archivos de `data/` están descritos en [`metadata/data_catalog.csv`](metadata/data_catalog.csv), sus variables en [`metadata/DATA_DICTIONARY.md`](metadata/DATA_DICTIONARY.md) y las sumas de verificación en [`metadata/descargas.csv`](metadata/descargas.csv). Las observaciones tienen metadatos RDLS 1.0.0 en [`metadata/rdls/`](metadata/rdls/).

La batimetría es un insumo de modelación y no un conjunto de datos de riesgo, por lo que no tiene archivo RDLS. Los resultados de los cuadernos (`notebooks/output/`) no se versionan.

Hasta que se confirmen las licencias de las fuentes, los datos de `data/` conservan las condiciones de su origen y no se les asigna una licencia propia.

## Datos con acceso restringido

Ninguno.

## Revisión CARE

- Los datos son una batimetría y observaciones de run-up de un evento; no contienen datos personales ni conocimiento local o tradicional.
- El área de estudio (Tumaco y el Pacífico sur colombiano) incluye territorios con presencia de comunidades étnicas. ¿Se requiere consulta o autorización para publicar el escenario? <confirmar>.

## Disponibilidad de código

- Repositorio: <https://github.com/scr-ungrd/cuadernos-reproducibles-crc002>. Licencia MIT. Los tres cuadernos se generan con `scripts/construir_cuadernos.py`.
- Versión: 2.1.0 (2026-11-16). Sin DOI: falta archivar un *release* en Zenodo.
- Ficha del modelo: [`MODEL_CARD.md`](MODEL_CARD.md), conforme al Estándar de modelos.
- Software: [`environment.yml`](environment.yml).

## Validación técnica y limitaciones

- Comprobaciones: control de calidad de las observaciones por profundidad equivalente, verificación de la deformación de Okada contra `pyrocko` (error menor que 1e-5 m) y contraste con resultados publicados.
- Limitaciones: sección «Limitaciones y trabajo futuro» del artículo. El escenario sísmico usa parámetros supuestos y las observaciones no están verificadas.
- El cuaderno es un ejercicio sin validar por una persona experta; no debe usarse para tomar decisiones.

## Compromiso de preservación

- Responsable: Subdirección para el Conocimiento del Riesgo, UNGRD (conocimiento@gestiondelriesgo.gov.co).
- Los datos se conservarán al menos cinco años después de la publicación. <confirmar el compromiso institucional>
