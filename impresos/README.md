# atoqlab · Material promocional

Nueve piezas listas para imprenta y para redes. Todo se diseña en HTML con
medidas físicas y se exporta a PDF vectorial con las fuentes incrustadas.

## Qué entregar a la imprenta

Los PDF de **`pdf/rgb/`** son los buenos. El nombre del archivo lleva la
especificación completa:

```
afiche-a3_297x420mm_sangrado3mm.pdf
          └ formato final    └ sangrado por lado
```

La página mide el formato final **más 6 mm** (3 mm de sangrado por cada lado).
No lleva marcas de corte: la imprenta recorta a la medida que indica el nombre.

| Pieza | Formato final | Caras | Notas |
|---|---|---|---|
| `afiche-a3` | 297 × 420 mm | 1 | Local, vitrina, mural |
| `volante-a5` | 148 × 210 mm | 2 | Reparto en mano |
| `triptico-a4` | 297 × 210 mm | 2 | Plegado en **Z** a 99 y 198 mm |
| `tarjeta` | 90 × 50 mm | 2 | Medida estándar en Perú |
| `ficha-tecnica` | 210 × 297 mm | 1 | Adjunto a cotizaciones |
| `membretada` | 210 × 297 mm | 1 | Cartas y proformas |
| `rollup` | 850 × 2000 mm | 1 | Sangrado de 20 mm |

Para redes, en `png/`: `promo-post_1080x1080.png` y
`promo-historia_1080x1920.png`, más el PNG a 300 dpi de cada pieza impresa.

## RGB o CMYK

**Dale el RGB salvo que te pidan lo contrario.** Casi toda imprenta prefiere
convertir con su propio perfil, que conoce su papel y su máquina.

`pdf/cmyk/` existe para cuando exijan el archivo ya separado. La conversión la
hace Ghostscript sin perfil ICC: sirve, pero el negro y los azules profundos
pueden variar. En ese caso, pide una prueba de color impresa antes del tiraje.

## Sobre las fotos

Todas las piezas usan **fotos reales del taller**, de 9 a 12.5 MP. Ya no hay
techo de tamaño: los JPG de `fotos/` llegan a 3000 px de lado, o sea 254 mm a
300 dpi, más de lo que pide cualquiera de estas piezas.

Las fotos vienen de `../atoqLab/fotos-taller/` y las procesa
`../atoqLab/scripts/fotos-taller.mjs`, que también genera los WebP de la web.
Un solo comando actualiza los dos proyectos. Si añades fotos nuevas, agrégalas
al catálogo `FOTOS` de ese script con su nombre y su texto alternativo.

Cuatro fotos son de 1280 × 720 (`laser-cabezal`, `plegadora-panel`) o de
1440 × 2560 (`bandejas-largas`, `bandejas-perspectiva`): sirven hasta 108 y
122 mm de ancho respectivamente. El resto no tiene restricción práctica.

## Regenerar

```bash
node impresos/scripts/qr.mjs          # códigos QR (tras cambiar el WhatsApp)
node impresos/scripts/verificar.mjs   # avisa si algo se sale del área segura
node impresos/scripts/exportar.mjs    # PDF en RGB + PNG a 300 dpi
node impresos/scripts/cmyk.mjs        # conversión a CMYK
```

`verificar.mjs` es el que evita el desastre: si una pieza desborda su área
segura, la imprenta te devuelve texto cortado. Córrelo siempre antes de exportar.

Para trabajar una pieza, abre su HTML de `piezas/` en el navegador y recarga.
`exportar.mjs afiche-a3` exporta solo esa.

## Detalles técnicos

- **Fuentes incrustadas como CID TrueType subconjuntadas.** Las piezas usan las
  instancias estáticas de `impresos/fuentes/`, no la Montserrat variable:
  Chrome no sabe subconjuntar una variable al exportar PDF y cae a fuentes
  Type 3, que algunos RIP manejan mal. Las genera `scripts/fuentes-estaticas.py`.
- **Área segura de 6 mm** desde el recorte. Nada crítico vive fuera de ahí.
- **QR con corrección de errores alta (H).** En impreso el código se ensucia,
  se dobla y se raya; con corrección H sigue leyéndose.
- Los datos de contacto están en `datos.json`, pero hoy cada pieza los repite
  en su HTML. Si cambia el teléfono, búscalo en `piezas/*.html`.

## Antes de mandar a imprimir

1. `grep -rn "999 888 777\|atoqlab.pe\|Caminos del Inca" impresos/piezas/` y
   reemplaza los datos ficticios.
2. Vuelve a generar los QR si cambió el número de WhatsApp.
3. Confirma las cifras técnicas de la ficha con el fabricante de la máquina.
4. Corre `verificar.mjs` y vuelve a exportar.
5. Pide prueba de color impresa para el afiche y el roll-up.
