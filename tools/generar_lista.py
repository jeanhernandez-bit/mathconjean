#!/usr/bin/env python3
"""Recorre <curso>/parcial-N/<carpeta>/ y escribe materiales.json."""
import hashlib, json, os, re
from urllib.parse import quote

BASES = (".", "pdf")   # carpetas de cursos: en la raiz del repositorio o dentro de pdf/
CATS = ("material-gratis", "quiz", "parciales")

def titulo(nombre):
    t = os.path.splitext(nombre)[0]
    t = re.sub(r"^\d+[\s._-]+", "", t)      # quita "01-" del inicio
    t = re.sub(r"(?<!\d)-|-(?!\d)", " ", t.replace("_", " "))
    return re.sub(r"\s+", " ", t).strip() or nombre

def huella(ruta):
    h = hashlib.sha1()
    with open(ruta, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()[:10]

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
        # Estructura alterna: <curso>/parciales/parcial-N/archivo.pdf
        alt = os.path.join(cdir, "parciales")
        if os.path.isdir(alt):
            for par in sorted(os.listdir(alt), key=natural):
                m = re.fullmatch(r"parcial-(\d+)", par)
                kdir = os.path.join(alt, par)
                if not m or not os.path.isdir(kdir):
                    continue
                files = sorted((f for f in os.listdir(kdir) if f.lower().endswith(".pdf")), key=natural)
                if files:
                    partes = [] if base == "." else [base]
                    lst = data.setdefault(curso, {}).setdefault(m.group(1), {}).setdefault("parciales", [])
                    lst += [{"t": titulo(f), "f": "/".join(quote(x) for x in partes + [curso, "parciales", par, f]), "v": huella(os.path.join(kdir, f))} for f in files]
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
                    lst = data.setdefault(curso, {}).setdefault(m.group(1), {}).setdefault(cat, [])
                    lst += [
                        {"t": titulo(f), "f": "/".join(quote(x) for x in partes + [curso, par, cat, f]), "v": huella(os.path.join(kdir, f))}
                        for f in files
                    ]

with open("materiales.json", "w", encoding="utf-8") as fh:
    json.dump(data, fh, ensure_ascii=False, indent=1)

# version.json: huella de cada archivo de datos. La pagina la consulta primero
# y solo vuelve a descargar materiales.json o videos.txt si su huella cambio.
ver = {"m": huella("materiales.json")}
for archivo, clave in (("videos.txt", "v"), ("destacados.txt", "d")):
    if os.path.isfile(archivo):
        ver[clave] = huella(archivo)
with open("version.json", "w", encoding="utf-8") as fh:
    json.dump(ver, fh)
print("materiales.json:", sum(len(v) for c in data.values() for p in c.values() for v in p.values()), "archivos")
