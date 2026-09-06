"""Piezas listas para redes sociales, en vectorial.

Cada portada usa el mismo esquema: fondo azul marino, el isotipo ampliado como
marca de agua saliendo por el borde derecho, un filete rojo abajo y el logotipo
en blanco dentro del area segura de cada red.
"""
from logos import (NAVY, RED, WHITE, MW, MH, MARK_RATIO, mark, mark_solid,
                   place_mark, lockup_h, lockup_v, H_W, H_H, V_W, V_H,
                   svg, write, REDES)

# ---------------------------------------------------------------- utilidades
def watermark(w, h, escala=1.15, x_rel=0.66, opacidad="0.08"):
    """Isotipo saliendo por el borde derecho.

    La escala se mantiene cerca de 1 a proposito: mas grande y solo asoma un
    fragmento (un ojo, media mejilla) que se lee como una forma suelta en vez
    de como el zorro.
    """
    alto = h * escala
    return place_mark(mark_solid(WHITE, opacidad), w * x_rel, (h - alto) / 2, alto)

def filete(w, h, grosor):
    return f'<rect x="0" y="{h - grosor}" width="{w}" height="{grosor}" fill="{RED}"/>'

def escalar(body, ancho_nativo, alto_nativo, ancho_destino, x, y):
    s = ancho_destino / ancho_nativo
    return f'<g transform="translate({x:.2f},{y:.2f}) scale({s:.5f})">{body}</g>', alto_nativo * s

def portada(nombre, w, h, ancho_logo, *, seguro=None, escala_wm=1.7, x_wm=0.60):
    """seguro = (ancho, alto) del area visible garantizada, centrada."""
    logo = lockup_h(WHITE, WHITE, WHITE, WHITE, WHITE, "0.72")
    g, alto_logo = escalar(logo, H_W, H_H, ancho_logo, 0, 0)
    cx, cy = (w - ancho_logo) / 2, (h - alto_logo) / 2
    g = g.replace('translate(0.00,0.00)', f'translate({cx:.2f},{cy:.2f})')

    cuerpo = (f'<rect width="{w}" height="{h}" fill="{NAVY}"/>'
              + watermark(w, h, escala_wm, x_wm)
              + filete(w, h, max(3, round(h * 0.016)))
              + g)
    write(REDES, nombre, svg(w, h, cuerpo, "atoqlab"))
    extra = f"  (area segura {seguro[0]}x{seguro[1]})" if seguro else ""
    print(f"  {nombre:38} {w}x{h}{extra}")

def avatar(nombre, size, fondo, cl, cr, solido=False):
    """Cuadrado para foto de perfil. El isotipo ocupa el 46% para sobrevivir
    al recorte circular que aplican casi todas las redes."""
    alto = size * 0.46
    ancho = MARK_RATIO * alto
    figura = mark_solid(cl) if solido else mark(cl, cr)
    cuerpo = (f'<rect width="{size}" height="{size}" fill="{fondo}"/>'
              + place_mark(figura, (size - ancho) / 2, (size - alto) / 2, alto))
    write(REDES, nombre, svg(size, size, cuerpo, "atoqlab"))
    print(f"  {nombre:38} {size}x{size}")

# ---------------------------------------------------------------- perfiles
print("perfil:")
avatar("avatar-azul.svg",   1080, NAVY,  WHITE, WHITE, solido=True)
avatar("avatar-rojo.svg",   1080, RED,   WHITE, WHITE, solido=True)
avatar("avatar-blanco.svg", 1080, WHITE, NAVY,  RED)
avatar("avatar-whatsapp.svg", 640, NAVY, WHITE, WHITE, solido=True)

# ---------------------------------------------------------------- portadas
print("portadas:")
portada("portada-facebook.svg",        1640, 856,  620, seguro=(820, 312))
portada("portada-linkedin-empresa.svg", 1128, 191, 330, x_wm=0.74, escala_wm=1.30)
portada("portada-linkedin-personal.svg", 1584, 396, 480, x_wm=0.70, escala_wm=1.20)
portada("portada-x.svg",               1500, 500,  520, x_wm=0.68)
portada("portada-youtube.svg",         2560, 1440, 760, seguro=(1546, 423), escala_wm=1.05, x_wm=0.70)

# ---------------------------------------------------------------- contenido
print("contenido:")
for nombre, w, h, ancho in [("post-instagram.svg", 1080, 1080, 620),
                            ("historia-instagram.svg", 1080, 1920, 660),
                            ("open-graph.svg", 1200, 630, 560)]:
    logo = lockup_v(WHITE, WHITE, WHITE, WHITE, WHITE, "0.72")
    g, alto = escalar(logo, V_W, V_H, ancho, 0, 0)
    g = g.replace('translate(0.00,0.00)', f'translate({(w-ancho)/2:.2f},{(h-alto)/2:.2f})')
    cuerpo = (f'<rect width="{w}" height="{h}" fill="{NAVY}"/>'
              + watermark(w, h, 1.05, 0.64)
              + filete(w, h, max(4, round(h * 0.018))) + g)
    write(REDES, nombre, svg(w, h, cuerpo, "atoqlab"))
    print(f"  {nombre:38} {w}x{h}")
