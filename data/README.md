# Datos del proyecto (versión 2)

## Batimetría y topografía: `dem_tumaco_noaa_15s.tif`

Recorte geográfico (EPSG:4326, 1 032 × 1 056 celdas de 15 arco-segundos, unos 460 m) del dominio **0,2° S–4,2° N y 81,2°–76,9° O**, pedido el 2 de noviembre de 2026 al
servicio de mosaico global de DEM de NOAA/NCEI:

```
https://gis.ngdc.noaa.gov/arcgis/rest/services/DEM_mosaics/DEM_global_mosaic/ImageServer
```

Es un **mosaico de modelos de distinta resolución y procedencia**; no es GEBCO ni ETOPO 2022 puros. La versión 1 de este repositorio los nombraba, pero el enlace de
descarga de GEBCO que usaba responde 404 y el servicio entregaba el mosaico de NOAA. El cuaderno 1 usa esta copia y, si no está, vuelve a pedirla al servicio.

Valores de control: elevación −5 183 a 5 615 m; el punto del epicentro está a −834 m y Tumaco a unos 4 m.

## Observaciones históricas: `observaciones_1979.csv` y `noaa_runups_1979.csv`

Doce lugares con run-up o tiempo observado del tsunami del 12 de diciembre de 1979, **con la procedencia de cada valor**. Se reconstruyó el 2026-11-17 a partir de Herd et al. (1981, *Science* 211, 441–445; p. 442–443) y de la base de run-ups de NOAA/NGDC (`https://www.ngdc.noaa.gov/hazel/hazard-service/api/v1/tsunamis/runups`, consultada el 2026-11-16; los registros del 12-12-1979 están en `noaa_runups_1979.csv`). Las columnas están en `metadata/DATA_DICTIONARY.md`.

**Las dos fuentes no coinciden** donde ambas dan run-up, y por eso no se promedian:

| Lugar | Herd et al. (1981) | NOAA/NGDC (registro) |
|---|---|---|
| Tumaco | 0,8 m sobre la posición previa de la marea alta (rango de marea de 1,3 m); el mareógrafo quedó destruido | 3 m (9742) |
| San Juan de la Costa | casi 2,5 m sobre la marea alta previa; de 3 a 4 olas | 6 m (9745) |
| Buenaventura | primera ola positiva en el mareógrafo a la 1 h 39 min; sin altura | 0,14 m (9743); llegada a la 1 h 40 min |
| Esmeraldas | retroceso del mar a los 5 a 6 min; sin run-up | sin run-up (9752) |
| El Charco, Iscuandé | los reportes de inundación fueron falsos | 2 m cada uno (9749, 9748) |

El CSV de la versión 1 daba 5,0 y 4,5 m en Tumaco «según Herd», 0,8 m en Buenaventura, 4,0 m y 12 min en Esmeraldas, y tres lugares (Bocagrande, Salinas y una ubicación de «San Juan» tierra adentro) que ninguna fuente respalda. Esos valores se retiraron en la versión 2.2.

Limitaciones: se desconoce la referencia vertical de los registros de NOAA/NGDC y el informe en el que se basan; las coordenadas son las de NOAA/NGDC y varios puntos caen en estuarios o tierra adentro (se excluyen del cuaderno 3 y se declara); solo hay dos tiempos observados (Buenaventura y Esmeraldas) y son de tipos distintos.

## Escenario sísmico usado en la versión 2

| Parámetro | Valor | Estado |
|-----------|-------|--------|
| Mw | 8,3 | Yoshimoto et al. (2017), citado por Escobar et al. (2020) y Ávila-Guzmán et al. (2026) |
| Epicentro | 1,584° N, 79,386° O | Herd et al. (1981), tabla 1 (hipocentro preliminar del NEIS) |
| Profundidad del hipocentro | 33 km | Según el artículo de la versión 1 (por verificar) |
| Longitud × ancho de la falla | 200 × 80 km | **Supuesto** |
| Rumbo / buzamiento / ángulo de desplazamiento | 30° / 15° / 90° | **Supuesto** |
| Profundidad del borde superior | 12 km | **Supuesto** (el borde inferior queda a ~33 km) |
| Rigidez / Poisson | 30 GPa / 0,25 | Valores típicos |
| Deslizamiento uniforme | 7,4 m | Derivado de M₀ = μ·L·W·D |

La versión 1 documentaba otros valores (Mw 8,2; rumbo ~10°, buzamiento ~20°, 250 × 100 km, deslizamiento ~4 m), también sin fuente verificable; se corren como un caso de
sensibilidad (cuaderno 2, sección 6). La distribución de deslizamiento real del evento (Poveda y Pulido, 2019) **no se usó** porque no se tiene a mano.

## Salidas de los cuadernos (no se versionan)

`notebooks/output/` (o `/content/output/` en Colab): `dem_utm17_450m.tif`, `resultados.npz` (η máxima, mapa de arribos, 31 instantáneas, series en estaciones),
`estaciones.csv` y `sensibilidad.csv`.
