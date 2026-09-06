"""Genera el sistema de logotipo de atoqlab.

Isotipo: cabeza de zorro geometrica -- "atoq" es zorro en quechua -- partida por
un kerf, la ranura que deja el laser al cortar. El kerf es transparente: la
marca se apoya en el fondo que tenga debajo, sea cual sea.

Salida:
  logos/svg/   sistema completo, vectorial
  redes/svg/   piezas listas para cada red social
"""
import os
from wordmark import instance, text_paths

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
LOGOS = os.path.join(ROOT, "logos", "svg")
REDES = os.path.join(ROOT, "redes", "svg")
for d in (LOGOS, REDES):
    os.makedirs(d, exist_ok=True)

NAVY, RED, WHITE = "#192851", "#B92222", "#FFFFFF"
BLUE, ASH = "#4A70D4", "#E4E4E4"

# ------------------------------------------------------------------ isotipo
K = 1.5                                   # media ranura del kerf
EYE_L = "M22 47 L34 53 L32.5 58 L20.5 52 Z"
EYE_R = "M74 47 L62 53 L63.5 58 L75.5 52 Z"
HALF_L = f"M6 4 L26 32 L{48-K} 34 L{48-K} 92 L20 62 L12 48 Z"
HALF_R = f"M90 4 L70 32 L{48+K} 34 L{48+K} 92 L76 62 L84 48 Z"
SOLID  = "M6 4 L26 32 L48 34 L70 32 L90 4 L84 48 L76 62 L48 92 L20 62 L12 48 Z"
MX, MY, MW, MH = 6, 4, 84, 88             # caja visible dentro del lienzo 96x96

def mark(cl, cr):
    return (f'<path fill-rule="evenodd" fill="{cl}" d="{HALF_L} {EYE_L}"/>'
            f'<path fill-rule="evenodd" fill="{cr}" d="{HALF_R} {EYE_R}"/>')

def mark_solid(c, opacity=None):
    op = f' fill-opacity="{opacity}"' if opacity else ""
    return f'<path fill-rule="evenodd" fill="{c}"{op} d="{SOLID} {EYE_L} {EYE_R}"/>'

def place_mark(body, x, y, height):
    """Coloca el isotipo con su esquina superior izquierda visible en (x, y)."""
    s = height / MH
    return f'<g transform="translate({x - MX*s:.3f},{y - MY*s:.3f}) scale({s:.5f})">{body}</g>'

MARK_RATIO = MW / MH                      # ancho / alto del isotipo

# ------------------------------------------------------------------ wordmark
WM_SIZE, WM_TRACK = 46, -0.6
TAG = "MANUFACTURA DE PRECISIÓN"
TAG_SIZE, TAG_WEIGHT = 9, 600

f800, f600 = instance(800), instance(TAG_WEIGHT)
d_atoq, w_atoq = text_paths(f800, "atoq", WM_SIZE, WM_TRACK, 0, 0)
w_atoq += WM_TRACK
d_lab, w_lab = text_paths(f800, "lab", WM_SIZE, WM_TRACK, w_atoq, 0)
WM_W = w_atoq + w_lab
_, tag_nat = text_paths(f600, TAG, TAG_SIZE, 0, 0, 0)
TAG_TRACK = (WM_W - tag_nat) / (len(TAG) - 1)
d_tag, _ = text_paths(f600, TAG, TAG_SIZE, TAG_TRACK, 0, 0)
D_ATOQ, D_LAB, D_TAG = " ".join(d_atoq), " ".join(d_lab), " ".join(d_tag)

ASC, DESC = 0.75 * WM_SIZE, 0.21 * WM_SIZE
GAP_TAG = 20

def wordmark(x, baseline, c_atoq, c_lab, c_tag=None, tag_op="0.62", scale=1.0):
    g = (f'<g transform="translate({x:.3f},{baseline:.3f}) scale({scale:.5f})">'
         f'<path fill="{c_atoq}" d="{D_ATOQ}"/><path fill="{c_lab}" d="{D_LAB}"/></g>')
    if c_tag:
        g += (f'<g transform="translate({x:.3f},{baseline + GAP_TAG*scale:.3f}) scale({scale:.5f})">'
              f'<path fill="{c_tag}" fill-opacity="{tag_op}" d="{D_TAG}"/></g>')
    return g

def svg(w, h, body, title, bg=None):
    rect = f'<rect width="{w:g}" height="{h:g}" fill="{bg}"/>' if bg else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:g} {h:g}" '
            f'width="{w:g}" height="{h:g}" role="img" aria-label="{title}">'
            f'<title>{title}</title>{rect}{body}</svg>\n')

def write(folder, name, content):
    with open(os.path.join(folder, name), "w") as fh:
        fh.write(content)
    return name

