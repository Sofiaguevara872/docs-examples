"""Presupuesto Logo e Isologo - Bengar Calisthenics (Paloma GB).

Replica el diseño de "Presupuesto_Pack_3_Concerts_Delta_School_2026.pdf".
La referencia salió de HTML impreso en Chrome (1 px CSS = 0.75 pt), así que las
formas giradas se dibujan en ese mismo espacio en px con las matrices `cm`
originales; los textos se ubican en pt, con `top` = baseline medido desde el
borde superior de la hoja.

Uso:  python3 presupuesto.py [salida.pdf]
"""
import os
import sys

from reportlab.lib.colors import HexColor, white
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = A4
PX = 0.75  # 1 px CSS en pt

# Fuentes: @fontsource/poppins y @fontsource/inter (.woff -> .ttf con fontTools).
FONTS = {
    "PB": "Poppins-ExtraBold",        # 800
    "PBI": "Poppins-ExtraBoldItalic",  # 800 italic
    "PK": "Poppins-Black",            # 900
    "IR": "Inter-Regular",            # 400
    "IS": "Inter-SemiBold",           # 600
}
for name in FONTS.values():
    pdfmetrics.registerFont(TTFont(name, os.path.join(HERE, "fonts", name + ".ttf")))
PB, PBI, PK, IR, IS = (FONTS[k] for k in ("PB", "PBI", "PK", "IR", "IS"))

INK = HexColor("#111111")      # negro de encabezado, textos y cuadros
SHAPE = HexColor("#2b2b2b")    # forma gris del encabezado
GREY_77 = HexColor("#777777")  # etiquetas y líneas de detalle
GREY_88 = HexColor("#888888")  # subtítulos de PARA / REFERENCIA
GREY_BB = HexColor("#bbbbbb")  # valores de Fecha / Vigencia
GREY_AA = HexColor("#aaaaaa")  # etiqueta DATOS DE PAGO
GREY_33 = HexColor("#333333")  # viñetas de segundo nivel
RULE = HexColor("#dddddd")     # reglas finas

ML, MR = 42.52, 552.76  # márgenes de 15 mm


# ---------------------------------------------------------------- primitivas
def width(s, font, size, cs=0.0):
    return pdfmetrics.stringWidth(s, font, size) + cs * (len(s) - 1)


def text(c, x, top, s, font, size, color, cs=0.0, align="left"):
    """Texto en una línea; saveState/restoreState evita arrastrar charSpace."""
    w = width(s, font, size, cs)
    if align == "right":
        x -= w
    c.saveState()
    c.setFillColor(color)
    c.setFont(font, size)
    c.drawString(x, H - top, s, charSpace=cs)
    c.restoreState()
    return x, w


def rect(c, x, top, w, h, color):
    c.saveState()
    c.setFillColor(color)
    c.rect(x, H - top - h, w, h, stroke=0, fill=1)
    c.restoreState()


def diamond(c, cx, cy_top, r=4.01):
    c.saveState()
    c.setFillColor(INK)
    p = c.beginPath()
    y = H - cy_top
    p.moveTo(cx, y + r)
    p.lineTo(cx + r, y)
    p.lineTo(cx, y - r)
    p.lineTo(cx - r, y)
    p.close()
    c.drawPath(p, stroke=0, fill=1)
    c.restoreState()


def ring(c, cx, cy_top, r_out=2.55, r_in=1.70):
    c.saveState()
    c.setStrokeColor(INK)
    c.setLineWidth(r_out - r_in)
    c.circle(cx, H - cy_top, (r_out + r_in) / 2, stroke=1, fill=0)
    c.restoreState()


def px_space(c):
    """Pasa al espacio de la referencia: px CSS, origen arriba a la izquierda."""
    c.transform(1, 0, 0, -1, 0, H)
    c.scale(PX, PX)


def px_text(c, x, y, s, font, size_px, color, cs_em=0.0):
    """Texto dentro de un marco en px (y hacia abajo)."""
    c.saveState()
    c.translate(x, y)
    c.scale(1, -1)
    c.setFillColor(color)
    c.setFont(font, size_px)
    c.drawString(0, 0, s, charSpace=cs_em * size_px)
    c.restoreState()


