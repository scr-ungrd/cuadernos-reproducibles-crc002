# Declaración de disponibilidad de datos y de código

Cuaderno CRC002: simulación del tsunami de Tumaco de 1979 con Google Colab. Conforme al «Estándar de datos» de la colección de Cuadernos Reproducibles (<https://scr-ungrd.github.io/cuadernos-reproducibles/estandar-de-datos>).

## Datos de entrada

Las dos fuentes, con su dirección exacta, versión o consulta y restricciones, están en [`metadata/sources.csv`](metadata/sources.csv). Ambas se obtienen sin credenciales y sin pago.

- **Mosaico global de DEM de NOAA/NCEI** (`DEM_mosaics/DEM_global_mosaic`): se pidió el 2026-11-02 y una copia del recorte se versiona en `data/dem_tumaco_noaa_15s.tif`. Es un mosaico de modelos de distinta resolución y procedencia. **Su licencia y la de los modelos que lo componen están por confirmar.**
- **Observaciones del tsunami de 1979** (Herd et al., 1981, `10.1126/science.211.4481.441`; base de tsunamis de NOAA/NGDC): 12 lugares en `data/observaciones_1979.csv`, reconstruidos en la versión 2.2 con la procedencia de cada valor (ver `metadata/DATA_DICTIONARY.md`), y los registros de NOAA/NGDC en `data/noaa_runups_1979.csv`. **Las dos fuentes no coinciden** (Tumaco: 0,8 m según Herd et al., 3 m según NOAA/NGDC) y no se promedian. La política abierta de NOAA/NCEI aplica CC0; los valores de Herd et al. son hechos citados con su referencia, y la licencia de la publicación original no se evaluó.

## Datos derivados publicados

Los archivos de `data/` están descritos en [`metadata/data_catalog.csv`](metadata/data_catalog.csv), sus variables en [`metadata/DATA_DICTIONARY.md`](metadata/DATA_DICTIONARY.md) y las sumas de verificación en [`metadata/descargas.csv`](metadata/descargas.csv). Las observaciones tienen metadatos RDLS 1.0.0 en [`metadata/rdls/`](metadata/rdls/).

La batimetría es un insumo de modelación y no un conjunto de datos de riesgo, por lo que no tiene archivo RDLS. Los resultados de los cuadernos (`notebooks/output/`) no se versionan.

Hasta que se confirmen las licencias de las fuentes, los datos de `data/` conservan las condiciones de su origen y no se les asigna una licencia propia.

## Datos con acceso restringido

Ninguno.

## Revisión CARE

- Los datos son una batimetría y observaciones de run-up de un evento; no contienen datos personales ni conocimiento local o tradicional.
- El área de estudio (Tumaco y el Pacífico sur colombiano) incluye territorios con presencia de comunidades étnicas. Sí: se requiere consulta o autorización antes de usar el escenario para decisiones o comunicación a las comunidades; este cuaderno es un ejercicio de reproducibilidad y no sustituye ese proceso.

## Disponibilidad de código

- Repositorio: <https://github.com/scr-ungrd/cuadernos-reproducibles-crc002>. Licencia MIT. Los tres cuadernos se generan con `scripts/construir_cuadernos.py`.
- Versión: 2.2.0 (2026-11-17). Sin DOI: falta archivar un *release* en Zenodo.
- Ficha del modelo: [`MODEL_CARD.md`](MODEL_CARD.md), conforme al Estándar de modelos.
- Software: [`environment.yml`](environment.yml).

## Validación técnica y limitaciones

- Comprobaciones: control de calidad de las observaciones por profundidad equivalente, verificación de la deformación de Okada contra `pyrocko` (error menor que 1e-5 m) y contraste con resultados publicados.
- Licencia de los valores de Herd et al. (1981), revisión del 2026-11-17 (análisis documental, no dictamen jurídico): el artículo es de Science y está protegido, pero el repositorio no copia su texto ni sus tablas; solo registra magnitudes de ola y tiempos de llegada, que son hechos, con la cita completa y la procedencia de cada valor. Un conjunto de hechos citado con atribución no exige permiso del editor. No se reproducen figuras ni tablas del artículo.
- Limitaciones: sección «Limitaciones y trabajo futuro» del artículo. El escenario sísmico usa parámetros supuestos y las observaciones de 1979 se contradicen entre fuentes (Herd et al. y NOAA/NGDC).
- El cuaderno es un ejercicio sin validar por una persona experta; no debe usarse para tomar decisiones.

## Compromiso de preservación

- Responsable: Subdirección para el Conocimiento del Riesgo, UNGRD (conocimiento@gestiondelriesgo.gov.co).
- Los datos se conservarán al menos cinco años después de la publicación. La SCR-UNGRD asume ese compromiso (confirmado el 2026-11-17).
