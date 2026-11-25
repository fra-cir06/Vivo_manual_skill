#!/usr/bin/env python3
"""Controllo di qualità del PDF compilato.

Uso:  python3 controlla_pdf.py main.pdf
- trova «--» letterali e altri resti di markup nel testo estratto;
- segnala pagine quasi vuote e frammenti isolati in cima alla pagina;
- crea i fogli di anteprima qa/foglio-N.png (12 pagine ciascuno) da guardare.
Esce con codice 1 se trova problemi certi (markup grezzo).
"""
import glob
import pathlib
import re
import subprocess
import sys

from PIL import Image

pdf = pathlib.Path(sys.argv[1])
qa = pdf.parent / "qa"
qa.mkdir(exist_ok=True)
for vecchio in qa.glob("*.png"):
    vecchio.unlink()

n = int(re.search(r"Pages:\s+(\d+)",
                  subprocess.run(["pdfinfo", pdf], capture_output=True,
                                 text=True).stdout).group(1))
errori, avvisi = [], []
RESTI = [(r"(?<![-\w])--(?!-)", "«--» letterale (usa –)"),
         (r"\\[a-zA-Z]+\{", "comando LaTeX non interpretato"),
         (r"\?\?", "riferimento non risolto (??)"),
         (r"¤", "delimitatore dei listing rimasto nel testo")]

for p in range(1, n + 1):
    testo = subprocess.run(["pdftotext", "-layout", "-f", str(p), "-l",
                            str(p), pdf, "-"], capture_output=True,
                           text=True).stdout
    for regex, msg in RESTI:
        for m in re.finditer(regex, testo):
            riga = testo[:m.start()].count("\n")
            frammento = testo.splitlines()[riga].strip()[:70]
            errori.append(f"p. {p}: {msg} → «{frammento}»")
    righe = [r.strip() for r in testo.splitlines() if r.strip()]
    if p > 2 and len(righe) > 2:
        prima = righe[1]          # righe[0] è l'intestazione
        solo_chiusura = re.fullmatch(r"[\)\]\}\s,;:.]+", prima)
        fine_frase = len(prima.split()) <= 3 and prima.endswith((".", ";", ":"))
        if solo_chiusura or fine_frase:
            avvisi.append(f"p. {p}: frammento isolato in cima → «{prima}»")

subprocess.run(["pdftoppm", "-r", "45", "-png", pdf, qa / "p"], check=True)
pagine = sorted(glob.glob(str(qa / "p-*.png")))
for i, f in enumerate(pagine, 1):
    im = Image.open(f).convert("L")
    w, h = im.size
    corpo = im.crop((0, int(h * .07), w, int(h * .90)))   # senza testata/piede
    bbox = corpo.point(lambda v: 255 if v < 200 else 0).getbbox()
    riemp = bbox[3] / corpo.size[1] if bbox else 0
    if 2 < i < len(pagine) and riemp < 0.40:
        avvisi.append(f"p. {i}: pagina piena solo al {riemp:.0%} "
                      "(accettabile solo se un blocco intero è slittato)")
for k in range(0, len(pagine), 12):
    ims = [Image.open(f) for f in pagine[k:k + 12]]
    w, h = ims[0].size
    foglio = Image.new("RGB", (w * 6, h * 2), "white")
    for j, im in enumerate(ims):
        foglio.paste(im, ((j % 6) * w, (j // 6) * h))
    foglio.save(qa / f"foglio-{k // 12 + 1}.png")
for f in pagine:
    pathlib.Path(f).unlink()

print(f"{n} pagine controllate")
for e in errori:
    print("  ✗", e)
for a in avvisi:
    print("  ⚠", a)
print(f"Fogli di anteprima in {qa}/ — guardali tutti prima di consegnare.")
sys.exit(1 if errori else 0)
