#!/usr/bin/env python3
"""Recorre <curso>/parcial-N/<carpeta>/ y escribe materiales.json."""
import json, os, re
from urllib.parse import quote

BASES = (".", "pdf")   # carpetas de cursos: en la raiz del repositorio o dentro de pdf/
CATS = ("material-gratis", "quiz", "parciales")

def titulo(nombre):
    t = os.path.splitext(nombre)[0]
    t = re.sub(r"^\d+[\s._-]+", "", t)      # quita "01-" del inicio
    t = re.sub(r"(?<!\d)-|-(?!\d)", " ", t.replace("_", " "))
    return re.sub(r"\s+", " ", t).strip() or nombre

def natural(s):
    return [int(p) if p.isdigit() else p.lower() for p in re.split(r"(\d+)", s)]

data = {}
for base in BASES:
    if not os.path.isdir(base):
        continue
    for curso in sorted(os.listdir(base)):
        cdir = os.path.join(base, curso)
        if curso.startswith(".") or not os.path.isdir(cdir):
            continue
        for par in sorted(os.listdir(cdir), key=natural):
            m = re.fullmatch(r"parcial-(\d+)", par)
            pdir = os.path.join(cdir, par)
            if not m or not os.path.isdir(pdir):
                continue
            for cat in CATS:
                kdir = os.path.join(pdir, cat)
                if not os.path.isdir(kdir):
                    continue
                files = sorted((f for f in os.listdir(kdir) if f.lower().endswith(".pdf")), key=natural)
                if files:
                    partes = [] if base == "." else [base]
                    data.setdefault(curso, {}).setdefault(m.group(1), {})[cat] = [
                        {"t": titulo(f), "f": "/".join(quote(x) for x in partes + [curso, par, cat, f])}
                        for f in files
                    ]

with open("materiales.json", "w", encoding="utf-8") as fh:
    json.dump(data, fh, ensure_ascii=False, indent=1)
print("materiales.json:", sum(len(v) for c in data.values() for p in c.values() for v in p.values()), "archivos")
