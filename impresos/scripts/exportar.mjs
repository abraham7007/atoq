/* HTML -> PDF vectorial (Playwright) + PNG a 300 dpi.

   El PDF sale en RGB con las fuentes incrustadas; scripts/cmyk.mjs hace
   despues la conversion a CMYK con Ghostscript. */
import { chromium } from "playwright";
import { readdirSync, mkdirSync, existsSync } from "node:fs";
import { basename } from "node:path";

const DIR = "impresos/piezas";
const PDF = "impresos/pdf/rgb";
const PNG = "impresos/png";
const DPI = 300;
const PX_POR_MM = 96 / 25.4;                 // 1 mm en px CSS
const ESCALA = DPI / 96;                     // deviceScaleFactor para 300 dpi

/* Tamaño de recorte de cada pieza, en mm. El sangrado (3 mm por lado) lo suma
   el sistema, por eso la pagina siempre mide 6 mm mas que el recorte. */
const PIEZAS = {
  "afiche-a3":      { w: 297, h: 420, nombre: "Afiche A3" },
  "volante-a5":     { w: 148, h: 210, nombre: "Volante A5, dos caras" },
  "triptico-a4":    { w: 297, h: 210, nombre: "Tríptico A4, dos caras" },
  "tarjeta":        { w: 90,  h: 50,  nombre: "Tarjeta de presentación, dos caras" },
  "ficha-tecnica":  { w: 210, h: 297, nombre: "Ficha técnica A4" },
  "membretada":     { w: 210, h: 297, nombre: "Hoja membretada A4" },
  "rollup":         { w: 850, h: 2000, nombre: "Roll-up 85 × 200 cm", sangrado: 20, png: false },
  /* Piezas de pantalla: se miden en px, no llevan sangrado y no van a PDF. */
  "promo-post":     { w: 1080, h: 1080, nombre: "Post promocional 1:1",  px: true },
  "promo-historia": { w: 1080, h: 1920, nombre: "Historia promocional",  px: true },
};

const solo = process.argv.slice(2).filter((a) => !a.startsWith("--"));
const guias = process.argv.includes("--guias");

mkdirSync(PDF, { recursive: true });
mkdirSync(PNG, { recursive: true });

const browser = await chromium.launch();
const base = `file://${process.cwd()}/${DIR}/`;

for (const archivo of readdirSync(DIR).filter((f) => f.endsWith(".html")).sort()) {
  const slug = basename(archivo, ".html");
  const spec = PIEZAS[slug];
  if (!spec) { console.log(`· sin ficha en el manifiesto: ${slug}`); continue; }
  if (solo.length && !solo.includes(slug)) continue;

  const s = spec.px ? 0 : (spec.sangrado ?? 3);
  const pw = spec.w + s * 2, ph = spec.h + s * 2;
  const aPx = (mm) => (spec.px ? Math.round(mm) : Math.round(mm * PX_POR_MM));

  if (spec.px) {
    // Pieza de pantalla: PNG 1:1, sin PDF ni sangrado.
    const p = await browser.newPage({ viewport: { width: pw, height: ph }, deviceScaleFactor: 1 });
    await p.goto(base + archivo, { waitUntil: "networkidle" });
    await p.waitForTimeout(400);
    const salidaPng = `${PNG}/${slug}_${pw}x${ph}.png`;
    await p.locator(".pieza").first().screenshot({ path: salidaPng });
    console.log(`✓ ${salidaPng.replace("impresos/", "")}`);
    await p.close();
    continue;
  }

  const page = await browser.newPage({
    viewport: { width: aPx(pw), height: aPx(ph) },
    deviceScaleFactor: 1,
  });
  await page.goto(base + archivo, { waitUntil: "networkidle" });
  if (guias) await page.evaluate(() => document.body.classList.add("guias"));
  await page.waitForTimeout(400);

  const caras = await page.locator(".pieza").count();
  const salida = `${PDF}/${slug}_${spec.w}x${spec.h}mm_sangrado${s}mm.pdf`;
  await page.pdf({ path: salida, printBackground: true, preferCSSPageSize: true,
                   margin: { top: 0, right: 0, bottom: 0, left: 0 } });
  console.log(`✓ ${salida.replace("impresos/", "")}  ${caras} cara(s)`);

  if (spec.png !== false) {
    await page.close();
    const p2 = await browser.newPage({
      viewport: { width: aPx(pw), height: aPx(ph) },
      deviceScaleFactor: ESCALA,
    });
    await p2.goto(base + archivo, { waitUntil: "networkidle" });
    await p2.waitForTimeout(300);
    const bloques = await p2.locator(".pieza").all();
    for (const [i, b] of bloques.entries()) {
      const sufijo = bloques.length > 1 ? `-cara${i + 1}` : "";
      await b.screenshot({ path: `${PNG}/${slug}${sufijo}@300dpi.png` });
    }
    console.log(`  ${PNG}/${slug}*@300dpi.png`);
    await p2.close();
  } else {
    await page.close();
  }
}
await browser.close();
