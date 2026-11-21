"""Dibuja el flujo de un cuaderno de la serie CRC con el diseño de la figura
«Flujo de evaluación multiamenaza» del libro de Leticia
(https://mromerot.github.io/leticia/book/conceptos/marco-riesgo/): franjas de color por
etapa con su rótulo a la izquierda, paralelogramos para las entradas, cajas redondeadas
para los procesos, rectángulos para los productos y una elipse para la síntesis.

Se usa desde un script por cuaderno que define `SPEC` y llama a `dibujar(SPEC, salida)`.
Escribe un SVG y, con `typst` (misma fuente que el PDF), un PNG a 220 ppi.

SPEC (todo en español, listas de líneas de texto):
  titulo, descripcion: para <title> y <desc> del SVG.
  entradas: 4 cajas [lineas, ...]                           (franja verde)
  amenaza / exposicion / vulnerabilidad: ver `Etapa` abajo   (franjas amarilla, celeste y azul)
  sintesis: elipse [lineas] y 3 salidas (titulo, subtitulo, glifo)  (franja roja)
  glifos: 'rampa' | 'barras' | 'lista' | 'onda'
"""
import subprocess
import tempfile
from pathlib import Path

TINTA = "#1c2733"
FUENTE = "Liberation Sans, Helvetica, Arial, sans-serif"
W, X0, XF = 720, 124, 712
CX = (X0 + XF) / 2
VERDE, AMARILLO, CELESTE, AZUL, ROJO = (
    ("#cfe8a9", "#f3fae5"), ("#fff3a0", "#fffde8"), ("#8fd3f4", "#e6f6fd"),
    ("#86b6dc", "#e9f2fa"), ("#ff9a8f", "#ffffff"),
)
CW, CG = 186, 15
XS3 = [X0 + i * (CW + CG) for i in range(3)]


