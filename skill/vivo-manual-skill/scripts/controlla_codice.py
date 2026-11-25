#!/usr/bin/env python3
"""Controlla gli script didattici prima di includerli nel manuale.

Uso:  python3 controlla_codice.py code/*.py   (dalla cartella del manuale)
- righe al massimo di 78 caratteri;
- import tutti in testa al file e nessun import inutilizzato;
- lo script gira senza errori né warning; l'output viene salvato in
  output/<nome>.txt per essere incluso con \\outputfile.
Esce con codice 1 se trova problemi.
"""
import ast
import pathlib
import subprocess
import sys

MAX = 78
problemi = 0


def segnala(f, msg):
    global problemi
    problemi += 1
    print(f"  ✗ {f}: {msg}")


for nome in sys.argv[1:]:
    f = pathlib.Path(nome)
    testo = f.read_text(encoding="utf-8")
    print(f"• {f.name}")
    for i, riga in enumerate(testo.splitlines(), 1):
        if len(riga) > MAX:
            segnala(f.name, f"riga {i} lunga {len(riga)} caratteri (max {MAX})")
    albero = ast.parse(testo)
    importati, fine_testa = {}, True
    for nodo in albero.body:
        e_import = isinstance(nodo, (ast.Import, ast.ImportFrom))
        e_doc = (isinstance(nodo, ast.Expr)
                 and isinstance(nodo.value, ast.Constant))
        if e_import and not fine_testa:
            segnala(f.name, f"import non in testa (riga {nodo.lineno})")
        if not (e_import or e_doc):
            fine_testa = False
    for nodo in ast.walk(albero):
        if isinstance(nodo, (ast.Import, ast.ImportFrom)):
            for a in nodo.names:
                nome_locale = (a.asname or a.name).split(".")[0]
                importati[nome_locale] = nodo.lineno
    usati = {n.id for n in ast.walk(albero) if isinstance(n, ast.Name)}
    usati |= {n.value.id for n in ast.walk(albero)
              if isinstance(n, ast.Attribute) and isinstance(n.value, ast.Name)}
    for n, riga in importati.items():
        if n not in usati:
            segnala(f.name, f"import inutilizzato '{n}' (riga {riga})")
    r = subprocess.run([sys.executable, "-W", "always", f.name],
                       cwd=f.parent, capture_output=True, text=True)
    if r.returncode != 0:
        segnala(f.name, "errore in esecuzione:\n" + r.stderr[-800:])
    elif "Warning" in r.stderr:
        segnala(f.name, "warning in esecuzione:\n" + r.stderr[-800:])
    out = f.parent.parent / "output" / (f.stem + ".txt")
    out.parent.mkdir(exist_ok=True)
    out.write_text(r.stdout, encoding="utf-8")
    for i, riga in enumerate(r.stdout.splitlines(), 1):
        if len(riga) > 90:
            segnala(f.name, f"riga {i} dell'output lunga {len(riga)} caratteri")

print("OK: nessun problema" if problemi == 0 else f"{problemi} problemi")
sys.exit(1 if problemi else 0)
