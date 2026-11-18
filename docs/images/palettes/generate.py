"""Regenerate the README palette previews from theme.PALETTES.

Usage: python docs/images/palettes/generate.py
"""

from __future__ import annotations

import sys
from pathlib import Path
from xml.sax.saxutils import escape

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(REPO / "skill" / "make-ppt" / "assets" / "src-template"))

from theme import PALETTES  # noqa: E402

SANS = "'Noto Sans TC','Microsoft JhengHei','PingFang TC',sans-serif"
MONO = "Consolas,Menlo,monospace"
# Neutral gray so swatch labels stay readable on both GitHub light and dark themes.
LABEL = "8A8A8A"

W, H = 872, 300
SLIDE_W, SLIDE_H = 416, 234
GAP = 40


def text(x, y, s, fill, size, family=SANS, weight="normal", extra=""):
    return (
        f'<text x="{x}" y="{y}" fill="#{fill}" font-family="{family}" '
        f'font-size="{size}" font-weight="{weight}"{extra}>{escape(s)}</text>'
    )


def chip(x, y, w, label, fill, txt):
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="20" rx="4" fill="#{fill}"/>'
        + text(x + w / 2, y + 14, label, txt, 11, weight="bold", extra=' text-anchor="middle"')
    )


def light_slide(p):
    return "\n".join(
        [
            f'<rect x="0.5" y="0.5" width="{SLIDE_W - 1}" height="{SLIDE_H - 1}" '
            f'fill="#{p["BG"]}" stroke="#{p["HAIRLINE"]}"/>',
            text(22, 30, "// 03    交付成果 · 平台組", p["ORANGE"], 10, MONO),
            f'<text x="22" y="60" font-family="{SANS}" font-size="20" font-weight="bold">'
            f'<tspan fill="#{p["INK"]}">部署時間從 40 分鐘降到 </tspan>'
            f'<tspan fill="#{p["ORANGE"]}">8 分鐘</tspan></text>',
            text(22, 82, "瓶頸在映像檔建置，加上快取後大幅縮短", p["INK_SOFT"], 11),
            f'<line x1="22" y1="96" x2="{SLIDE_W - 22}" y2="96" stroke="#{p["HAIRLINE"]}"/>',
            f'<rect x="22" y="110" width="178" height="102" rx="5" '
            f'fill="#{p["PANEL_BG"]}" stroke="#{p["PANEL_LN"]}"/>',
            text(34, 132, "檢查結果", p["MUTED"], 10, MONO),
            chip(34, 142, 48, "通過", p["GREEN"], p["ON_DARK"]),
            chip(88, 142, 48, "風險", p["RED"], p["ON_DARK"]),
            chip(142, 142, 48, "工具", p["BLUE"], p["ON_DARK"]),
            chip(34, 174, 102, "重點標示", p["ORANGE_SOFT"], p["ORANGE"]),
            f'<rect x="214" y="110" width="180" height="102" rx="5" fill="#{p["DARK_PANEL"]}"/>',
            text(228, 136, "$ make build", p["DARK_PANEL_TXT"], 11, MONO),
            text(228, 160, "# cache hit 92%", p["DARK_PANEL_MUTED"], 11, MONO),
            text(228, 184, "→ done in 8m 02s", p["ACCENT_ON_DARK"], 11, MONO, "bold"),
        ]
    )


def dark_cover(p):
    x0 = SLIDE_W + GAP
    return "\n".join(
        [
            f'<rect x="{x0}" y="0" width="{SLIDE_W}" height="{SLIDE_H}" fill="#{p["INK"]}"/>',
            f'<line x1="{x0 + 22}" y1="26" x2="{x0 + SLIDE_W - 22}" y2="26" '
            f'stroke="#{p["ON_DARK"]}" stroke-opacity="0.45"/>',
            text(x0 + 22, 44, "平台組 · 2026-11", p["SOFT_ON_DARK"], 10, MONO),
            text(x0 + 22, 98, "// MONTHLY REPORT", p["ACCENT_ON_DARK"], 10, MONO),
            text(x0 + 22, 136, "十一月交付報告", p["ON_DARK"], 30, weight="bold"),
            f'<rect x="{x0 + 22}" y="152" width="44" height="3" fill="#{p["ACCENT_ON_DARK"]}"/>',
            text(x0 + 22, 180, "範圍：CI/CD、監控、弱點修補", p["SOFT_ON_DARK"], 12),
        ]
    )


SWATCHES = [
    ("BG", "背景"),
    ("INK", "主文字"),
    ("INK_SOFT", "內文"),
    ("ORANGE", "強調"),
    ("DARK_PANEL", "深色面板"),
    ("GREEN", "通過"),
    ("RED", "風險"),
    ("BLUE", "資訊"),
]


def swatches(p):
    parts = []
    step = W / len(SWATCHES)
    top = SLIDE_H + 26
    for i, (key, label) in enumerate(SWATCHES):
        x = i * step
        parts.append(
            f'<rect x="{x + 0.5:.1f}" y="{top + 0.5}" width="28" height="28" rx="4" '
            f'fill="#{p[key]}" stroke="#BBBBBB" stroke-opacity="0.6"/>'
        )
        parts.append(text(f"{x + 36:.1f}", top + 12, label, LABEL, 11))
        parts.append(text(f"{x + 36:.1f}", top + 27, f"#{p[key]}", LABEL, 11, MONO))
    return "\n".join(parts)


def render(name, p):
    body = "\n".join([light_slide(p), dark_cover(p), swatches(p)])
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
        f'viewBox="0 0 {W} {H}" role="img" aria-label="{name} palette preview">\n'
        f"{body}\n</svg>\n"
    )


def main():
    for name, palette in PALETTES.items():
        out = HERE / f"{name}.svg"
        out.write_text(render(name, palette), encoding="utf-8")
        print(out.relative_to(REPO))


if __name__ == "__main__":
    main()
