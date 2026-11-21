"""Figura del flujo de modelación del CRC002 (cadena de modelación del tsunami de 1979).

Escribe `images/flujo_tsunami.svg` y `images/flujo_tsunami.png` (la ruta del PNG es la
que usa `article.md`). Requiere `typst`. Uso:  python scripts/figura_flujo.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from flujo_lib import dibujar

RAIZ = Path(__file__).resolve().parents[1]

SPEC = dict(
    titulo="Flujo de modelación del tsunami de Tumaco de 1979",
    descripcion=("Cinco etapas: datos de entrada; escenario sísmico, dislocación de Okada y condición inicial; "
                 "propagación con aguas someras lineales; lectura en celdas de mar cercanas a la costa; "
                 "y tres productos del escenario determinista de Mw 8,3."),
    entradas=dict(etapa="ENTRADAS", titulo=["Datos de", "entrada"], cajas=[
        ["DEM de NOAA/NCEI", "(450 m, UTM 17N)"], ["Magnitud Mw 8,3", "(literatura)"],
        ["Geometría de la falla", "(supuesto)"], ["Observaciones de 1979", "(NOAA/NGDC, Herd)"]]),
    amenaza=dict(etapa="PASOS 1 Y 2", titulo=["Fuente"],
                 cabeceras=["Escenario sísmico", "Dislocación de Okada", "Condición inicial"],
                 procesos=[["Magnitud de la literatura;", "geometría supuesta", "(200 × 80 km, buzam. 15°)"],
                           ["Deformación elástica", "del fondo marino", "(rigidez 30 GPa, Poisson 0,25)"],
                           ["Deformación vertical = η", "inicial en la malla", "de 450 m"]],
                 productos=[["Falla rectangular:", "rumbo 30°, desplaz. 90°,", "deslizamiento de 7,4 m"],
                            ["Contraste con otra", "implementación (pyrocko):", "diferencia < 1e-5 m"],
                            ["De +3,1 m (levantamiento)", "a −1,3 m (hundimiento)"]],
                 resumen=["η inicial en un dominio de 479 × 488 km (0,2° S a 4,2° N; 81,2° a 76,9° O)"]),
    exposicion=dict(etapa="PASO 3", titulo=["Propagación"], cajas=[
        ["Aguas someras lineales", "(LSWE), c = √(gH)"], ["Malla de Arakawa C y", "esquema forward-backward"],
        ["Paso de 1 s durante", "6 600 s (110 min)"]],
        resumen=["Propagación de η en la malla de 1 065 × 1 084 celdas (CFL = 0,70)"]),
    vulnerabilidad=dict(etapa="PASO 4", titulo=["Lectura en", "la costa"], cajas=[
        ["Celdas de mar de 10 m", "de profundidad o más"], ["Series de tiempo", "en estaciones"],
        ["Pendiente: inundación en", "tierra (no lineal, run-up)"]], pendientes=(2,),
        resumen=["Elevación máxima y llegada de la ola en las celdas de mar cercanas a la costa"]),
    sintesis=dict(etapa="RESULTADO", titulo=["Escenario", "determinista"],
                  elipse=["Escenario de Mw 8,3: un rango de elevaciones,", "no una validación del evento de 1979"],
                  salidas=[("Mapa de elevación máxima", "110 min, LSWE", "rampa"),
                           ("Series de tiempo", "y animación", "onda"),
                           ("Comparación y sensibilidad", "con 1979 y con la v1", "barras")]),
)

if __name__ == "__main__":
    dibujar(SPEC, RAIZ / "images" / "flujo_tsunami.svg", RAIZ / "images" / "flujo_tsunami.png")