# ---------------------------------------------------------------- encabezado
# Matrices `cm` y rectángulos (px) tomados del content stream de la referencia.
HEADERS = {
    1: dict(
        h=294.80315,  # 245 px a 80 dpi
        shape_cm=(0.984808, 0.173648, -0.173648, 0.984808, 48.721205, -126.019778),
        shape=(627.401575, 83.149606, 234.330709, 264.566929),
        tag1_cm=(0.997564, -0.069756, 0.069756, 0.997564, -4.680231, 8.964639),
        tag1=(49.133858, 52.913386, 153.765713, 37.162148), tag1_txt=(64.251969, 76.627761),
        tag2_cm=(0.99863, 0.052336, -0.052336, 0.99863, 5.895089, -7.476527),
        tag2=(79.370079, 90.708661, 132.671963, 36.230507), tag2_txt=(94.488189, 113.723817),
    ),
    2: dict(
        h=219.212598,  # 182 px a 80 dpi
        shape_cm=(0.984808, 0.173648, -0.173648, 0.984808, 42.814432, -126.536554),
        shape=(627.401575, 68.031496, 234.330709, 226.771654),
        tag1_cm=(0.997564, -0.069756, 0.069756, 0.997564, -3.889291, 8.937018),
        tag1=(49.133858, 41.574803, 153.765713, 37.162148), tag1_txt=(64.251969, 65.289178),
        tag2_cm=(0.99863, 0.052336, -0.052336, 0.99863, 4.906063, -7.502425),
        tag2=(79.370079, 71.811024, 132.671963, 36.230507), tag2_txt=(94.488189, 94.82618),
    ),
}


def header(c, page):
    g = HEADERS[page]
    c.saveState()
    px_space(c)
    c.setFillColor(INK)
    c.rect(0, 0, W / PX, g["h"], stroke=0, fill=1)

    # Rectángulo redondeado gris girado 10°, recortado por el encabezado.
    c.saveState()
    clip = c.beginPath()
    clip.rect(0, 0, W / PX, g["h"])
    c.clipPath(clip, stroke=0, fill=0)
    c.transform(*g["shape_cm"])
    c.setFillColor(SHAPE)
    c.roundRect(*g["shape"], radius=52.913386, stroke=0, fill=1)
    c.restoreState()

    # Etiquetas blancas inclinadas (-4° y +3°).
    for cm, box, pos, s, size in (
        (g["tag1_cm"], g["tag1"], g["tag1_txt"], "SOFÍA GUEVARA", 14.666016),
        (g["tag2_cm"], g["tag2"], g["tag2_txt"], "FOTO & VIDEO", 14.0),
    ):
        c.saveState()
        c.transform(*cm)
        c.setFillColor(white)
        c.rect(*box, stroke=0, fill=1)
        px_text(c, *pos, s, PB, size, INK, cs_em=0.0245)
        c.restoreState()
    c.restoreState()


def footer(c):
    rect(c, ML, 789.0, MR - ML, 0.567, RULE)
    text(c, ML, 808.26, "SOFÍA GUEVARA · FOTO & VIDEO", PB, 7, INK, cs=0.22)
    text(c, MR, 807.69, "sofiguevara.com.ar", IR, 7, GREY_77, align="right")


def big_title(c, top, parts, size, cs):
    """Partes (texto, fuente) en una misma línea con tracking negativo."""
    x = ML
    for s, font in parts:
        text(c, x, top, s, font, size, white, cs=cs)
        x += width(s, font, size, cs) + cs
    return x - cs


# ---------------------------------------------------------------- página 1
DATE = "29/10/2026"
VALID = "hasta el 03/11"

ITEMS = [
    ("Primer paso: videollamada inicial", "Incluida",
     "Antes de arrancar · Por Meet o Zoom",
     ["Conocer la historia de Bengar, su público y hacia dónde quiere crecer.",
      "Relevar referencias visuales, gustos y lo que la marca no quiere transmitir.",
      "Acordar alcance, tiempos y próximos pasos del proyecto."]),
    ("Logo e isologo", None,
     "Diseño a medida · 3 rondas de cambios incluidas",
     ["Logo principal de Bengar Calisthenics.",
      "Isologo: símbolo y nombre integrados en una sola pieza.",
      "Pensados para funcionar en remeras, redes y todo lo que quieras hacer con la marca."]),
    ("Qué te llevás", None,
     "Entrega digital · Archivos ordenados por carpeta",
     ["Logo e isologo en alta resolución, listos para usar donde los necesites.",
      "Archivos finales en PNG, SVG y PDF."]),
]

