/* Convierte los PDF de RGB a CMYK con Ghostscript.

   Es una conversion sin perfil ICC: sirve para que la imprenta reciba un
   archivo ya separado, pero el color final se debe aprobar con una prueba
   sobre el papel real. Si la imprenta prefiere convertir ella misma, dale el
   PDF de pdf/rgb, que suele dar mejor resultado. */
import { execFileSync } from "node:child_process";
import { readdirSync, mkdirSync, statSync } from "node:fs";

const ORIGEN = "impresos/pdf/rgb";
const DESTINO = "impresos/pdf/cmyk";
mkdirSync(DESTINO, { recursive: true });

const kb = (p) => `${Math.round(statSync(p).size / 1024)} KB`;

for (const f of readdirSync(ORIGEN).filter((f) => f.endsWith(".pdf")).sort()) {
  const salida = `${DESTINO}/${f.replace(".pdf", "_CMYK.pdf")}`;
  execFileSync("gs", [
    "-dSAFER", "-dBATCH", "-dNOPAUSE", "-dQUIET",
    "-sDEVICE=pdfwrite",
    "-dPDFSETTINGS=/prepress",
    "-sColorConversionStrategy=CMYK",
    "-dProcessColorModel=/DeviceCMYK",
    "-dConvertCMYKImagesToRGB=false",
    "-dEmbedAllFonts=true", "-dSubsetFonts=true",
    "-dAutoRotatePages=/None",
    "-dDownsampleColorImages=false", "-dDownsampleGrayImages=false",
    `-sOutputFile=${salida}`, `${ORIGEN}/${f}`,
  ]);
  console.log(`✓ ${salida.replace("impresos/", "").padEnd(58)} ${kb(salida)}`);
}
