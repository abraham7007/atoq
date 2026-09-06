/* Manual de marca -> PDF A4.

   Inyecta las instancias estaticas de Montserrat solo para imprimir: Chrome no
   sabe subconjuntar una fuente variable al exportar PDF y cae a fuentes Type 3.
   El HTML sigue usando la variable, que pesa la sexta parte en el navegador. */
import { chromium } from "playwright";
import { statSync } from "node:fs";

const RAIZ = process.cwd();
const SALIDA = "atoqlab-manual-de-marca.pdf";

const estaticas = ["Regular", "Medium", "SemiBold", "Bold", "ExtraBold"]
  .map((n, i) => `@font-face{font-family:"Montserrat Print";font-weight:${[400,500,600,700,800][i]};
      font-style:normal;src:url("file://${RAIZ}/impresos/fuentes/Montserrat-${n}.ttf") format("truetype")}`)
  .join("\n") + `\nbody,.arbol{font-family:"Montserrat Print",Montserrat,sans-serif !important}
      code,.arbol{font-family:ui-monospace,Menlo,monospace !important}`;

const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto(`file://${RAIZ}/manual-de-marca.html`, { waitUntil: "networkidle" });
await page.addStyleTag({ content: estaticas });
await page.evaluate(() => document.fonts.ready);
await page.waitForTimeout(600);

await page.pdf({
  path: SALIDA,
  // Los margenes se fijan aqui, no en el @page: con displayHeaderFooter activo
  // Chrome reserva espacio extra para el pie y recorta la caja de contenido.
  // Area util resultante: 269 x 180 mm.
  format: "A4",
  landscape: true,
  printBackground: true,
  preferCSSPageSize: false,
  margin: { top: "14mm", right: "14mm", bottom: "16mm", left: "14mm" },
  displayHeaderFooter: true,
  headerTemplate: "<span></span>",
  footerTemplate: `<div style="width:100%;padding:0 14mm;font:400 7pt Helvetica;color:#8A93A8;
      display:flex;justify-content:space-between">
      <span>atoqlab · Manual de marca v1.0 preliminar</span>
      <span class="pageNumber"></span></div>`,
});

await browser.close();
console.log(`✓ ${SALIDA}  ${Math.round(statSync(SALIDA).size / 1024)} KB`);