def dibujar(spec, salida_svg, salida_png):
    out = []

    def esc(t):
        return t.replace("&", "&amp;").replace("<", "&lt;")

    def texto(x, y, lineas, size=11.5, peso=400, ancla="middle", opacidad=None, alto=14.0):
        y0 = y - alto * (len(lineas) - 1) / 2 + size * 0.35
        extra = f' opacity="{opacidad}"' if opacidad else ""
        for i, l in enumerate(lineas):
            out.append(f'<text x="{x}" y="{y0 + i * alto:.1f}" font-size="{size}" font-weight="{peso}" '
                       f'text-anchor="{ancla}" fill="{TINTA}"{extra}>{esc(l)}</text>')

    def franja(y, h, color, etapa, titulo):
        out.append(f'<rect x="0" y="{y}" width="{W}" height="{h}" fill="{color[0]}"/>')
        texto(12, y + 20, [etapa], size=10.5, ancla="start", opacidad=".65")
        texto(12, y + 40 + 8.5 * (len(titulo) - 1), titulo, size=14, peso=700, ancla="start", alto=17)

    def caja(x, y, w, h, lineas, relleno, forma="redonda", discontinua=False, size=11.5):
        borde = "#7a2a05" if discontinua else TINTA
        dash = ' stroke-dasharray="5 3"' if discontinua else ""
        if forma == "redonda":
            out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{relleno}" stroke="{borde}" stroke-width="1.2"{dash}/>')
        elif forma == "rect":
            out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{relleno}" stroke="{borde}" stroke-width="1.2"{dash}/>')
        else:
            s = 10
            out.append(f'<polygon points="{x + s},{y} {x + w},{y} {x + w - s},{y + h} {x},{y + h}" fill="{relleno}" stroke="{borde}" stroke-width="1.2"/>')
        texto(x + w / 2, y + h / 2, lineas, size=size)

    def linea(x1, y1, x2, y2, flecha=False, discontinua=False):
        dash = ' stroke-dasharray="4 3"' if discontinua else ""
        marca = ' marker-end="url(#ar)"' if flecha else ""
        out.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{TINTA}" stroke-width="1.2"{dash}{marca}/>')

    # Etapa 1: entradas
    e1 = spec["entradas"]
    franja(0, 112, VERDE, e1["etapa"], e1["titulo"])
    pw, pg = 137, 13
    xs4 = [X0 + i * (pw + pg) for i in range(4)]
    for x, l in zip(xs4, e1["cajas"]):
        caja(x, 16, pw, 52, l, VERDE[1], "paralelogramo", size=10.5)
        linea(x + pw / 2, 68, x + pw / 2, 86)
    linea(xs4[0] + pw / 2, 86, xs4[3] + pw / 2, 86)

    # Etapa 2: tres cadenas proceso -> producto y una caja que las reúne
    e2 = spec["amenaza"]
    y2 = 112
    franja(y2, 252, AMARILLO, e2["etapa"], e2["titulo"])
    for x, c, p, q in zip(XS3, e2["cabeceras"], e2["procesos"], e2["productos"]):
        linea(x + CW / 2, 86, x + CW / 2, y2 + 20)
        texto(x + CW / 2, y2 + 30, [c], size=11, peso=700)
        caja(x, y2 + 42, CW, 58, p, AMARILLO[1])
        linea(x + CW / 2, y2 + 100, x + CW / 2, y2 + 124, flecha=True)
        caja(x, y2 + 124, CW, 60, q, "#ffffff", "rect")
        linea(x + CW / 2, y2 + 184, x + CW / 2, y2 + 198)
    linea(XS3[0] + CW / 2, y2 + 198, XS3[2] + CW / 2, y2 + 198)
    linea(CX, y2 + 198, CX, y2 + 208, flecha=True)
    caja(X0, y2 + 208, XF - X0, 32, e2["resumen"], "#ffffff", "rect")

    def franja_tres(y, color, e, flecha_entrada_desde):
        franja(y, 122, color, e["etapa"], e["titulo"])
        linea(CX, flecha_entrada_desde, CX, y + 12, flecha=True) if flecha_entrada_desde is not None else None
        for i, (x, l) in enumerate(zip(XS3, e["cajas"])):
            pend = i in e.get("pendientes", ())
            caja(x, y + 12, CW, 46, l, color[1], discontinua=pend)
            linea(x + CW / 2, y + 58, x + CW / 2, y + 70, discontinua=pend)
        linea(XS3[0] + CW / 2, y + 70, XS3[2] + CW / 2, y + 70)
        caja(X0, y + 78, XF - X0, 32, e["resumen"], "#ffffff", "rect")

    y3 = y2 + 252
    franja_tres(y3, CELESTE, spec["exposicion"], y2 + 240)
    y4 = y3 + 122
    franja_tres(y4, AZUL, spec["vulnerabilidad"], None)

    # Etapa 5: síntesis y tres productos
    s = spec["sintesis"]
    y5 = y4 + 122
    franja(y5, 168, ROJO, s["etapa"], s["titulo"])
    linea(CX, y4 + 110, CX, y5 + 14, flecha=True)
    out.append(f'<ellipse cx="{CX}" cy="{y5 + 40}" rx="236" ry="26" fill="#ffffff" stroke="{TINTA}" stroke-width="1.2"/>')
    texto(CX, y5 + 40, s["elipse"])
    for i, (x, (t, sub, glifo)) in enumerate(zip(XS3, s["salidas"])):
        linea(x + CW / 2, y5 + 62 if i != 1 else y5 + 66, x + CW / 2, y5 + 88, flecha=True)
        out.append(f'<rect x="{x}" y="{y5 + 88}" width="{CW}" height="70" fill="#ffffff" stroke="{TINTA}" stroke-width="1.2"/>')
        texto(x + CW / 2, y5 + 102, [t], size=11, peso=700)
        texto(x + CW / 2, y5 + 146, [sub], size=10)
        gy, gx = y5 + 114, x + CW / 2
        if glifo == "rampa":
            for k, c in enumerate(["#e6f6fd", "#8fd3f4", "#4aa3d8", "#2a6fb0", "#14437a"]):
                out.append(f'<rect x="{gx - 45 + k * 18}" y="{gy}" width="16" height="16" fill="{c}" stroke="{TINTA}" stroke-width=".6"/>')
        elif glifo == "barras":
            for k, h in enumerate([8, 16, 12, 4]):
                out.append(f'<rect x="{gx - 36 + k * 20}" y="{gy + 20 - h}" width="14" height="{h}" fill="#b2182b" opacity=".8"/>')
            linea(gx - 40, gy + 20, gx + 44, gy + 20)
        elif glifo == "lista":
            for k, w in enumerate([60, 44, 28]):
                out.append(f'<rect x="{gx - 30}" y="{gy + k * 7}" width="{w}" height="5" fill="#86b6dc" stroke="{TINTA}" stroke-width=".5"/>')
        elif glifo == "onda":
            pts = " ".join(f"{gx - 40 + k * 4},{gy + 10 - 9 * __import__('math').sin(k / 2.2) * __import__('math').exp(-k / 14):.1f}" for k in range(21))
            out.append(f'<polyline points="{pts}" fill="none" stroke="#b2182b" stroke-width="1.4"/>')
            linea(gx - 40, gy + 10, gx + 40, gy + 10)

    H = y5 + 168
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" '
           f'aria-labelledby="t d" font-family="{FUENTE}">\n<title id="t">{esc(spec["titulo"])}</title>\n'
           f'<desc id="d">{esc(spec["descripcion"])}</desc>\n'
           f'<defs><marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
           f'<path d="M0,0 L10,5 L0,10 z" fill="{TINTA}"/></marker></defs>\n') + "\n".join(out) + "\n</svg>\n"
    salida_svg, salida_png = Path(salida_svg), Path(salida_png)
    salida_svg.parent.mkdir(parents=True, exist_ok=True)
    salida_svg.write_text(svg, encoding="utf-8")
    with tempfile.TemporaryDirectory() as tmp:
        (Path(tmp) / "f.svg").write_text(svg, encoding="utf-8")
        (Path(tmp) / "f.typ").write_text(f'#set page(width: {W}pt, height: {H}pt, margin: 0pt)\n#image("f.svg", width: 100%)\n')
        subprocess.run(["typst", "compile", "--ppi", "220", str(Path(tmp) / "f.typ"), str(salida_png)], check=True)
    print("escrito", salida_png, f"({W}x{H})")
