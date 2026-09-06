from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.misc.transform import Transform
import json, sys

import os
SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "fuentes", "Montserrat-Variable.ttf")

def instance(weight):
    f = TTFont(SRC)
    return instancer.instantiateVariableFont(f, {"wght": weight}, inplace=False)

def text_paths(font, text, size, tracking=0.0, x=0.0, baseline=0.0):
    """Devuelve (lista_de_d, ancho_total). tracking en unidades de 'size'."""
    upem = font["head"].unitsPerEm
    scale = size / upem
    cmap = font.getBestCmap()
    gs = font.getGlyphSet()
    hmtx = font["hmtx"]
    out, pen_x = [], x
    for ch in text:
        gname = cmap.get(ord(ch))
        if gname is None:
            raise SystemExit(f"glifo ausente: {ch!r}")
        spen = SVGPathPen(gs)
        # y-flip: SVG crece hacia abajo
        t = Transform(scale, 0, 0, -scale, pen_x, baseline)
        gs[gname].draw(TransformPen(spen, t))
        d = spen.getCommands()
        if d:
            out.append(d)
        adv = hmtx[gname][0] * scale
        pen_x += adv + tracking
    return out, pen_x - tracking - x

if __name__ == "__main__":
    spec = json.loads(sys.argv[1])
    font = instance(spec["weight"])
    ds, w = text_paths(font, spec["text"], spec["size"], spec.get("tracking", 0),
                       spec.get("x", 0), spec.get("baseline", 0))
    print(json.dumps({"d": " ".join(ds), "width": round(w, 2)}))
