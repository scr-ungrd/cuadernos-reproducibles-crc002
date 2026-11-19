# CRC002: simulación del tsunami de Tumaco de 1979 con Google Colab

> **Cuaderno reproducible de conocimiento del riesgo.** Subdirección para el Conocimiento del Riesgo (SCR), Unidad Nacional para la Gestión del Riesgo de Desastres (UNGRD), Colombia.
> **Ejercicio sin validar por una persona experta: no usar para tomar decisiones.**

- **Sitio:** <https://scr-ungrd.github.io/cuadernos-reproducibles-crc002/>
- **Binder:** <https://mybinder.org/v2/gh/scr-ungrd/cuadernos-reproducibles-crc002/main>

## Qué hace

Simula la propagación del tsunami del 12 de diciembre de 1979 (Mw 8,3) en el Pacífico colombiano con una fuente de Okada y aguas someras no lineales con fricción de Manning y celda seca (versión 3; las lineales de la versión 2 se conservan como comparación), en tres cuadernos que corren en Google Colab sin GPU ni TPU. Se inspira en Madden et al. (2023) pero no usa su código ni su esquema: batimetría (`01-bathymetry.ipynb`), simulación (`02-simulation.ipynb`) y visualización (`03-visualization.ipynb`). El alcance y las limitaciones están en el artículo (`article.md`).

## Estructura

| Ruta | Contenido |
|---|---|
| `article.md` | Artículo del sitio y del PDF |
| `notebooks/` | Los tres cuadernos (se generan con `scripts/construir_cuadernos.py`) |
| `data/` | Recorte del DEM de NOAA/NCEI y observaciones de 1979; véase `data/README.md` |
| `metadata/` | Fuentes (`sources.csv`), catálogo y diccionario de datos, sumas SHA-256 y metadatos RDLS |
| `scripts/` | `construir_cuadernos.py` y `registrar_descargas.py` |
| `DATA_STATEMENT.md`, `CITATION.cff`, `CHANGELOG.md`, `AI_USE.md` | Disponibilidad de datos y de código, cita, historial de cambios y uso de IA |

## Ejecutar

```bash
conda env create -f environment.yml   # Python 3.10 y versiones exactas, verificado el 2026-11-17
conda activate tsunami-tumaco
jupyter lab notebooks/
```

Los cuadernos se ejecutan en orden. El cuaderno 2 necesita el DEM del cuaderno 1 o la copia de `data/`.

## Licencia

Código bajo licencia MIT ([`LICENSE`](LICENSE)); texto y figuras bajo CC BY 4.0 ([`LICENSE-CC-BY-4.0`](LICENSE-CC-BY-4.0)). Los datos de `data/` conservan las condiciones de su origen: el recorte del DEM de NOAA/NCEI es de dominio público en EE. UU. y NCEI aplica CC0 a nivel internacional, y las observaciones de 1979 son hechos citados de Herd et al. (1981) y NOAA/NGDC con su procedencia (véanse `metadata/sources.csv` y `DATA_STATEMENT.md`).

## Cita y DOI

Los metadatos de cita están en [`CITATION.cff`](CITATION.cff). El DOI de todas las versiones es [10.5281/zenodo.24322477](https://doi.org/10.5281/zenodo.24322477); la versión actual (2.2.2) tiene el DOI [10.5281/zenodo.24324555](https://doi.org/10.5281/zenodo.24324555). La 2.2.1 (10.5281/zenodo.24324157) tiene un CSV mal formado y no debe usarse.

## Uso de inteligencia artificial

El desarrollo de este repositorio contó con la asistencia de Claude Sonnet 5.5, según el historial de commits. El registro y la declaración están en [`AI_USE.md`](AI_USE.md).
