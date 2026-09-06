/* SVG -> PNG. Los logos salen en dos resoluciones; las piezas de redes, en su
   tamaño exacto, que es lo que cada plataforma espera. */
import sharp from "sharp";
import { readdirSync, readFileSync, mkdirSync } from "node:fs";

const D = { density: 1200 };
const kb = (n) => `${(n / 1024).toFixed(0)} KB`;

mkdirSync("logos/png", { recursive: true });
mkdirSync("redes/png", { recursive: true });
mkdirSync("logos/png/favicon", { recursive: true });

console.log("logos/png  (1000 y 2000 px de ancho, fondo transparente)");
for (const f of readdirSync("logos/svg").filter((f) => f.endsWith(".svg"))) {
  const base = f.replace(".svg", "");
  for (const w of [1000, 2000]) {
    const out = `logos/png/${base}@${w}.png`;
    const i = await sharp(readFileSync(`logos/svg/${f}`), D)
      .resize({ width: w }).png({ compressionLevel: 9 }).toFile(out);
    if (w === 1000) console.log(`  ${base.padEnd(34)} ${i.width}x${i.height}  ${kb(i.size)}`);
  }
}

console.log("\nredes/png  (tamaño exacto de cada plataforma)");
for (const f of readdirSync("redes/svg").filter((f) => f.endsWith(".svg"))) {
  const svg = readFileSync(`redes/svg/${f}`);
  const out = `redes/png/${f.replace(".svg", ".png")}`;
  // Estos SVG ya declaran el tamaño exacto de destino: renderizarlos a mayor
  // densidad solo genera un intermedio gigante que revienta el limite de sharp.
  const i = await sharp(svg).png({ compressionLevel: 9 }).toFile(out);
  console.log(`  ${f.replace(".svg", "").padEnd(34)} ${i.width}x${i.height}  ${kb(i.size)}`);
}

console.log("\nfavicon");
for (const s of [16, 32, 48, 180, 192, 512]) {
  const out = `logos/png/favicon/favicon-${s}.png`;
  await sharp(readFileSync("logos/svg/atoqlab-favicon.svg"), D)
    .resize(s, s).png({ compressionLevel: 9 }).toFile(out);
  console.log(`  favicon-${s}.png`);
}
