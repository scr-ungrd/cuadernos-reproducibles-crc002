# Diccionario de variables

Describe los archivos de `data/`. La descripción de su origen y de su estado de verificación está en [`data/README.md`](../data/README.md) y en [`sources.csv`](sources.csv).

## `observaciones_1979.csv`

Ocho estaciones con run-up y tiempo de arribo del tsunami del 12 de diciembre de 1979. **No están verificadas contra las fuentes primarias.**

| Columna | Descripción | Tipo | Unidad |
|---|---|---|---|
| `estacion` | Nombre del lugar de observación | texto | |
| `lat` | Latitud (aproximada en varias estaciones) | decimal | grados norte |
| `lon` | Longitud (negativa al oeste) | decimal | grados este |
| `runup_m` | Run-up observado | decimal | m |
| `tiempo_arr_min` | Tiempo de arribo después del sismo | entero | min |
| `fuente` | Referencia declarada en la tabla: Herd et al. 1981 o NOAA NGDC | texto | |

No hay valores faltantes. Cuatro estaciones son comparables con la simulación (Tumaco muelle, Tumaco playa, Bocagrande y Esmeraldas); las demás se excluyen y se declara en el cuaderno 3.

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
