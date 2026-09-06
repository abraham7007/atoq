# atoqlab · Kit de marca

Identidad de **atoqlab** — corte láser de fibra. Todo lo de esta carpeta se
genera con scripts, así que un cambio de color o de forma se propaga a los
logos, a las piezas de redes y al manual con un solo comando.

> **Versión 1.0 preliminar.** La marca sirve para trabajar y visualizar, y se
> puede revisar entera sin romper nada: todo sale de `scripts/`.
>
> **Los datos de contacto son ficticios.** El teléfono, la dirección, el correo
> y el WhatsApp que aparecen en el manual y en las piezas impresas son de
> relleno, incluidos los que van dentro de los códigos QR. No llames a esos
> números. Antes de mandar cualquier pieza a imprenta hay que reemplazarlos:
> ver el checklist final de [impresos/README.md](impresos/README.md).

## Empieza por aquí

Abre **`manual-de-marca.html`** en el navegador. Ahí está cómo usar el logo,
la paleta con su contraste comprobado, la tipografía y qué pieza va en cada
red social.

Para compartirlo, **`atoqlab-manual-de-marca.pdf`** es la misma cosa en 10
páginas **A4 horizontal**, con portada fotográfica, numeración y las fuentes
incrustadas. El formato apaisado da 269 mm de ancho útil, suficiente para tres
columnas de tarjetas y un rail de título a la izquierda. Se regenera con:

```bash
node scripts/manual-pdf.mjs
```

## Qué hay

Los PNG a 300 dpi y los PDF en CMYK no se versionan porque son regenerables y
pesan 53 MB. Salen con `node impresos/scripts/exportar.mjs` y
`node impresos/scripts/cmyk.mjs`.

```
logos/svg/     29 archivos. El original de todo, siempre preferir este.
logos/png/     @1000 y @2000 px, fondo transparente. Solo si no aceptan SVG.
logos/png/favicon/   16 a 512 px.
redes/png/     Listas para subir, al tamaño exacto de cada plataforma.
redes/svg/     Las mismas, editables.
paleta/        tokens.css · tokens.json · atoqlab.ase (Adobe) · atoqlab.gpl (Inkscape/GIMP)
fuentes/       Montserrat variable, TTF y WOFF2. Licencia SIL OFL.
```

### Versiones del logo

| Versión | Cuándo |
|---|---|
| `horizontal` | La principal: cabeceras, papelería, firmas de correo |
| `compacto` | Sin bajada, cuando mide menos de 120 px de ancho |
| `vertical` | Espacios cuadrados: posts, sellos, señalética |
| `isotipo` | Solo el zorro: avatares, favicon, marcaje de piezas |
| `wordmark` | Solo el texto, casos puntuales |

Colores disponibles: `color`, `blanco`, `azul`, `rojo`, `negro`.
Nomenclatura: `atoqlab-{versión}-{color}.svg`.

La variante `isotipo-solido-*` no lleva kerf. Es para grabado láser, bordado y
sellos, donde una ranura de décimas de milímetro se cierra sola y ensucia la
figura.

## Regenerar

Requiere Python 3 y Node.

```bash
python3 -m venv .venv && ./.venv/bin/pip install fonttools
npm install

./.venv/bin/python scripts/logos.py       # logos/svg
./.venv/bin/python scripts/redes.py       # redes/svg
./.venv/bin/python scripts/paleta.py      # paleta/ (tokens, .ase, .gpl, contraste)
node scripts/rasterizar.mjs               # todos los PNG
./.venv/bin/python scripts/manual.py      # manual-de-marca.html
node scripts/manual-pdf.mjs               # atoqlab-manual-de-marca.pdf
```

El orden importa: `manual.py` lee `paleta/tokens.json`, `manual-pdf.mjs` lee el
HTML que produce, y `rasterizar.mjs` lee los SVG. Para cambiar un color, edítalo en `scripts/paleta.py` y en la
constante correspondiente de `scripts/logos.py`, y vuelve a correr todo.

## Cómo está hecho el logo

El wordmark no es texto: son **trazos vectoriales** extraídos de Montserrat
variable con `fontTools` e instanciados en ExtraBold. Por eso los SVG se ven
igual en cualquier equipo, tenga o no la fuente instalada, y no hay riesgo de
que un visor sustituya la tipografía.

El isotipo se dibuja por coordenadas en `scripts/logos.py`. El kerf —la ranura
central— es transparente, no blanco: la marca se apoya en el fondo que tenga
debajo. Por eso funciona igual sobre blanco, sobre el azul marino y sobre el
rojo.

## Relación con el sitio web

El sitio vive aparte, en `../atoqLab`. Comparten paleta y tipografía pero no
comparten archivos: si cambias la marca aquí, hay que copiar los SVG nuevos a
`../atoqLab/public/logo/` y volver a correr `node scripts/gen-icons.mjs` allá.