ROWS = [
    ("Seña para reservar el proyecto (20%)", "$50.000"),
    ("Saldo a la entrega final", "$200.000"),
]
TOTAL = "$250.000"


def page1(c):
    header(c, 1)
    space = width(" ", IR, 7.5)
    for top, label, value in ((51.62, "Fecha", DATE), (64.37, "Vigencia", VALID)):
        vx, _ = text(c, MR, top, value, IR, 7.5, GREY_BB, align="right")
        text(c, vx - space, top, label, IS, 7.5, white, align="right")

    # "PRESU" upright + "PUESTO" italic; tracking -0.031 em calibrado para que
    # el ancho total coincida con la referencia (42.52 -> 288.28 pt).
    big_title(c, 154.02, [("PRESU", PK), ("PUESTO", PBI)], 36, cs=-1.121)
    text(c, ML, 193.67, "LOGO DE MARCA · BENGAR CALISTHENICS", IS, 6.8, white, cs=1.159)

    # PARA / REFERENCIA
    for x, label, name, sub in (
        (ML, "PARA", "Bengar Calisthenics", "Paloma GB"),
        (297.64, "SERVICIO", "Logo de marca", None),
    ):
        text(c, x, 257.90, label, IS, 5.8, GREY_77, cs=1.197)
        text(c, x, 276.52, name, PB, 11, INK)
        if sub:
            text(c, x, 290.47, sub, IR, 7.5, GREY_88)
    rect(c, ML, 312.12, MR - ML, 2.27, INK)

    # Ítems
    top = 343.10
    for title, price, detail, bullets in ITEMS:
        text(c, ML, top, title, PB, 12.5, INK)
        if price:
            text(c, MR, top, price, PB, 12.5, INK, align="right")
        text(c, ML, top + 13.91, detail, IR, 7.5, GREY_77)
        b = top + 13.91 + 18.22
        for i, line in enumerate(bullets):
            if i:
                b += 14.94
            diamond(c, 46.49, b - 2.24)
            text(c, 58.11, b, line, IR, 8.2, INK)
        top = b + 30.65
    last = b

    # Seña / saldo
    rule_top = last + 16.11
    rect(c, ML, rule_top, MR - ML, 0.85, INK)
    row = rule_top + 16.38
    for i, (label, amount) in enumerate(ROWS):
        if i:
            grey = row + 10.11
            rect(c, ML, grey, MR - ML, 0.567, RULE)
            row = grey + 15.53
        text(c, ML, row, label, IR, 9, INK)
        text(c, MR, row + 0.73, amount, PB, 9, INK, align="right")

    # Cuadro TOTAL
    box_top = row + 27.12
    box_h = 60.62
    assert box_top + box_h < 789.0 - 12, "el cuadro TOTAL toca el pie"
    rect(c, 289.13, box_top, MR - 289.13, box_h, INK)
    text(c, 308.98, box_top + 32.67, "TOTAL", IS, 6.5, white, cs=1.257)
    text(c, 532.91, box_top + 36.96, TOTAL, PK, 19, white, align="right")

    footer(c)


# ---------------------------------------------------------------- página 2
CONDITIONS = [
    ("Para confirmar el proyecto se solicita una **seña del 20% del valor total "
     "($50.000)**.",
     ["Esta seña **reserva tu lugar en la agenda** y no es reembolsable."]),
    ("El **saldo restante de $200.000** se abona contra la entrega final del material.", []),
    ("**Plazo de entrega:** 15 días hábiles a partir de la acreditación de la seña.", []),
    ("El presupuesto incluye **3 rondas de cambios** sobre la propuesta elegida:",
     ["Cada ronda reúne todas las correcciones en **una sola devolución**.",
      "Las rondas extra **se cotizan aparte**."]),
    ("**Vigencia:** este presupuesto es válido hasta el **03/11/2026**.", []),
]


