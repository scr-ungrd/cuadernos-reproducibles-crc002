# Diccionario de variables

Describe los archivos de `data/`. La descripción de su origen y de su estado de verificación está en [`data/README.md`](../data/README.md) y en [`sources.csv`](sources.csv).

## `observaciones_1979.csv`

Doce lugares con run-up o tiempo observado del tsunami del 12 de diciembre de 1979, con la procedencia de cada valor. **Herd et al. (1981) y la base de NOAA/NGDC no coinciden** donde ambos dan run-up (Tumaco: 0,8 frente a 3 m; San Juan de la Costa: 2,5 frente a 6 m); los valores no se promedian. Las coordenadas son las del registro de NOAA/NGDC.

| Columna | Descripción | Tipo | Unidad |
|---|---|---|---|
| `estacion` | Nombre del lugar de observación | texto | |
| `lat` | Latitud (la del registro de NOAA/NGDC) | decimal | grados norte |
| `lon` | Longitud (negativa al oeste) | decimal | grados este |
| `runup_herd_m` | Altura de la ola sobre la posición previa de la marea alta, según Herd et al. (1981), p. 442 | decimal | m |
| `runup_noaa_m` | Run-up del registro de NOAA/NGDC (`id_noaa`); se desconoce su referencia vertical | decimal | m |
| `t_obs_min` | Tiempo observado después del sismo (7:59:04 UTC) | decimal | min |
| `t_obs_tipo` | Qué es `t_obs_min`: `primera_ola_positiva` (mareógrafo de Buenaventura) o `retroceso` (inicio del retroceso del mar, Esmeraldas) | texto | |
| `id_noaa` | Identificador del registro en la base de run-ups de NOAA/NGDC | entero | |
| `notas` | Texto de apoyo con la cita de Herd et al. (1981) | texto | |

Hay valores faltantes por diseño: cada fuente cubre solo algunos lugares. Siete lugares son comparables con la simulación; los demás se excluyen y se declara en el cuaderno 3.

## `noaa_runups_1979.csv`

Registros de la base de run-ups de NOAA/NGDC para el 12 de diciembre de 1979 en Colombia y Ecuador, tal como los devolvió la API el 2026-11-16 (se omite un registro duplicado sin altura de Isla Gorgona, id 11154).

| Columna | Descripción | Tipo | Unidad |
|---|---|---|---|
| `id_noaa` | Identificador del registro | entero | |
| `lugar` | Nombre del lugar en la base | texto | |
| `pais` | País | texto | |
| `lat`, `lon` | Coordenadas del registro | decimal | grados |
| `runup_m` | Run-up registrado (vacío si no hay) | decimal | m |
| `dist_fuente_km` | Distancia a la fuente que calcula NOAA | decimal | km |
| `tipo_medicion` | Código de tipo de medición de NOAA (no se interpretó) | entero | |
| `primer_movimiento` | Código de primer movimiento de NOAA (no se interpretó) | texto | |
| `dudoso` | Marca de dato dudoso de NOAA (`n` = no) | texto | |

## `dem_tumaco_noaa_15s.tif`

Una banda con la elevación (positiva) y la batimetría (negativa) del dominio de simulación.

| Elemento | Valor |
|---|---|
| Sistema de coordenadas | WGS 84 (EPSG:4326) |
| Celdas | 1 032 columnas × 1 056 filas |
| Tamaño de celda | 15 arco-segundos (0,004167°, unos 460 m) |
| Dominio | de 0,2° S a 4,2° N y de 81,2° a 76,9° O |
| Unidad | metros |
| Valores de control | de −5 183 a 5 615 m; el epicentro está a −834 m y Tumaco a unos 4 m |
| Fecha del pedido | 2026-11-02 |
