# Contraste de los valores de Herd et al. (1981) con el artículo

Fecha: 2026-11-17. Fuente: Herd, D. G., Youd, T. L., Meyer, H., Arango, J. L., Person, W. J., y Mendoza, C. (1981). The great Tumaco, Colombia earthquake of 12 December 1979. *Science, 211*(4481), 441–445. <https://doi.org/10.1126/science.211.4481.441>. Páginas 442 (texto y figura 1) y 443 (tabla 1).

**Método.** Los valores los extrajo un modelo de lenguaje (Claude Sonnet 5.5, con Claude Code) leyendo el PDF que aportó la persona autora. El 2026-11-17 el mismo modelo volvió a leer las páginas 442 y 443 como imagen (el PDF es un escaneo sin texto) y comparó cada valor de `data/observaciones_1979.csv` y de la documentación. Es un contraste del 100 % de los valores, pero **no es independiente**: lo hizo el mismo sistema que los transcribió. Una persona debe repetirlo (criterio U09 del instructivo de uso de IA).

| Valor | En el repositorio | En el artículo | Resultado |
|---|---|---|---|
| Tumaco: run-up | 0,8 m | «only about 0.8 m above the former high-tide position» | Coincide |
| Tumaco: rango de marea | 1,3 m | «approximately 1.3 m» | Coincide |
| Tumaco: mareógrafo | destruido, sin hora | destruido por el temblor | Coincide |
| San Juan: run-up | 2,5 m | «nearly 2.5 meters above the former high-tide position» | Coincide |
| San Juan: agua en la aldea | más de 2 m | «more than 2 meters of water» | Coincide |
| San Juan: olas | 3 a 4, 10 a 15 min tras el retroceso | «three to four waves», «10 to 15 minutes» | Coincide |
| Buenaventura: primera ola | 4:38 h, 1 h 39 min (99 min) | «4:38 a.m., 1 hour and 39 minutes after the main shock» | Coincide |
| Esmeraldas: retroceso | 5 a 6 min | «only 5 to 6 minutes after the earthquake» | Coincide |
| Isla Gorgona | descenso del suelo de 0,8 m | «0.8-m rise of sea level»; figura 1: 80 cm | Coincide |
| Guapi: hundimiento | **40 a 45 cm** | figura 1 (recuadro): Guapi **25–30 cm**; 40–45 cm es Bozán | **Error corregido** |
| El Charco e Iscuandé | reportes falsos | «were false» | Coincide |
| Epicentro | 1,584° N, 79,386° O | tabla 1: 1.584°N, 79.386°W | Coincide |
| Hora origen | 7:59:04 UTC | tabla 1: 7:59:04.3 | Coincide |
| Magnitud de la tabla 1 | no se usa | mb 6,4; Ms 7,9 | No aplica |

**Resultado.** 13 valores comparados con el artículo; 1 error de transcripción (Guapi, 40–45 en lugar de 25–30 cm), corregido en `data/observaciones_1979.csv`. Tasa de error: 1 de 13 (7,7 %). El valor corregido es un hundimiento del suelo citado solo en `notas`; no entra en ninguna comparación con el modelo y no cambia los resultados.
