"""Instancia Montserrat variable en pesos estaticos.

Chrome no sabe subconjuntar una instancia de fuente variable al exportar PDF:
cae a fuentes Type 3, que son glifos dibujados uno a uno. Imprimen bien, pero
pierden el nombre de la fuente y hay RIP de imprenta que los manejan mal.
Con TTF estaticos, Chrome incrusta subconjuntos TrueType normales.
"""
import os
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
ORIGEN = os.path.join(RAIZ, "fuentes", "Montserrat-Variable.ttf")
DESTINO = os.path.join(RAIZ, "impresos", "fuentes")
os.makedirs(DESTINO, exist_ok=True)

PESOS = {400: "Regular", 500: "Medium", 600: "SemiBold", 700: "Bold", 800: "ExtraBold"}

for peso, nombre in PESOS.items():
    f = instancer.instantiateVariableFont(TTFont(ORIGEN), {"wght": peso}, inplace=False)
    completo = f"Montserrat {nombre}"
    postscript = f"Montserrat-{nombre}"
    for r in f["name"].names:
        if r.nameID == 1: r.string = "Montserrat".encode("utf-16-be") if r.platformID == 3 else b"Montserrat"
        elif r.nameID == 2: r.string = nombre.encode("utf-16-be") if r.platformID == 3 else nombre.encode()
        elif r.nameID == 4: r.string = completo.encode("utf-16-be") if r.platformID == 3 else completo.encode()
        elif r.nameID == 6: r.string = postscript.encode("utf-16-be") if r.platformID == 3 else postscript.encode()
    salida = os.path.join(DESTINO, f"{postscript}.ttf")
    f.save(salida)
    print(f"✓ impresos/fuentes/{postscript}.ttf  {os.path.getsize(salida)//1024} KB")
