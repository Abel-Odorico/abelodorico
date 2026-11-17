#!/usr/bin/env python3
"""Recolore os cards gerados pelo github-cool-readme com a paleta ADL.

Uso: adl_recolor.py <pasta-com-svgs>

Cada card tem versao -dark e -light. As cores originais sao fixas no SVG,
entao trocamos cada uma por uma cor da paleta ADL (9 cores, paleta fechada):
azul #0B1F3B, petroleo #0A4D5C, terracota #B85C4E, dourado #C9A961,
branco #FAF8F5, areia #D4C4B0, carvao #2D3436, oliva #7A8B7F, bordo #6B2E3E.
Cores de linguagens (barra de linguagens) sao mantidas: carregam significado.
"""
import re
import sys
from pathlib import Path

AZUL, PETROLEO, TERRACOTA = "#0B1F3B", "#0A4D5C", "#B85C4E"
DOURADO, BRANCO, AREIA = "#C9A961", "#FAF8F5", "#D4C4B0"
CARVAO, OLIVA = "#2D3436", "#7A8B7F"

THEMES = {
    "dark": {
        "bg": (AZUL, PETROLEO),
        "map": {
            "#f0f6fc": BRANCO,    # texto principal
            "#9198a1": AREIA,     # texto secundario / icones
            "#7d8590": OLIVA,     # texto apagado
            "#6e7681": OLIVA,
            "#3d444d": PETROLEO,  # trilhas e divisores
            "#ffab1a": DOURADO,   # destaque
            "#d98a00": OLIVA,     # barras: intensidade media
            "#8f5200": PETROLEO,  # barras: intensidade baixa
        },
    },
    "light": {
        "bg": (BRANCO, AREIA),
        "map": {
            "#1f2328": AZUL,
            "#59636e": CARVAO,
            "#818b98": OLIVA,
            "#8c959f": OLIVA,
            "#d1d9e0": AREIA,
            "#b35c00": PETROLEO,
            "#e08a00": PETROLEO,
            "#f0a020": AREIA,     # barras: intensidade baixa
            "#c26a00": OLIVA,     # barras: intensidade media
            "#9a4d00": PETROLEO,  # barras: intensidade alta
        },
    },
}

BG_RECT = re.compile(r'(<rect x="0\.5" y="0\.5"[^>]*?)fill="none" stroke="none"')


def recolor(path: Path, theme: dict) -> bool:
    svg = path.read_text(encoding="utf-8")
    for old, new in theme["map"].items():
        svg = re.sub(re.escape(old) + r"(?![0-9a-fA-F])", new, svg, flags=re.I)
    fill, stroke = theme["bg"]
    svg, n = BG_RECT.subn(rf'\1fill="{fill}" stroke="{stroke}"', svg, count=1)
    path.write_text(svg, encoding="utf-8")
    return n == 1


def main() -> int:
    folder = Path(sys.argv[1])
    for path in sorted(folder.glob("*.svg")):
        mode = "dark" if path.stem.endswith("-dark") else "light" if path.stem.endswith("-light") else None
        if mode is None:
            continue
        if not recolor(path, THEMES[mode]):
            print(f"::warning::fundo nao encontrado em {path.name}; cores aplicadas sem fundo")
    return 0


if __name__ == "__main__":
    sys.exit(main())