# =====================================================================
#  Bloques reutilizables
# =====================================================================
H_MARK_H = 66                                   # alto del isotipo en el lockup
H_GAP = 18
H_MARK_W = MARK_RATIO * H_MARK_H
H_X0 = H_MARK_W + H_GAP
H_BASE = (H_MARK_H - (ASC + GAP_TAG)) / 2 + ASC
H_W, H_H = H_X0 + WM_W, max(H_MARK_H, H_BASE + GAP_TAG)

def lockup_h(cl, cr, c_atoq, c_lab, c_tag, tag_op):
    """Lockup horizontal en su tamaño nativo (H_W x H_H)."""
    return (place_mark(mark(cl, cr), 0, 0, H_MARK_H)
            + wordmark(H_X0, H_BASE, c_atoq, c_lab, c_tag, tag_op))

# Version compacta, sin bajada. Por debajo de 120 px de ancho el tagline deja
# de leerse, asi que estorba en vez de aportar.
C_MARK_H = 56
C_MARK_W = MARK_RATIO * C_MARK_H
C_GAP = 14
C_X0 = C_MARK_W + C_GAP
C_BASE = C_MARK_H / 2 + ASC * 0.36          # centrado optico del wordmark
C_W, C_H = C_X0 + WM_W, C_MARK_H

def lockup_compacto(cl, cr, c_atoq, c_lab):
    return (place_mark(mark(cl, cr), 0, 0, C_MARK_H)
            + wordmark(C_X0, C_BASE, c_atoq, c_lab))

V_MARK_H = 84
V_MARK_W = MARK_RATIO * V_MARK_H
V_GAP = 20
V_W = max(V_MARK_W, WM_W)
V_BASE = V_MARK_H + V_GAP + ASC
V_H = V_BASE + GAP_TAG

def lockup_v(cl, cr, c_atoq, c_lab, c_tag, tag_op):
    return (place_mark(mark(cl, cr), (V_W - V_MARK_W) / 2, 0, V_MARK_H)
            + wordmark((V_W - WM_W) / 2, V_BASE, c_atoq, c_lab, c_tag, tag_op))

# =====================================================================
#  Sistema de logotipo
# =====================================================================
COMBOS = [
    ("color",  NAVY, RED,   NAVY,  RED,   NAVY,  "0.62"),
    ("blanco", WHITE, WHITE, WHITE, WHITE, WHITE, "0.72"),
    ("azul",   NAVY, NAVY,  NAVY,  NAVY,  NAVY,  "0.62"),
    ("rojo",   RED,  RED,   RED,   RED,   RED,   "0.62"),
    ("negro",  "#000000", "#000000", "#000000", "#000000", "#000000", "0.62"),
]

hechos = []
for nombre, cl, cr, ca, cb, ct, op in COMBOS:
    hechos.append(write(LOGOS, f"atoqlab-horizontal-{nombre}.svg",
        svg(round(H_W, 1), round(H_H, 1), lockup_h(cl, cr, ca, cb, ct, op), "atoqlab")))
    hechos.append(write(LOGOS, f"atoqlab-vertical-{nombre}.svg",
        svg(round(V_W, 1), round(V_H, 1), lockup_v(cl, cr, ca, cb, ct, op), "atoqlab")))
    hechos.append(write(LOGOS, f"atoqlab-isotipo-{nombre}.svg",
        svg(MW, MH, place_mark(mark(cl, cr), 0, 0, MH), "atoqlab")))
    hechos.append(write(LOGOS, f"atoqlab-compacto-{nombre}.svg",
        svg(round(C_W, 1), round(C_H, 1), lockup_compacto(cl, cr, ca, cb), "atoqlab")))
    hechos.append(write(LOGOS, f"atoqlab-wordmark-{nombre}.svg",
        svg(round(WM_W, 1), round(ASC + DESC, 1), wordmark(0, ASC, ca, cb), "atoqlab")))

# Monocromo de una tinta: sin kerf, para grabado laser, bordado y sellos
for nombre, color in [("navy", NAVY), ("blanco", WHITE), ("negro", "#000000")]:
    hechos.append(write(LOGOS, f"atoqlab-isotipo-solido-{nombre}.svg",
        svg(MW, MH, place_mark(mark_solid(color), 0, 0, MH), "atoqlab")))

# Favicon: cuadrado azul con el zorro en blanco
BOX = 96
fav = (f'<rect width="{BOX}" height="{BOX}" rx="20" fill="{NAVY}"/>'
       + place_mark(mark_solid(WHITE), (BOX - MW*0.72)/2, (BOX - MH*0.72)/2, MH*0.72))
hechos.append(write(LOGOS, "atoqlab-favicon.svg", svg(BOX, BOX, fav, "atoqlab")))

print(f"logos/svg: {len(hechos)} archivos")
print(f"  horizontal {H_W:.0f}x{H_H:.0f}   vertical {V_W:.0f}x{V_H:.0f}   isotipo {MW}x{MH}")
