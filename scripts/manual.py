"""Arma manual-de-marca.html.

Las tablas de color y de contraste se rellenan desde paleta/tokens.json, que
genera scripts/paleta.py, para que el manual no se desincronice de los tokens
que realmente usa el codigo.
"""
import json, os, datetime

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
datos = json.load(open(os.path.join(ROOT, "paleta", "tokens.json")))

def swatches():
    out = []
    for c in datos["colores"]:
        r, g, b = c["rgb"]
        cy, m, y, k = c["cmyk_referencial"]
        claro = c["hex"] in ("#FFFFFF", "#E4E4E4", "#C6C6C6", "#31CF6E")
        out.append(f'''
        <article class="swatch">
          <div class="swatch__chip{' swatch__chip--borde' if claro else ''}" style="background:{c['hex']}"></div>
          <div class="swatch__datos">
            <h3>{c['nombre']}</h3>
            <p class="swatch__uso">{c['uso']}</p>
            <dl>
              <div><dt>HEX</dt><dd>{c['hex']}</dd></div>
              <div><dt>RGB</dt><dd>{r} {g} {b}</dd></div>
              <div><dt>CMYK</dt><dd>{cy} {m} {y} {k}</dd></div>
              <div><dt>Token</dt><dd><code>--color-{c['token']}</code></dd></div>
            </dl>
          </div>
        </article>''')
    return "".join(out)

def contraste_filas():
    out = []
    for c in datos["contraste"]:
        falla = c["texto_normal"] == "—"
        estado = "falla" if falla else ("ok" if c["texto_normal"] in ("AA", "AAA") else "aviso")
        etiqueta = {"falla": "No usar", "ok": "Aprobado", "aviso": "Solo texto grande"}[estado]
        out.append(f'''
          <tr>
            <td>{c['texto']}</td>
            <td>{c['fondo']}</td>
            <td class="num">{c['ratio']}:1</td>
            <td>{c['texto_normal']}</td>
            <td>{c['texto_grande']}</td>
            <td><span class="pill pill--{estado}">{etiqueta}</span></td>
          </tr>''')
    return "".join(out)

REDES = [
    ("Foto de perfil", "Instagram · Facebook · LinkedIn · X", "1080 × 1080", "redes/png/avatar-azul.png",
     "Versión azul por defecto. Todas las redes la recortan en círculo, por eso el isotipo ocupa solo el 46%."),
    ("Foto de perfil alterna", "Cuando el feed es oscuro", "1080 × 1080", "redes/png/avatar-rojo.png",
     "Fondo rojo atoq. Misma construcción."),
    ("Foto de perfil clara", "Directorios y fondos oscuros", "1080 × 1080", "redes/png/avatar-blanco.png",
     "Única versión donde el isotipo va a dos tintas."),
    ("WhatsApp Business", "Perfil de empresa", "640 × 640", "redes/png/avatar-whatsapp.png",
     "WhatsApp comprime fuerte: por eso va la versión sólida, sin kerf."),
    ("Portada Facebook", "Página de empresa", "1640 × 856", "redes/png/portada-facebook.png",
     "Área segura de 820 × 312 al centro: en escritorio se recorta a eso."),
    ("Portada LinkedIn", "Página de empresa", "1128 × 191", "redes/png/portada-linkedin-empresa.png",
     "Banda muy baja. El logo va al centro porque el avatar tapa la esquina inferior izquierda."),
    ("Fondo LinkedIn", "Perfil personal", "1584 × 396", "redes/png/portada-linkedin-personal.png",
     "Para el perfil de quien represente a la empresa."),
    ("Encabezado X", "Perfil de X", "1500 × 500", "redes/png/portada-x.png", "El avatar tapa la esquina inferior izquierda."),
    ("Banner YouTube", "Canal", "2560 × 1440", "redes/png/portada-youtube.png",
     "Área segura de 1546 × 423: es lo único que se ve en móvil."),
    ("Post de marca", "Instagram · Facebook", "1080 × 1080", "redes/png/post-instagram.png",
     "Plantilla para anuncios y presentaciones de marca."),
    ("Historia", "Instagram · Facebook · WhatsApp", "1080 × 1920", "redes/png/historia-instagram.png",
     "Deja libres los 250 px de arriba y abajo: ahí van los controles de la app."),
    ("Vista previa de enlace", "Al compartir la web", "1200 × 630", "redes/png/open-graph.png",
     "Open Graph. Ya está montada en el sitio web."),
]

def redes_filas():
    return "".join(f'''
        <article class="pieza">
          <img src="{ruta}" alt="{nombre}" loading="lazy" />
          <div class="pieza__datos">
            <h3>{nombre}</h3>
            <p class="pieza__donde">{donde}</p>
            <p class="pieza__medida">{medida} px</p>
            <p class="pieza__nota">{nota}</p>
          </div>
        </article>''' for nombre, donde, medida, ruta, nota in REDES)

HTML = open(os.path.join(os.path.dirname(__file__), "manual.template.html")).read()
salida = (HTML
          .replace("<!--SWATCHES-->", swatches())
          .replace("<!--CONTRASTE-->", contraste_filas())
          .replace("<!--REDES-->", redes_filas())
          .replace("{{FECHA}}", datetime.date.today().strftime("%d.%m.%Y")))
open(os.path.join(ROOT, "manual-de-marca.html"), "w").write(salida)
print(f"manual-de-marca.html  {len(salida):,} bytes")
