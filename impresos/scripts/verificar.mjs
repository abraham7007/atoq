/* Avisa si el contenido de alguna pieza se sale del area segura.
   Un desborde aqui significa texto cortado en la imprenta. */
import { chromium } from "playwright";
import { readdirSync } from "node:fs";

const b = await chromium.launch();
let fallos = 0;

for (const f of readdirSync("impresos/piezas").filter((f) => f.endsWith(".html")).sort()) {
  const p = await b.newPage({ viewport: { width: 1600, height: 2400 } });
  await p.goto(`file://${process.cwd()}/impresos/piezas/${f}`, { waitUntil: "networkidle" });
  await p.waitForTimeout(250);

  const r = await p.evaluate(() =>
    [...document.querySelectorAll(".seguro, .panel")].map((el, i) => {
      const caja = el.getBoundingClientRect();
      const ultimo = el.lastElementChild?.getBoundingClientRect();
      return {
        i, desborde: ultimo ? Math.round(ultimo.bottom - caja.bottom) : 0,
        clase: el.className.split(" ")[0],
      };
    }));

  const malos = r.filter((x) => x.desborde > 1);
  if (malos.length) {
    fallos += malos.length;
    console.log(`⚠ ${f}`);
    for (const m of malos) console.log(`    ${m.clase} #${m.i + 1} se pasa ${m.desborde}px del borde`);
  } else {
    console.log(`✓ ${f}`);
  }
  await p.close();
}
await b.close();
if (fallos) { console.log(`\n${fallos} desborde(s). Revisa antes de mandar a imprenta.`); process.exit(1); }
console.log("\nTodas las piezas caben en su área segura.");