def rich_words(markup):
    """'a **b c**.' -> [[('a',0)], [('b',1)], [('c',1), ('.',0)]]"""
    words, cur = [], []
    for i, seg in enumerate(markup.split("**")):
        bold = i % 2 == 1
        parts = seg.split(" ")
        for j, p in enumerate(parts):
            if j:
                if cur:
                    words.append(cur)
                cur = []
            if p:
                cur.append((p, bold))
    if cur:
        words.append(cur)
    return words


def rich_paragraph(c, x, top, markup, size, color, max_w, leading):
    fonts = {False: IR, True: IS}
    space = width(" ", IR, size)
    lines, line, lw = [], [], 0.0
    for word in rich_words(markup):
        ww = sum(width(p, fonts[b], size) for p, b in word)
        if line and lw + space + ww > max_w:
            lines.append(line)
            line, lw = [], 0.0
        lw += (space if line else 0) + ww
        line.append(word)
    lines.append(line)
    for n, line in enumerate(lines):
        cx = x
        for k, word in enumerate(line):
            if k:
                cx += space
            for p, b in word:
                _, w = text(c, cx, top + n * leading, p, fonts[b], size, color)
                cx += w
    return top + (len(lines) - 1) * leading  # baseline de la última línea


def page2(c):
    header(c, 2)
    big_title(c, 111.96, [("RESERVA DE FECHA", PK)], 25, cs=-0.737)
    big_title(c, 136.96, [("Y CONDICIONES GENERALES", PBI)], 25, cs=-0.730)

    top = 206.73
    for i, (para, subs) in enumerate(CONDITIONS):
        diamond(c, 46.49, top - 3.49)
        last = rich_paragraph(c, 59.53, top, para, 10, INK, MR - 59.53, 15)
        for j, sub in enumerate(subs):
            stop = last + (19.09 if j == 0 else 18.94)
            ring(c, 64.35, stop - 2.48)
            last = rich_paragraph(c, 76.54, stop, sub, 9.6, GREY_33, MR - 76.54, 14.4)
        top = last + (24.48 if subs else 24.64)

    # Bloque negro de datos de pago, esquina superior derecha redondeada.
    bx, btop, bbot, r = 340.16, 613.10, 756.85, 28.35
    k = 0.5523 * r
    c.saveState()
    c.setFillColor(INK)
    p = c.beginPath()
    p.moveTo(0, H - bbot)
    p.lineTo(0, H - btop)
    p.lineTo(bx - r, H - btop)
    p.curveTo(bx - r + k, H - btop, bx, H - btop - r + k, bx, H - btop - r)
    p.lineTo(bx, H - bbot)
    p.close()
    c.drawPath(p, stroke=0, fill=1)
    c.restoreState()

    x = 28.35
    text(c, x, 645.80, "DATOS DE PAGO", IS, 5.8, GREY_AA, cs=1.064)
    text(c, x, 666.51, "Sofía Guevara", PB, 8.6, white)
    text(c, x, 681.67, "CVU: 0000003100090532884726", IR, 8.6, white)
    _, w = text(c, x, 696.72, "Alias:", IR, 8.6, white)
    text(c, x + w + width(" ", IR, 8.6), 696.72, "sofia.guevara872", PB, 8.6, white)
    text(c, x, 711.89, "CUIT/CUIL: 27-44159391-6", IR, 8.6, white)
    text(c, x, 726.94, "Mercado Pago", IR, 8.6, white)

    thanks = ["Gracias por tu interés y por valorar",
              "mi trabajo. Ante cualquier duda o",
              "necesidad, escribime sin",
              "compromiso."]
    for i, line in enumerate(thanks):
        text(c, 371.34, 693.29 + i * 14.25, line, PBI, 9.5, INK)

    footer(c)


def build(out):
    c = canvas.Canvas(out, pagesize=A4, initialFontName=IR, initialFontSize=10)
    c.setTitle("Presupuesto Logo e Isologo - Bengar Calisthenics")
    c.setAuthor("Sofía Guevara")
    page1(c)
    c.showPage()
    page2(c)
    c.showPage()
    c.save()


if __name__ == "__main__":
    build(sys.argv[1] if len(sys.argv) > 1 else
          os.path.join(HERE, "Presupuesto_Logo_Isologo_Bengar_Calisthenics_2026.pdf"))
