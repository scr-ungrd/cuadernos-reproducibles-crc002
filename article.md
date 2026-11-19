---
title: Simulación del Tsunami de Tumaco de 1979 con Google Colab
subtitle: Propagación del tsunami del 12 de diciembre de 1979 (Mw 8,3) con una fuente de Okada y aguas someras no lineales con fricción de Manning en Google Colab
---

+++ {"no-pdf": true}

[![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/scr-ungrd/cuadernos-reproducibles-crc002/blob/main/notebooks/03-visualization.ipynb)
[![Abrir en Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/scr-ungrd/cuadernos-reproducibles-crc002/main?filepath=notebooks/03-visualization.ipynb)

+++

---

:::{danger} Ejercicio sin validar: no usar para tomar decisiones
Este cuaderno **no ha sido validado por una persona experta** en modelación de tsunamis. Es un ejercicio de reproducibilidad y de aprendizaje. Sus resultados **no deben usarse para tomar decisiones** de gestión del riesgo, ordenamiento territorial, diseño de obras, planes de evacuación ni alertas.

Falta, como mínimo: la revisión por una persona experta; la distribución de deslizamiento real del evento (la geometría de la falla es un supuesto); la validación contra observaciones de 1979, que hoy se contradicen entre fuentes (Herd et al., 1981 y NOAA/NGDC); y una malla y una topografía finas en la costa (a 450 m la inundación que calcula el modelo no lineal es solo indicativa y las amplitudes simuladas son poco confiables).
:::

+++ {"part": "abstract"}

El 12 de diciembre de 1979 un terremoto de la zona de subducción colombo-ecuatoriana generó un tsunami que causó cerca de 452 muertes en Nariño {cite:p}`escobar2020tsunami`.
Este trabajo presenta una simulación reproducible de su propagación en tres cuadernos de Google Colab que corren en CPU. La versión 2 reemplazó la onda en N calibrada de la versión 1 por la
deformación del fondo de una falla rectangular calculada con el modelo de Okada {cite:p}`okada1985` (Mw 8,3; geometría supuesta), y el esquema de Lax-Friedrichs por una malla
escalonada que no añade difusión numérica. La **versión 3** resuelve las ecuaciones de aguas someras **no lineales con fricción de Manning y celda seca**, en NumPy y en CPU, con un diseño inspirado en {cite:t}`madden2023` que no usa sus TPU ni su esquema numérico. La simulación cubre 110 minutos sobre un dominio de unos 480 × 480 km y 450 m de resolución. **El tiempo de llegada a Tumaco es poco sensible a la resolución y a los parámetros de la falla (19 a 25 min) y coincide en orden de magnitud con los 22 min que modela TUNAMI-N2 {cite:p}`avila2026`; las amplitudes dependen mucho de la fuente (2,3 a 4,6 m en la celda de mar de Tumaco según el caso, con las ecuaciones lineales) y el modelo no lineal del caso base da 3,7 m, de 1,6 a 2,0 veces los 1,9–2,3 m publicados para la isla {cite:p}`escobar2020tsunami`. Las observaciones de 1979 no coinciden entre fuentes (en Tumaco, 0,8 m según Herd et al. y 3 m según NOAA/NGDC), de modo que la comparación es un rango y no una validación.** El producto es un flujo de trabajo y una lectura de sus límites, no un mapa de amenaza.

+++ {"part": "keypoints"}

- La fuente es una dislocación elástica de Okada (1985) con Mw 8,3; la propagación usa aguas someras no lineales con fricción de Manning y celda seca en NumPy (se inspira en Madden et al., 2023, sin TPU ni su esquema)
- El tiempo de llegada a Tumaco cambia poco (19 a 25 min) con la resolución y los parámetros de la falla y es del orden de los 22 min de TUNAMI-N2
- Las amplitudes simuladas (3,7 m en la celda de Tumaco con el modelo no lineal; 2,3 a 4,6 m con el lineal según la fuente) dependen de la fuente y superan entre 1,6 y 2,0 veces los 1,9–2,3 m publicados para la isla
- Herd et al. (1981) y NOAA/NGDC no coinciden en el run-up de 1979 (Tumaco: 0,8 frente a 3 m); no hay validación
- Es un ejercicio sin validar por una persona experta: no debe usarse para tomar decisiones

+++

## Introducción

### Contexto sísmico del Pacífico colombiano

La costa Pacífica colombiana está expuesta a fuentes cercanas en la zona de subducción de la placa de Nazca bajo la suramericana. En el siglo XX esa zona produjo cuatro terremotos
de Mw > 7,7, en 1906, 1942, 1958 y 1979; el mayor fue el del 31 de enero de 1906 (Mw > 8,4), y todos generaron tsunamis con daños y pérdida de vidas en la costa de Colombia y Ecuador {cite:p}`escobar2020tsunami`.
Los eventos de 1906 y 1979 fueron desastres, el segundo grave para Tumaco {cite:p}`ungrd2019atlas`. Tumaco es además el municipio con mayor población expuesta y probabilidad de pérdidas por tsunami
del país {cite:p}`ungrd2019atlas`.

### El evento del 12 de diciembre de 1979

El sismo de 1979 se estima en Mw 8,3 (Yoshimoto et al., 2017, citado por {cite:t}`escobar2020tsunami` y {cite:t}`avila2026`; la versión 1 de este cuaderno usaba 8,2). El escenario de 1979 de Poveda y Pulido (2019) se definió invirtiendo ondas P telesísmicas {cite:p}`escobar2020tsunami`. En el departamento de Nariño
causó unas 452 muertes y 1 011 heridos, y destruyó cerca de 3 080 viviendas (Ramírez y Goberna, 1980, citado por {cite:t}`escobar2020tsunami`). El epicentro que usa este cuaderno (1,584° N, 79,386° O, a
unos 80 km al suroeste de Tumaco, con 33 km de profundidad asignada) es el hipocentro preliminar del NEIS que publican {cite:t}`herd1981` en su tabla 1.

### Objetivo y alcance

1. **Demostrar** que la propagación de un tsunami histórico puede simularse con código propio, en NumPy puro y en la CPU gratuita de Colab.
2. **Anclar la fuente en la física** (dislocación elástica con Mw de la literatura) en lugar de calibrarla, y medir qué tan lejos queda el resultado de las observaciones y de otros modelos.
3. **Declarar lo que el modelo no puede decir**, para que el cuaderno sirva como paso previo al análisis de amenaza de una ciudad y no se confunda con él.

### Relación con Madden et al. (2023)

Este cuaderno se concibió para reproducir en Google Colab, con el escenario de Tumaco, el trabajo de {cite:t}`madden2023`. Ellos resuelven las ecuaciones de aguas someras no lineales con volúmenes finitos (reconstrucción WENO de quinto orden y Runge-Kutta de tercer orden) en las unidades de procesamiento tensorial (TPU) de Google, con el código `tsunamiTPUlab` (Python y TensorFlow, licencia Apache 2.0), y calculan la inundación de Crescent City (California) a 8 m de resolución, que contrastan con GeoClaw. **Este cuaderno se inspira en ese trabajo, pero no lo reproduce.** Difiere en tres aspectos:

1. **No usa TPU ni TensorFlow.** Ejecutar `tsunamiTPUlab` exige un proyecto de Google Cloud y un depósito de almacenamiento de pago, lo que contradice el requisito de la serie de que cualquier persona pueda ejecutar los cuadernos sin cuenta ni costo (aquí corren en la CPU estándar de Colab y en Binder). Además, con una malla de 450 m y 110 minutos de simulación el problema cabe en una CPU: la ventaja de la TPU aparece con mallas de decenas de millones de celdas, que este escenario no tiene.
2. **No usa su esquema numérico.** La versión 2 resolvía las ecuaciones lineales. La versión 3 resuelve las **no lineales con fricción de Manning y celda seca**, pero con diferencias finitas en malla escalonada, advección contra-corriente de primer orden y forma de velocidad (no conservativa). Eso no representa la rotura ni los resaltos hidráulicos que un esquema WENO5 conservativo sí puede capturar. No se probó el código de Madden et al. ni se comparó con sus resultados.
3. **No reproduce su caso ni su resolución.** Ellos usan un modelo de elevación de 4 m para Crescent City; aquí el modelo de elevación disponible para Tumaco es de 15″ (unos 450 m). El único producto de GEM-15 (Google, 15 m) que se revisó el 2026-11-18 tiene dato en cerca del 2 % de un recorte de 44 × 44 km alrededor de Tumaco y en ninguna celda de la ciudad (la revisión no se versionó), así que no sirve para esta zona. La comparación con GeoClaw tampoco se hizo: se verifica el solver con soluciones exactas (incluido el cuenco parabólico que ellos también usan) y con las observaciones de 1979.

De ese trabajo se conservan la formulación no lineal con fricción de Manning, el tratamiento de celda seca y la prueba del cuenco parabólico. Para una inundación a la escala del paper haría falta topografía y batimetría costera de unos 10 m, que no se tiene.

## Marco teórico

### De la ruptura al arribo: la cadena de modelación

El análisis de amenaza por tsunami de origen sísmico sigue una cadena de cuatro pasos: definir los escenarios sismotectónicos, calcular la deformación sísmica que fija las condiciones iniciales, propagar las ondas largas
en aguas someras y evaluar el impacto en la costa con información topo-batimétrica de distinta resolución {cite:p}`ungrd2019atlas`. Las modelaciones colombianas
de referencia aplican esa cadena: Guapi con TUNAMI-N2, deformación de Okada y batimetría GEBCO {cite:p}`sanchez2023guapi`; Tumaco y Buenaventura con distribuciones de deslizamiento
de banda ancha {cite:p}`escobar2020tsunami`. Este cuaderno implementa los pasos 1 a 3, con el paso 4 reducido a leer la elevación en celdas de mar cercanas a la costa.

La {numref}`Figura %s <fig-flujo>` resume esa cadena tal como la implementa este cuaderno: los datos y el escenario alimentan la dislocación de Okada, que fija la condición inicial; las ondas se propagan con aguas someras lineales y se leen en las celdas de mar cercanas a la costa.

:::{figure} images/flujo_tsunami.png
:label: fig-flujo
:alt: Flujo en cinco etapas: datos de entrada; escenario sísmico, dislocación de Okada y condición inicial; propagación con aguas someras lineales; lectura en celdas de mar cercanas a la costa; y tres productos del escenario determinista de Mw 8,3.
Flujo de modelación del tsunami de 1979, de los datos y el escenario sísmico a la lectura en la costa (adaptado del flujo de evaluación multiamenaza del libro de Leticia, para una sola amenaza). La línea discontinua marca lo que el cuaderno no calcula. LSWE, ecuaciones lineales de aguas someras; CFL, número de Courant-Friedrichs-Lewy; DEM, modelo digital de elevación. **La figura es de la versión 2:** en la versión 3 el paso 3 resuelve además las ecuaciones no lineales con fricción de Manning y celda seca, y el paso 4 incluye una inundación en tierra solo indicativa a 450 m.
:::

### Generación: la dislocación elástica de Okada

El movimiento súbito de una falla deforma el fondo marino. Para una falla rectangular de longitud $L$, ancho $W$, buzamiento $\delta$ y deslizamiento $D$ en un semiespacio elástico, {cite:t}`okada1985` da expresiones
cerradas del desplazamiento en superficie. Aquí solo interesa la componente vertical $u_z$, que se toma como la elevación inicial de la superficie del agua, $\eta_0 = u_z$, con velocidades nulas. Es la
aproximación habitual de generación instantánea y desacoplada; desprecia el filtro que impone la columna de agua a las deformaciones de longitud de onda corta y el aporte del desplazamiento horizontal sobre el talud.
El deslizamiento sale del momento sísmico, con $M_0 = 10^{1,5 M_w + 9,1}$ N·m y $D = M_0/(\mu L W)$.

### Propagación: ondas largas y aguas someras

Mientras la longitud de onda sea mucho mayor que la profundidad, la teoría de aguas someras describe la propagación {cite:p}`ungrd2019atlas`, y la celeridad depende solo de la profundidad en reposo $H$:

$$
c = \sqrt{g H}
$$

(unos 200 m/s, 700 km/h, sobre 4 000 m de profundidad). Las ecuaciones **no lineales** (NSWE) incluyen la advección, la fricción y el cambio de profundidad con la propia ola, y son las que permiten calcular la inundación en tierra. Las **lineales** (LSWE) suponen
amplitud pequeña frente a la profundidad y $H$ fija. Con $M = Hu$ y $N = Hv$:

$$
\frac{\partial \eta}{\partial t} + \frac{\partial M}{\partial x} + \frac{\partial N}{\partial y} = 0, \qquad
\frac{\partial M}{\partial t} + gH\frac{\partial \eta}{\partial x} = 0, \qquad
\frac{\partial N}{\partial t} + gH\frac{\partial \eta}{\partial y} = 0 .
$$

Valen en el mar abierto y en la plataforma profunda; cerca de la costa la amplitud deja de ser pequeña frente a la profundidad y las LSWE sobreestiman la elevación porque no disipan energía. **La elevación de un modelo lineal no es el run-up.**

La versión 3 resuelve las NSWE. Con la profundidad total $D = H + \eta$ y la velocidad $\mathbf{U} = (u, v)$:

$$
\frac{\partial \eta}{\partial t} + \nabla\cdot(D\mathbf{U}) = 0, \qquad
\frac{\partial \mathbf{U}}{\partial t} + (\mathbf{U}\cdot\nabla)\mathbf{U} + g\nabla\eta + \frac{g n^2 |\mathbf{U}|}{D^{4/3}}\,\mathbf{U} = 0,
$$

donde $n$ es el coeficiente de rugosidad de Manning. Se usa $n = 0{,}025$ s·m⁻¹ᐟ³ en todo el dominio, un valor típico que **no se calibró ni se verificó para esta costa**. El término de fricción solo importa en agua somera ($D^{-4/3}$), de modo que en el océano profundo las NSWE y las LSWE dan casi lo mismo.

### Esquema numérico

La versión 1 usaba Lax-Friedrichs en una malla colocada, un esquema de primer orden cuya difusión numérica atenuaba la ola, de modo que hubo que inflar la amplitud inicial. La versión 2 usa una **malla escalonada de Arakawa C con el esquema *forward-backward***:
$\eta$ en el centro de las celdas, los flujos en las caras, y los flujos se actualizan con el $\eta$ ya actualizado. Es un esquema clásico de diferencias finitas para aguas someras. En una onda plana de 35 km de longitud de onda que recorre
119 km, el esquema de la versión 1 conserva el 43 % de la amplitud y el escalonado el 99,96 % (prueba en el cuaderno 2). Las fronteras abiertas usan la condición de radiación $M = \pm\sqrt{gH}\,\eta$.

La **versión 3** conserva la malla escalonada y el paso *forward-backward* y añade: (i) la advección, con diferencias contra-corriente de primer orden y en forma de velocidad (no conservativa); (ii) la fricción de Manning, semi-implícita para que no invierta el flujo; y (iii) la **celda seca**: una cara solo transporta agua si el agua sobre el terreno más alto de sus dos celdas supera 1 cm, y un limitador impide sacar de una celda más agua de la que contiene. La cara que se activa hereda la velocidad de la vecina del lado mojado; sin ese paso el frente de mojado pierde impulso. Se verificó con el cuenco parabólico unidimensional contra su solución exacta (error relativo de la profundidad tras un periodo: ver cuaderno 2, sección 3b). La forma de velocidad no es conservativa y **no representa la rotura de la ola ni los resaltos hidráulicos**. Los arreglos son de 32 bits, lo que reduce el tiempo de ejecución a la mitad (los resultados coinciden con los de 64 bits en las estaciones a 0,01 m).

### Determinista frente a probabilista

Una simulación de un escenario es una amenaza **determinista**: dice qué pasaría con una fuente dada. La evaluación **probabilista** pondera muchas fuentes con su frecuencia y entrega la profundidad de inundación por periodo de retorno, que es lo que
hace falta para calcular la pérdida anual esperada {cite:p}`ungrd2019atlas`. Este cuaderno es de la primera clase. En el libro *Teoría y métodos de análisis de riesgos de desastres y climáticos*
([capítulo de tsunami](https://mromerot.github.io/teoria-riesgos/)) se explica cómo encaja cada tipo en el cálculo del riesgo.

## Metodología

### Datos y dominio

El dominio abarca de 0,2° S a 4,2° N y de 81,2° a 76,9° O (479 × 488 km), con 450 m de resolución en UTM 17N. Es mayor que el de la versión 1 (0,5–3,5° N, 79,5–77° O) por dos razones: el epicentro quedaba a 15 km de la
frontera oeste y Esmeraldas (Ecuador) estaba fuera. Los datos de elevación salen del mosaico global de DEM de NOAA/NCEI {cite:p}`noaa_dem_mosaic`. **La versión 1 los atribuía a GEBCO 2023 y ETOPO 2022; no lo son:** el enlace de GEBCO ya no responde y el servicio
entrega un mosaico de modelos de distinta procedencia. Una copia del recorte se versiona en `data/`. La reproyección conserva el norte arriba y el oeste a la izquierda; la versión 1 invertía el eje X al guardar el DEM, lo que espejaba los mapas.

### Escenario sísmico

La magnitud (Mw 8,3) es de la literatura; **la geometría es un supuesto**, porque no se tiene a mano el modelo de deslizamiento de Poveda y Pulido (2019) en que se basan {cite:t}`escobar2020tsunami` y {cite:t}`avila2026`.

| Parámetro | Valor | Estado |
|---|---|---|
| Mw | 8,3 | Literatura |
| Longitud × ancho | 200 × 80 km | Supuesto |
| Rumbo / buzamiento / ángulo de desplazamiento | 30° / 15° / 90° | Supuesto |
| Profundidad del borde superior | 12 km (el inferior, ~33 km) | Supuesto; el hipocentro de 33 km se ubica en el borde inferior |
| Rigidez / Poisson | 30 GPa / 0,25 | Valores típicos |
| Deslizamiento | 7,4 m | Derivado |

El modelo de Okada implementado reproduce a 1e-5 m una implementación independiente (pyrocko) en tres geometrías. La deformación inicial va de +3,1 m (levantamiento hacia el oeste, sobre la parte somera de la falla) a −1,3 m (hundimiento hacia la costa)
({numref}`fig-fuente`).

:::{figure} notebooks/fuente_okada.png
:label: fig-fuente
:alt: Deformación vertical del fondo por la falla de Okada
Deformación vertical del fondo (η inicial) del escenario de Mw 8,3. Líneas discontinuas: proyección de la falla. La estrella roja es el epicentro, en el punto medio del borde inferior de la falla (borde este).
:::

### Parámetros de la simulación

| Parámetro | Valor | Justificación |
|---|---|---|
| Malla | 1 065 × 1 084 celdas de 450 m | DEM de 15″ reproyectado |
| Paso de tiempo | 1 s | $\mathrm{CFL}=c_{\max}\,\Delta t\,\sqrt{2}/\Delta x = 0{,}70 < 1$ |
| Duración | 6 600 s (110 min) | Incluye la primera ola positiva observada en el mareógrafo de Buenaventura (99 min) y ondas reflejadas |
| Instantáneas | cada 240 s | 28 cuadros para la animación |
| Fricción | Manning, $n = 0{,}025$ | Valor típico, sin calibrar; las LSWE (comparación) no tienen fricción |
| Tiempo de ejecución | ~5,5 min (NSWE) y ~1 min (LSWE) para 110 min | CPU de un Apple M1; el cuaderno 2 completo toma unos 11 min |

### Estaciones y control de calidad de las observaciones

`data/observaciones_1979.csv` se reconstruyó en la versión 2.2 con la procedencia de cada valor. De los doce lugares, dos tienen run-up en **las dos fuentes y difieren por un factor de 2,4 a 3,8**: Tumaco (0,8 m según Herd et al., 1981, p. 442, sobre la posición previa de la marea alta; 3 m en el registro 9742 de NOAA/NGDC {cite:p}`noaa_tsunami_db`) y San Juan de la Costa (2,5 m frente a 6 m, registro 9745). Los demás son solo de NOAA/NGDC. Los valores de las dos fuentes **no se promedian**: se trabaja con el rango.
Solo hay dos tiempos: la primera ola positiva en el mareógrafo de Buenaventura (99 min; Herd et al.: 1 h 39 min) y el inicio del retroceso del mar en Esmeraldas (5 a 6 min). En Tumaco el mareógrafo quedó destruido y no hay hora de llegada. Para la primera ola se revisa la coherencia con una onda larga: con la distancia $d$ y el arribo $t$, la profundidad equivalente es $H_{eq}=(d/t)^2/g$ (unos 380 m en Buenaventura, plausible para una ruta de plataforma).

Cada estación se lee en la celda de mar más cercana con profundidad de al menos 10 m y a menos de 10 km. Buenaventura, por ser un mareógrafo, usa la de al menos 5 m a menos de 3 km. Quedan **siete estaciones comparables** de doce: Tumaco, San Juan de la Costa, Buenaventura, Esmeraldas, Isla Gorgona, Guapi y Vuelta Larga (estas dos últimas comparten celda). Limones, Iscuandé, El Charco, Timbiquí y El Barro quedan sin mar de 10 m a menos de 10 km y se excluyen.

## Resultados

### Elevación máxima

La elevación máxima en celdas de 10 m de profundidad o más es de 6,2 m con el modelo no lineal ({numref}`fig-max-eta`), frente a 8,8 m con el lineal. Se concentra en una franja sobre la falla y en la costa frente al epicentro, de Tumaco hacia el sur. En celdas de menos de 10 m el modelo no lineal llega a 7 m (el lineal llegaba a 40 m); con celdas de 450 m eso es amplificación en agua somera y no se interpreta.

:::{figure} notebooks/max_eta_map.png
:label: fig-max-eta
:alt: Elevación máxima de la ola
Elevación máxima de la superficie del mar en 110 min (NSWE, Manning 0,025). Izquierda: dominio completo, solo celdas de 10 m de profundidad o más. Derecha: plataforma de Tumaco (10–200 m).
:::

### Series de tiempo

Frente a Tumaco la primera señal es un descenso del nivel (la subsidencia cosísmica inicial y un valle previo a la ola); el primer ascenso mayor de 0,1 m llega a los 22 min y la cresta máxima (3,7 m) a los 28 min; el nivel baja hasta −3,3 m ({numref}`fig-timeseries`).
El vaivén persiste con fricción de Manning; es esperable en una bahía somera, donde la energía queda atrapada y se refleja, pero no se verificó con una malla más fina. En Esmeraldas el nivel ya es negativo en el instante inicial y el primer ascenso llega a los 11 min. En Buenaventura la celda de 5 m no registra ninguna ola mayor de 0,1 m en 110 min.

:::{figure} notebooks/time_series.png
:label: fig-timeseries
:alt: Series de tiempo en siete estaciones
Series de η en siete estaciones. Línea discontinua roja: tiempo observado (primera ola positiva en Buenaventura; inicio del retroceso en Esmeraldas); banda o línea roja horizontal: run-up observado, con el rango entre Herd et al. (1981) y NOAA/NGDC donde ambos existen.
:::

### Comparación con las observaciones y con otros modelos

| Estación | Run-up Herd (m) | Run-up NOAA/NGDC (m) | η máx. sim. (m) | η sim./Herd | η sim./NOAA |
|---|---|---|---|---|---|
| Tumaco | 0,8 | 3,0 | 3,7 | 4,6 | 1,2 |
| San Juan de la Costa | 2,5 | 6,0 | 1,5 | 0,59 | 0,25 |
| Isla Gorgona | — | 5,0 | 0,4 | — | 0,08 |
| Guapi | — | 2,0 | 0,4 | — | 0,21 |
| Vuelta Larga | — | 3,0 | 0,4 | — | 0,14 |

Con dos fuentes que se contradicen y pocos puntos **no se calcula un RMSE ni un R²**. Lo que sí se puede decir ({numref}`fig-validation`):

:::{figure} notebooks/validation.png
:label: fig-validation
:alt: Comparación de tiempos y amplitudes
Izquierda: tiempo observado y simulado de la primera ola positiva (solo Buenaventura). Derecha: run-up de Herd et al. (1981) y de NOAA/NGDC, y η máxima simulada en el mar; no son magnitudes equivalentes.
:::

- **Tiempos.** Los de las NSWE y las LSWE coinciden con diferencias menores de 0,5 min en todas las estaciones comparables. Solo hay dos tiempos observados. En Buenaventura la primera ola positiva se midió a los 99 min y el modelo **no produce ninguna ola mayor de 0,1 m** en 110 min en la celda de 5 m (la amplitud observada, 0,14 m, está apenas sobre ese umbral). En Esmeraldas el retroceso observado a los 5–6 min **coincide en signo** con el descenso que el modelo ya tiene en t = 0, pero el tiempo no es comparable porque la fuente es instantánea. En Tumaco no hay hora de llegada observada; los 22 min simulados coinciden con los de {cite:t}`avila2026`.
- **Amplitudes.** La razón entre η simulada y run-up va de 0,08 a 4,6 según la estación y la fuente: no hay un sesgo único. En Tumaco el modelo da 4,6 veces el valor de Herd y 1,2 veces el de NOAA/NGDC, y entre 1,6 y 2,0 veces las alturas máximas de 1,88–2,30 m que {cite:t}`escobar2020tsunami` obtienen para la isla de Tumaco con el escenario de 1979. En San Juan de la Costa queda por debajo de las dos fuentes y en Isla Gorgona, Guapi y Vuelta Larga entre 5 y 12 veces por debajo de NOAA/NGDC. Una celda de mar de 10 a 44 m de profundidad, a varios kilómetros de la coordenada, no representa un run-up, así que estas razones se leen como orden de magnitud.

### Sensibilidad

Con la malla de 900 m, que corre en 4 s con las LSWE, se varió un parámetro a la vez ({numref}`tbl-sens`). Esta tabla es de las **ecuaciones lineales**; la no linealidad y la fricción se analizan aparte ({numref}`tbl-sens-nswe`).

:::{table} Respuesta en la celda de Tumaco al variar un parámetro a la vez. «v1» son los parámetros documentados en la versión 1 (Mw 8,2; rumbo 10°; buzamiento 20°; 250 × 100 km).
:label: tbl-sens
| Variación | η máx. en Tumaco (m) | Arribo en Tumaco (min) |
|---|---|---|
| Resolución 450 → 900 m | 4,56 → 4,55 | 21,9 → 21,9 |
| Mw 8,3 → 8,2 (a 900 m) | 4,55 → 3,22 | 21,9 → 22,0 |
| Buzamiento 12° y 18° | 4,41–4,61 | 21,3–22,3 |
| Rumbo 20° y 40° | 3,86–3,90 | 18,9–23,4 |
| Longitud 150 y 250 km | 3,83–4,22 | 22,2 |
| Profundidad del borde superior 8 y 16 km | 4,40–4,49 | 21,7–22,0 |
| Parámetros de la v1 | 2,31 | 24,7 |
:::

La **resolución** casi no mueve la celda de Tumaco (de 4,56 a 4,55 m y sin cambio en el arribo), aunque en San Juan de la Costa pasa de 2,2 a 3,2 m porque la celda elegida cambia; la comparación por estación depende de esa elección. La **fuente** pesa mucho: entre el caso más pequeño (parámetros de la versión 1) y el más grande, la amplitud en Tumaco varía de 2,3 a 4,6 m. El arribo
es robusto, de 19 a 25 min en todos los casos.

:::{table} Respuesta a 900 m del modelo lineal y del no lineal con distinto coeficiente de Manning ($n$, s·m⁻¹ᐟ³; el intervalo es el habitual y **no está calibrado**). «Celdas inundadas» son las celdas de 900 m de tierra con más de 0,5 m de agua.
:label: tbl-sens-nswe
| Modelo | Tumaco η máx. (m) | Tumaco arribo (min) | San Juan de la Costa η máx. (m) | Guapi η máx. (m) | Celdas inundadas |
|---|---|---|---|---|---|
| LSWE (sin fricción) | 4,55 | 21,9 | 3,17 | 0,50 | 0 |
| NSWE, $n = 0{,}040$ | 3,45 | 21,9 | 1,76 | 0,36 | 78 |
| NSWE, $n = 0{,}025$ | 3,41 | 21,8 | 1,80 | 0,41 | 134 |
| NSWE, $n = 0{,}015$ | 3,38 | 21,8 | 1,81 | 0,46 | 184 |
| NSWE, sin fricción | 3,38 | 21,8 | 1,82 | 0,49 | 298 |
:::

La **no linealidad** reduce la amplitud en Tumaco de 4,55 a unos 3,4 m (−25 %) sin mover el arribo. La **fricción** casi no cambia la elevación en las celdas de mar de 10 m o más (3,38 a 3,45 m en Tumaco), pero sí el avance sobre tierra: el área inundada se reduce a menos de la tercera parte entre $n \approx 0$ y $n = 0{,}040$. Es coherente con que la fricción actúe donde la profundidad es pequeña, pero a 900 m las celdas inundadas solo sirven como indicador relativo.

### Animación de la propagación

La {numref}`fig-animation` muestra la propagación con el oeste a la izquierda y el norte arriba. El lóbulo de levantamiento nace sobre la falla, junto a la estrella, y se divide en una ola que viaja hacia la costa y otra hacia el océano abierto. La estrella
marca el epicentro; en la versión 1 el mapa estaba espejado y la fuente nacía a unos 200 km de ella.

:::{figure} notebooks/tsunami_propagation.gif
:label: fig-animation
:alt: Animación de la propagación del tsunami
Animación de la propagación del tsunami de Tumaco 1979 (NSWE de la versión 3, 28 cuadros, t = 0–108 min). Escala de color: η en metros (se omiten |η| < 0,1 m y celdas de menos de 10 m de profundidad). La estrella roja es el epicentro.
:::

## Alcance: qué se puede y qué no se puede concluir

**Lo que el cuaderno sí sustenta.**

- **El tiempo de llegada a Tumaco ronda los 20–25 min y es robusto.** Cambia poco con la resolución, con los parámetros supuestos (19 a 25 min), con la no linealidad y con la fricción (21,8 a 21,9 min a 900 m), y coincide con un modelo no lineal publicado {cite:p}`avila2026`. Para el análisis de riesgo de una ciudad es la cifra más útil: el tiempo disponible para evacuar de una fuente cercana es de minutos {cite:p}`ungrd2019atlas`,
  y aquí son del orden de 20.
- **La ola no es una sola.** Tras un descenso inicial llegan varias crestas durante al menos 30–45 min, y la máxima no es la primera. Un plan de evacuación no debe darse por terminado con el primer ascenso.
- **El flujo de trabajo es reproducible** y verificado: Okada contra una implementación independiente, onda plana contra la solución exacta, reposo exacto, conservación de la masa y cuenco parabólico contra su solución exacta para las NSWE, y fuente ligada al epicentro (pruebas automáticas).

**Lo que no sustenta.**

- **No es un mapa de amenaza.** Las NSWE de la versión 3 inundan la tierra, pero con celdas de 450 m (más grandes que la isla de Tumaco) y sin rotura de la ola la profundidad de inundación es solo indicativa. Las zonas seguras (por ejemplo, el umbral de 0,3 m que usa {cite:t}`avila2026`) requieren topografía y batimetría finas de las islas de Tumaco.
- **Las amplitudes no son confiables en valor absoluto.** Dependen mucho de una fuente cuya geometría es un supuesto y en Tumaco el caso base da de 1,6 a 2,0 veces lo publicado. Sirven para comparar escenarios entre sí, no para dimensionar obras ni tasas de daño.
- **No es una validación.** Las dos fuentes de run-up de 1979 se contradicen (factor de 2,4 a 3,8 donde coinciden), solo hay dos tiempos documentados y en uno de ellos (Buenaventura) el modelo no reproduce la ola. Una concordancia con cualquiera de las dos habría sido casual.

**Cómo entra en el cálculo del riesgo.** El producto de amenaza que necesita el cálculo es la profundidad de inundación por escenario o por periodo de retorno; este cuaderno aporta el paso de propagación y el tiempo de arribo. La
exposición (Tumaco concentra la mayor población expuesta del país {cite:p}`ungrd2019atlas`) y la vulnerabilidad física, con funciones de fragilidad como las comparadas para los edificios de Tumaco {cite:p}`paez2021tsunamifrag`, se aplican sobre
la inundación, no sobre la elevación en el mar.

## Instrucciones de reproducción

1. **Cuaderno 1** (`01-bathymetry.ipynb`): lee o descarga el DEM, lo reproyecta a UTM 17N y comprueba la orientación. Menos de 1 min.
2. **Cuaderno 2** (`02-simulation.ipynb`): escenario de Okada, solver, pruebas, simulación de 110 min y sensibilidad. Unos 11 min (las NSWE a 450 m toman unos 5,5 minutos).
3. **Cuaderno 3** (`03-visualization.ipynb`): mapas, series, control de calidad, comparación y animación. 1–2 min.

:::{note}
El 2026-11-18 los cuadernos 2 y 3 corrieron completos en un Apple M1, sin GPU y sin errores (cuaderno 2: 11 min; cuaderno 3: 12 s), pero en un entorno de trabajo existente y no en uno nuevo creado desde `environment.yml`; el cuaderno 1 no cambió desde la versión 2.2.2, que sí se ejecutó el 2026-11-17 en un entorno limpio. No se probó en Colab ni en Binder y no se midió el tiempo en una CPU de Colab (más lenta que un M1). Los cuadernos no necesitan TPU ni GPU. Si se abren en Colab, el cuaderno 2 requiere el DEM del cuaderno 1 o la copia de `data/`.
:::

## Limitaciones y trabajo futuro

1. **Esquema de las NSWE.** Primer orden en la advección y forma de velocidad (no conservativa): no representa la rotura ni los resaltos hidráulicos. Un esquema de volúmenes finitos conservativo de orden alto, como el de {cite:t}`madden2023`, y una comparación con GeoClaw o con `tsunamiTPUlab` serían el siguiente paso. El coeficiente de Manning (0,025) es un valor típico sin calibrar.
2. **Fuente.** Falla única de deslizamiento uniforme con geometría supuesta. Debe reemplazarse por la distribución de deslizamiento de Poveda y Pulido (2019) y verificar el epicentro, la profundidad y el mecanismo contra Herd et al. (1981) y Yoshimoto et al. (2017).
3. **Generación instantánea y desacoplada**, sin filtro por la columna de agua ni desplazamiento horizontal sobre el talud.
4. **Resolución.** 450 m no capturan las islas de Tumaco ni el estuario; hacen falta mallas anidadas con batimetría local.
5. **Observaciones.** Herd et al. (1981) y la base de NOAA/NGDC no coinciden en el run-up (Tumaco: 0,8 frente a 3 m; San Juan de la Costa: 2,5 frente a 6 m). Falta consultar los informes que están detrás de los registros de NOAA (referencia vertical y tipo de medición), el informe de Pararas-Carayannis (1980) que cita Herd et al. y registros mareográficos de Tumaco y Buenaventura; con ellos se podría reducir el rango y validar de verdad.
6. **Probabilista.** Un análisis para el cálculo de la pérdida anual esperada necesita muchas fuentes con sus frecuencias.

## Conclusiones

Se simuló la propagación del tsunami de Tumaco de 1979 con una fuente de Okada y aguas someras no lineales con fricción de Manning y celda seca, sin parámetro de calibración, en NumPy y en CPU; el diseño se inspira en {cite:t}`madden2023` pero no usa TPU ni su esquema. El tiempo de arribo a Tumaco (19–25 min) es robusto y consistente con un modelo publicado;
la amplitud es sensible a una geometría de falla que aún es un supuesto y en Tumaco da de 1,6 a 2,0 veces lo publicado (la no linealidad la reduce entre 19 % y 25 % respecto al modelo lineal). Las observaciones de 1979 se contradicen entre fuentes y en Buenaventura el modelo no reproduce la ola, así que no hay validación. La versión 2 corrigió los errores de la versión 1 (mapa espejado, fuente desligada del epicentro, atribución de los datos, estaciones fuera del dominio) y deja
explícito lo que falta para pasar de un escenario de propagación a un análisis de amenaza.

## Disponibilidad de datos y código

- **Código:** <https://github.com/scr-ungrd/cuadernos-reproducibles-crc002> (licencia MIT; el constructor de los cuadernos está en `scripts/construir_cuadernos.py`).
- **Elevación:** recorte de {cite:t}`noaa_dem_mosaic` en `data/dem_tumaco_noaa_15s.tif`.
- **Observaciones históricas:** `data/observaciones_1979.csv` (12 lugares, con la procedencia de cada valor: Herd et al., 1981 y NOAA/NGDC, que no coinciden) y los registros de NOAA/NGDC consultados el 2026-11-16 en `data/noaa_runups_1979.csv` (doi:10.7289/V5PN93H7).
- **Metadatos:** las fuentes y sus condiciones están en `metadata/sources.csv`, el catálogo y el diccionario de datos en `metadata/`, las sumas de verificación en `metadata/descargas.csv` y los metadatos RDLS de las observaciones en `metadata/rdls/`. La declaración completa está en `DATA_STATEMENT.md`.
- **Licencias:** código bajo MIT; texto y figuras bajo CC BY 4.0. La licencia del mosaico de NOAA/NCEI y de las observaciones está por confirmar.
- **DOI:** [10.5281/zenodo.24324555](https://doi.org/10.5281/zenodo.24324555) (versión 2.2.2); el DOI de todas las versiones es [10.5281/zenodo.24322477](https://doi.org/10.5281/zenodo.24322477).

## Declaración de uso de inteligencia artificial

El desarrollo de este cuaderno contó con la asistencia de Claude Sonnet 5.5 (Anthropic), según el historial de commits del repositorio. El detalle de los usos y de la revisión humana se registra en `AI_USE.md`.

```{bibliography}
```
