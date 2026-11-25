# Manuali PDF in stile «dispensa»

Skill per Claude e sorgenti LaTeX per produrre manuali di studio in PDF con uno stile grafico fisso (font, box colorati, banner dei capitoli) adattato all'argomento. I contenuti si basano su fonti ufficiali e sono controllati automaticamente prima della consegna.

## Contenuto

```
manuali-pdf/
├── skill/design-manuale-pdf-skill/SKILL.md   la skill completa (regole + template)
├── strumenti/
│   ├── controlla_codice.py                   controllo degli script didattici
│   └── controlla_pdf.py                      controllo di qualità del PDF
├── template/                                 template minimo pronto da compilare
├── manuali/                                  sorgenti dei manuali prodotti
│   ├── classificatore-bayes/
│   ├── kathara-basic-ipv4/
│   ├── random-forest/
│   └── modello-er/
└── pdf/                                      i PDF compilati
```

| Manuale | Tipo | Versione della skill |
|---|---|---|
| Classificatore di Bayes | teorico, con formule | v1 |
| Kathará, lab basic-ipv4 | tecnico, comandi e reti | v1 |
| Random Forest | teorico e codice Python | v1 (da rigenerare con le regole v2) |
| Modello Entity-Relationship | teorico, schemi E-R in TikZ | v2 |

## Requisiti

- TeX Live con **XeLaTeX** e i pacchetti `tcolorbox`, `tikz`, `listings`, `fontspec`, `needspace`, `titlesec`, `fancyhdr`, `tocloft`, `enumitem`.
- Font: TeX Gyre Pagella, Fira Sans (Light, Regular, SemiBold, ExtraBold), DejaVu Sans Mono.
- Python 3 con `matplotlib`, `Pillow`; `scikit-learn` per il manuale Random Forest.
- `poppler-utils` (`pdftotext`, `pdftoppm`, `pdfinfo`) per `controlla_pdf.py`.

## Compilare un manuale

```bash
cd manuali/modello-er
xelatex -interaction=nonstopmode main.tex
xelatex -interaction=nonstopmode main.tex      # seconda passata: copertina e indice
python3 ../../strumenti/controlla_pdf.py main.pdf
```

Per il Random Forest, prima rigenera output e figure:

```bash
cd manuali/random-forest/code
python3 es2_pipeline_tuning.py   # crea anche i CSV usati da figs.py
python3 figs.py
```

## Usare la skill

Il file `skill/design-manuale-pdf-skill/SKILL.md` si carica come skill in Claude. Si attiva quando si chiede un PDF descritto come manuale, dispensa, guida o appunti, partendo da documenti forniti oppure solo da un argomento.
