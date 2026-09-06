"""Paleta de atoqlab en los formatos que hacen falta fuera del navegador.

Genera tokens para codigo (CSS y JSON), paletas intercambiables para Adobe
(.ase) e Inkscape/GIMP (.gpl), y calcula el contraste WCAG de cada
combinacion, que es lo que decide si un color se puede usar sobre otro.
"""
import json, os, struct

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT = os.path.join(ROOT, "paleta")
os.makedirs(OUT, exist_ok=True)

COLORES = [
    ("Azul marino",  "navy",       "#192851", "Color principal. Titulares, texto y fondos sólidos."),
    ("Azul soporte", "blue",       "#4A70D4", "Acentos, degradados, estado de foco. No usar para texto pequeño sobre blanco."),
    ("Rojo atoq",    "brand",      "#B92222", "Color de acción: botones, enlaces destacados, footer."),
    ("Rojo claro",   "brand-400",  "#D63E3E", "Estado hover del rojo atoq. Solo interacción."),
    ("Error",        "danger",     "#E32529", "Mensajes de error y validación."),
    ("Éxito",        "success",    "#31CF6E", "Confirmaciones y estados correctos."),
    ("Gris fondo",   "ash",        "#E4E4E4", "Fondos alternos y separadores suaves."),
    ("Gris borde",   "ash-dark",   "#C6C6C6", "Bordes y líneas divisorias."),
    ("Blanco",       "white",      "#FFFFFF", "Fondo base y texto sobre color sólido."),
]

def rgb(h):
    return tuple(int(h[i:i+2], 16) for i in (1, 3, 5))

def cmyk(h):
    """Conversion referencial. Para imprenta hay que perfilar con el proveedor."""
    r, g, b = (v / 255 for v in rgb(h))
    k = 1 - max(r, g, b)
    if k >= 1:
        return (0, 0, 0, 100)
    f = lambda c: round((1 - c - k) / (1 - k) * 100)
    return (f(r), f(g), f(b), round(k * 100))

def luminancia(h):
    def canal(v):
        v /= 255
        return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = (canal(v) for v in rgb(h))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b

def contraste(a, b):
    la, lb = sorted((luminancia(a), luminancia(b)), reverse=True)
    return round((la + 0.05) / (lb + 0.05), 2)

def nivel(ratio, grande=False):
    if grande:
        return "AAA" if ratio >= 4.5 else "AA" if ratio >= 3 else "—"
    return "AAA" if ratio >= 7 else "AA" if ratio >= 4.5 else "AA grande" if ratio >= 3 else "—"

# ------------------------------------------------------------------- tokens
css = ["/* Tokens de color de atoqlab. Generado por scripts/paleta.py */", ":root {"]
for nombre, slug, hexa, _ in COLORES:
    css.append(f"  --color-{slug}: {hexa};")
css.append("}")
open(os.path.join(OUT, "tokens.css"), "w").write("\n".join(css) + "\n")

datos = {
    "colores": [
        {"nombre": n, "token": s, "hex": h, "rgb": list(rgb(h)),
         "cmyk_referencial": list(cmyk(h)), "uso": u}
        for n, s, h, u in COLORES
    ],
    "contraste": [
        {"texto": a, "fondo": b, "ratio": contraste(ha, hb),
         "texto_normal": nivel(contraste(ha, hb)),
         "texto_grande": nivel(contraste(ha, hb), grande=True)}
        for (a, ha), (b, hb) in [
            (("Azul marino", "#192851"), ("Blanco", "#FFFFFF")),
            (("Blanco", "#FFFFFF"), ("Azul marino", "#192851")),
            (("Rojo atoq", "#B92222"), ("Blanco", "#FFFFFF")),
            (("Blanco", "#FFFFFF"), ("Rojo atoq", "#B92222")),
            (("Azul soporte", "#4A70D4"), ("Blanco", "#FFFFFF")),
            (("Azul marino", "#192851"), ("Gris fondo", "#E4E4E4")),
            (("Rojo atoq", "#B92222"), ("Azul marino", "#192851")),
        ]
    ],
}
open(os.path.join(OUT, "tokens.json"), "w").write(json.dumps(datos, indent=2, ensure_ascii=False) + "\n")

# ------------------------------------------------ paleta GIMP / Inkscape (.gpl)
gpl = ["GIMP Palette", "Name: atoqlab", "Columns: 3", "#"]
for nombre, _, hexa, _ in COLORES:
    r, g, b = rgb(hexa)
    gpl.append(f"{r:>3} {g:>3} {b:>3}\t{nombre}")
open(os.path.join(OUT, "atoqlab.gpl"), "w").write("\n".join(gpl) + "\n")

# ------------------------------------------- paleta Adobe (.ase) para Ai / Ps
def bloque_color(nombre, hexa):
    txt = nombre.encode("utf-16-be") + b"\x00\x00"
    cuerpo = (struct.pack(">H", len(nombre) + 1) + txt + b"RGB "
              + b"".join(struct.pack(">f", v / 255) for v in rgb(hexa))
              + struct.pack(">H", 0))            # 0 = color global
    return struct.pack(">HI", 0x0001, len(cuerpo)) + cuerpo

ase = b"ASEF" + struct.pack(">HHI", 1, 0, len(COLORES))
ase += b"".join(bloque_color(n, h) for n, _, h, _ in COLORES)
open(os.path.join(OUT, "atoqlab.ase"), "wb").write(ase)

print("paleta/")
for f in sorted(os.listdir(OUT)):
    print(f"  {f:20} {os.path.getsize(os.path.join(OUT, f)):>6} bytes")
print("\ncontraste WCAG:")
for c in datos["contraste"]:
    print(f"  {c['texto']:14} sobre {c['fondo']:14} {c['ratio']:>6}:1   normal {c['texto_normal']:<10} grande {c['texto_grande']}")
