# theme.py — design tokens for the make-ppt visual grammar.
# Values are extracted from the fixed visual reference (AI_Agentic_Coding_導入實戰.pdf).
# Every slide module imports from here. Never hardcode colors/sizes in slide code.

import os, subprocess
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor

# ---------------------------------------------------------------- canvas
SLIDE_W = Inches(13.333)   # 16:9 widescreen
SLIDE_H = Inches(7.5)

MARGIN_X = Inches(0.62)    # left/right page margin
EYEBROW_Y = Inches(0.42)   # eyebrow baseline area
TITLE_Y = Inches(0.86)     # title top for standard content slides
CONTENT_W = SLIDE_W - 2 * MARGIN_X

# ---------------------------------------------------------------- palette
BG        = RGBColor(0xFA, 0xF8, 0xF4)  # warm off-white / light ivory
INK       = RGBColor(0x1A, 0x17, 0x14)  # near-black (also dark panel/section bg)
INK_SOFT  = RGBColor(0x4A, 0x44, 0x3D)  # dark warm gray body text
MUTED     = RGBColor(0x8A, 0x81, 0x77)  # supporting / inactive warm gray
HAIRLINE  = RGBColor(0xDE, 0xD8, 0xCE)  # thin dividers
PANEL_BG  = RGBColor(0xFF, 0xFF, 0xFE)  # light card/panel fill (barely off bg)
PANEL_LN  = RGBColor(0xE4, 0xDE, 0xD4)  # light panel border

ORANGE    = RGBColor(0xD7, 0x5F, 0x00)  # primary emphasis (decisive phrases, key arrows, rules)
ORANGE_SOFT = RGBColor(0xF6, 0xE3, 0xD2)  # pale orange fill for highlighted chips inside panels
GREEN     = RGBColor(0x3E, 0x8E, 0x5A)  # success / accepted / human checkpoint
RED       = RGBColor(0xC1, 0x32, 0x27)  # risk / rejected / vulnerability / failure
BLUE      = RGBColor(0x39, 0x72, 0xDA)  # information / tool / technical category
DARK_PANEL = RGBColor(0x1F, 0x1B, 0x17) # terminal panel background
DARK_PANEL_TXT = RGBColor(0xE9, 0xE4, 0xDC)
DARK_PANEL_MUTED = RGBColor(0x8F, 0x87, 0x7C)

ON_DARK   = RGBColor(0xF5, 0xF2, 0xEC)  # primary text on dark backgrounds

# ---------------------------------------------------------------- type scale (pt)
# Fixed 2pt-stepped ladder. Two hard rules hold across every deck:
#   1. Nothing renders below MIN_PT (12pt).
#   2. Every text size sits on the 2pt grid (all tokens are even).
# snap_pt() (below) enforces both at run time, so any ad-hoc size a slide passes is
# pulled onto the grid — but slide code should still use these named tokens.
MIN_PT      = 12     # floor — no text on any slide is smaller than this
STEP_PT     = 2      # size ladder increments by 2pt

S_TITLE     = 28     # content-slide argument title — target size; kept to one line (see TITLE_MIN)
S_TITLE_MIN = 22     # title auto-fit floor: shrink on the 2pt grid only as far as this to avoid wrapping
S_TITLE_BIG = 40     # cover / section-divider display hero (a different register, not a page title)
S_SECTION_NUM = 150  # giant section number (display numeral)

S_TAKEAWAY  = 20     # bottom takeaway conclusion
S_SUPPORT   = 16     # supporting sentence / sub-heading  ("小標")
S_BODY      = 14     # body text  ("內文")
S_EYEBROW   = 12     # eyebrow metadata (== MIN_PT, matches mono)
S_LABEL     = 12     # pills / status labels  (== MIN_PT)
S_MONO      = 12     # mono metadata          (== MIN_PT)

def snap_pt(size):
    """Clamp a point size to the >=MIN_PT floor and snap it onto the 2pt grid, so the
    two type rules always hold even if slide code passes an off-grid value (13 -> 14,
    11 -> 12, 9.5 -> 10, 8 -> 10). Display sizes are already even, so they pass through."""
    s = max(MIN_PT, int(round(float(size))))
    if s % STEP_PT:
        s += 1
    return s

# ---------------------------------------------------------------- fonts
def _installed_font_families() -> str:
    """Enumerate installed font family names, cross-platform. Probed once and cached."""
    # Linux / macOS: fontconfig
    try:
        r = subprocess.run(["fc-list", ":family"], capture_output=True, text=True, timeout=10)
        if r.returncode == 0 and r.stdout.strip():
            return r.stdout
    except Exception:
        pass
    # Windows: family names are the value names under the Fonts registry keys
    if os.name == "nt":
        chunks = []
        for root in ("HKLM", "HKCU"):
            key = root + r"\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts"
            try:
                r = subprocess.run(["reg", "query", key], capture_output=True, text=True, timeout=10)
                chunks.append(r.stdout)
            except Exception:
                pass
        return "\n".join(chunks)
    return ""

_FONT_FAMILIES = _installed_font_families()

def _fc_has(family: str) -> bool:
    return family.lower() in _FONT_FAMILIES.lower()

def pick_font(candidates, fallback):
    """Return the first installed family; verify before committing (no blind fallback)."""
    for c in candidates:
        if _fc_has(c):
            return c
    return fallback

# CJK display/body font (heavy weights must exist for editorial titles)
FONT_CJK = pick_font(
    ["Noto Sans TC", "Noto Sans CJK TC", "Noto Sans CJK JP", "Microsoft JhengHei", "PingFang TC"],
    "Noto Sans CJK TC",
)
# Mono font for eyebrows, code, protocol labels, technical metadata
FONT_MONO = pick_font(
    ["JetBrains Mono", "Cascadia Code", "IBM Plex Mono", "Noto Sans Mono", "DejaVu Sans Mono", "Consolas"],
    "Courier New",
)

# ---------------------------------------------------------------- deck context
# The mono context line on dark cover/section slides. Set this ONCE per deck to what
# the deck actually is — topic, team, and/or date (e.g. "技術分享 / 2026-07",
# "平台組 · Agent 導入回顧"). It must be true: never invent event or summit branding
# (no "20XX ___ SUMMIT / TAIWAN" chrome) — this deck is shared with 同仁, not hosted
# at a conference.
DECK_CONTEXT = "技術分享"

# ---------------------------------------------------------------- misc metrics
RULE_W = Pt(1.0)          # hairline weight
ACCENT_RULE_W = Pt(2.25)  # orange takeaway rule weight
RADIUS_SMALL = 0.06       # rounded-rect adjustment for pills/panels (0..0.5)
