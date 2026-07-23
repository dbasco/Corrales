#!/usr/bin/env python3
"""
Genera una copia de dist/ navegable con file:// (doble clic), reescribiendo las
rutas absolutas (/assets/..., /visita/) a relativas y apuntando los enlaces de
directorio a index.html.

Uso:  python3 scripts/build_local_preview.py [dist] [dist-local]

Solo para revisión en local. Lo que se sube al servidor es dist/ tal cual: en
producción las rutas absolutas son las correctas.
"""
import re, shutil, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "dist"
DST = Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / "dist-local"

# No tocar: metadatos que deben seguir siendo absolutos (canonical, og:url, hreflang, JSON-LD)
SKIP_ATTRS = re.compile(r'(?:rel="canonical"|property="og:url"|rel="alternate")')


def to_rel(target: str, depth: int) -> str:
    """/visita/ + depth 1  ->  ../visita/index.html"""
    frag = ""
    if "#" in target:
        target, frag = target.split("#", 1)
        frag = "#" + frag
    t = target.lstrip("/")
    if t == "":
        t = "index.html"
    elif t.endswith("/"):
        t += "index.html"
    prefix = "../" * depth
    return prefix + t + frag


def rewrite(html: str, depth: int) -> str:
    def attr(m):
        head, q, val = m.group(1), m.group(2), m.group(3)
        # respetar protocolo, protocol-relative, anclas puras, mailto/tel
        if not val.startswith("/") or val.startswith("//"):
            return m.group(0)
        return f'{head}={q}{to_rel(val, depth)}{q}'

    # href="/..." y src="/..."
    html = re.sub(r'\b(href|src)=("|\')(/[^"\']*)\2', attr, html)
    # url(/assets/...) dentro de CSS/style inline
    html = re.sub(r'url\((/[^)\'"]+)\)', lambda m: f'url({to_rel(m.group(1), depth)})', html)
    return html


def main():
    if not SRC.exists():
        sys.exit(f"No existe {SRC}. Ejecuta antes: python3 build.py")
    if DST.exists():
        shutil.rmtree(DST)
    shutil.copytree(SRC, DST)

    n = 0
    for f in DST.rglob("*.html"):
        depth = len(f.relative_to(DST).parts) - 1
        original = f.read_text(encoding="utf-8")
        # preservar las líneas de canonical/og:url/hreflang intactas
        keep = {}
        def stash(m):
            k = f"@@KEEP{len(keep)}@@"
            keep[k] = m.group(0)
            return k
        tmp = re.sub(r'<link[^>]*rel="(?:canonical|alternate)"[^>]*>|<meta[^>]*property="og:url"[^>]*>', stash, original)
        tmp = rewrite(tmp, depth)
        for k, v in keep.items():
            tmp = tmp.replace(k, v)
        f.write_text(tmp, encoding="utf-8")
        n += 1
    print(f"OK: {n} páginas reescritas a rutas relativas en {DST}")


if __name__ == "__main__":
    main()
