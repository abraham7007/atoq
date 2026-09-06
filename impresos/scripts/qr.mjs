/* Codigos QR en SVG. En impreso son el unico puente directo al canal digital. */
import QRCode from "qrcode";
import { readFileSync, writeFileSync, mkdirSync } from "node:fs";

const d = JSON.parse(readFileSync("impresos/datos.json", "utf8"));
mkdirSync("impresos/piezas/qr", { recursive: true });

const destinos = {
  whatsapp: `https://wa.me/${d.whatsapp}?text=${encodeURIComponent(d.whatsappMensaje)}`,
  web: d.webUrl,
};

for (const [nombre, url] of Object.entries(destinos)) {
  // Correccion alta: en impreso el codigo se ensucia, se dobla y se raya.
  const svg = await QRCode.toString(url, {
    type: "svg", errorCorrectionLevel: "H", margin: 0,
    color: { dark: "#192851", light: "#0000" },
  });
  writeFileSync(`impresos/piezas/qr/${nombre}.svg`, svg);

  const blanco = svg.replace(/#192851/g, "#FFFFFF");
  writeFileSync(`impresos/piezas/qr/${nombre}-blanco.svg`, blanco);
  console.log(`✓ qr/${nombre}.svg  ->  ${url.slice(0, 62)}`);
}
