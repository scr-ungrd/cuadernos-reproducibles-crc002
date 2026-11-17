"""Pruebas automáticas de los datos de `data/`: estructura, duplicados, rangos y valores esperados.

Uso:  python scripts/probar_datos.py
Falla con un mensaje claro si un CSV está mal formado o si un valor sale de su rango. Se ejecuta en el despliegue antes de los cuadernos.
"""
import csv
import sys
from pathlib import Path

import pandas as pd

DATOS = Path(__file__).resolve().parent.parent / "data"
errores = []


def comprobar(cond, mensaje):
    if not cond:
        errores.append(mensaje)


def campos_por_fila(ruta):
    """Número de campos de cada fila según el módulo csv (detecta comas sin comillas)."""
    with open(ruta, newline="", encoding="utf-8") as f:
        return {len(fila) for fila in csv.reader(f)}


for nombre, columnas in {
    "observaciones_1979.csv": ["estacion", "lat", "lon", "runup_herd_m", "runup_noaa_m", "t_obs_min", "t_obs_tipo", "id_noaa", "notas"],
    "noaa_runups_1979.csv": ["id_noaa", "lugar", "pais", "lat", "lon", "runup_m", "dist_fuente_km", "tipo_medicion", "primer_movimiento", "dudoso"],
}.items():
    ruta = DATOS / nombre
    comprobar(len(campos_por_fila(ruta)) == 1, f"{nombre}: las filas no tienen el mismo número de campos (¿coma sin comillas?)")
    d = pd.read_csv(ruta)
    comprobar(list(d.columns) == columnas, f"{nombre}: columnas distintas de las esperadas")
    comprobar(not d.duplicated().any(), f"{nombre}: hay filas duplicadas")
    comprobar(len(d) == 12, f"{nombre}: se esperaban 12 filas y hay {len(d)}")
    comprobar(d.lat.between(-3, 5).all() and d.lon.between(-82, -76).all(), f"{nombre}: coordenadas fuera del dominio")

obs = pd.read_csv(DATOS / "observaciones_1979.csv")
comprobar(obs[["runup_herd_m", "runup_noaa_m"]].stack().between(0, 20).all(), "observaciones_1979.csv: run-up fuera de 0 a 20 m")
comprobar(set(obs.t_obs_tipo.dropna()) <= {"primera_ola_positiva", "retroceso"}, "observaciones_1979.csv: tipo de tiempo desconocido")
comprobar(obs.id_noaa.is_unique, "observaciones_1979.csv: id_noaa repetido")
comprobar(float(obs.set_index("estacion").loc["Tumaco", "runup_herd_m"]) == 0.8, "observaciones_1979.csv: Tumaco debe tener 0,8 m según Herd et al.")

if errores:
    print("FALLAN LAS PRUEBAS DE DATOS:")
    print("\n".join(" - " + e for e in errores))
    sys.exit(1)
print("Pruebas de datos: todas correctas.")
