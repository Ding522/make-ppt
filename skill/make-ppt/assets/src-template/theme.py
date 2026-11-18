# theme.py — design tokens for the make-ppt visual grammar.
# warm-editorial values are extracted from the fixed visual reference
# (AI_Agentic_Coding_導入實戰.pdf); the other palettes reuse the same token semantics.
# Every slide module imports from here. Never hardcode colors/sizes in slide code.

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
# Set PALETTE ONCE per deck from outline.md `Palette`. Every palette defines the same
# tokens with the same semantics, so slide code and primitives never branch on it.
# ORANGE is the palette's single emphasis slot (orange / burnt orange / ink), kept under
# its historical name. ACCENT_ON_DARK is that emphasis on INK / DARK_PANEL surfaces.
PALETTE = "warm-editorial"

PALETTES = {
    # Default: technical shares, adoption stories, case studies, retrospectives.
    "warm-editorial": dict(
        BG="FAF8F4", INK="1A1714", INK_SOFT="4A443D", MUTED="8A8177", HAIRLINE="DED8CE",
        PANEL_BG="FFFFFE", PANEL_LN="E4DED4",
        ORANGE="D75F00", ORANGE_SOFT="F6E3D2", ACCENT_ON_DARK="D75F00",
        GREEN="3E8E5A", RED="C13227", BLUE="3972DA",
        DARK_PANEL="1F1B17", DARK_PANEL_TXT="E9E4DC", DARK_PANEL_MUTED="8F877C",
        ON_DARK="F5F2EC", SOFT_ON_DARK="CFC9C0",
        THEME_TONE_LIGHT="E8DCCB", THEME_TONE_DARK="8C6E54",
    ),
    # Cool slate (based on Nord): architecture, cloud / security, technical specs.
    "nord-slate": dict(
        BG="ECEFF4", INK="2E3440", INK_SOFT="4C566A", MUTED="6F7889", HAIRLINE="D8DEE9",
        PANEL_BG="F7F9FB", PANEL_LN="D2D9E3",
        ORANGE="B8603E", ORANGE_SOFT="F2DDD3", ACCENT_ON_DARK="D08770",
        GREEN="5D8A4E", RED="B04A55", BLUE="3F6A9A",
        DARK_PANEL="3B4252", DARK_PANEL_TXT="D8DEE9", DARK_PANEL_MUTED="8C96A8",
        ON_DARK="ECEFF4", SOFT_ON_DARK="C9D1DD",
        THEME_TONE_LIGHT="C9D3E0", THEME_TONE_DARK="5E81AC",
    ),
    # Black and white: formal documents, printed / grayscale output, audit reports.
    # Emphasis is ink + weight + accent rules, so it never reads as the RED risk color.
    "mono-print": dict(
        BG="FFFFFF", INK="111111", INK_SOFT="444444", MUTED="767676", HAIRLINE="D9D9D9",
        PANEL_BG="FAFAFA", PANEL_LN="D9D9D9",
        ORANGE="111111", ORANGE_SOFT="EEEEEE", ACCENT_ON_DARK="FFFFFF",
        GREEN="2E7D4F", RED="B3261E", BLUE="2B5FA8",
        DARK_PANEL="1E1E1E", DARK_PANEL_TXT="EAEAEA", DARK_PANEL_MUTED="9A9A9A",
        ON_DARK="FFFFFF", SOFT_ON_DARK="CCCCCC",
        THEME_TONE_LIGHT="EEEEEE", THEME_TONE_DARK="777777",
    ),
}

if PALETTE not in PALETTES:
    raise ValueError(f"unknown palette: {PALETTE!r}; choose one of {sorted(PALETTES)}")
_P = {name: RGBColor.from_string(value) for name, value in PALETTES[PALETTE].items()}

BG        = _P["BG"]          # page background
INK       = _P["INK"]         # primary text; also dark section / cover background
INK_SOFT  = _P["INK_SOFT"]    # body text on light bg
MUTED     = _P["MUTED"]       # supporting / inactive
HAIRLINE  = _P["HAIRLINE"]    # thin dividers
PANEL_BG  = _P["PANEL_BG"]    # light card/panel fill (barely off bg)
PANEL_LN  = _P["PANEL_LN"]    # light panel border

ORANGE    = _P["ORANGE"]      # the emphasis color on light surfaces
ORANGE_SOFT = _P["ORANGE_SOFT"]  # pale emphasis fill for highlighted chips inside panels
ACCENT_ON_DARK = _P["ACCENT_ON_DARK"]  # emphasis on INK / DARK_PANEL surfaces
GREEN     = _P["GREEN"]       # success / accepted / human checkpoint
RED       = _P["RED"]         # risk / rejected / vulnerability / failure
BLUE      = _P["BLUE"]        # information / tool / technical category
DARK_PANEL = _P["DARK_PANEL"]  # terminal panel background
DARK_PANEL_TXT = _P["DARK_PANEL_TXT"]
DARK_PANEL_MUTED = _P["DARK_PANEL_MUTED"]

ON_DARK   = _P["ON_DARK"]     # primary text on dark backgrounds
SOFT_ON_DARK = _P["SOFT_ON_DARK"]  # secondary text on dark backgrounds

# ---------------------------------------------------------------- PowerPoint theme
# Written into ppt/theme/theme1.xml by primitives.apply_deck_theme() so manual edits in
# PowerPoint see the deck palette in the theme color picker, and new shapes, text, and
# slides default to it. Slide code still applies explicit RGB values from the palette
# above; these slots never replace those tokens. THEME_TONE_* exist only so the theme
# picker leads with the palette's own tones for manual edits — slide code does not use them.
THEME_NAME = f"make-ppt {PALETTE}"
THEME_TONE_LIGHT = _P["THEME_TONE_LIGHT"]
THEME_TONE_DARK  = _P["THEME_TONE_DARK"]
THEME_COLORS = {
    "dk1": INK,
    "lt1": BG,
    "dk2": INK_SOFT,
    "lt2": HAIRLINE,
    "accent1": ORANGE,
    "accent2": THEME_TONE_LIGHT,
    "accent3": THEME_TONE_DARK,
    "accent4": RED,
    "accent5": GREEN,
    "accent6": BLUE,
    "hlink": BLUE,
    "folHlink": MUTED,
}

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
S_COVER_TITLE_LIGHT = 56  # editorial-light cover hero; may wrap to two deliberate lines
S_COVER_TITLE_DARK = 52   # report-dark cover hero; one or two deliberate lines
S_COVER_SUBTITLE = 18     # cover subtitle / report scope
S_TITLE_BIG = 40     # section-divider display hero (a different register, not a page title)
S_SECTION_NUM = 150  # giant section number (display numeral)

S_TAKEAWAY  = 20     # bottom takeaway conclusion
S_SUPPORT   = 16     # supporting sentence / sub-heading  ("小標")
S_BODY      = 14     # body text  ("內文")
S_TABLE_HEADER = 16  # native table header
S_TABLE_BODY = 14    # native table body; never shrink below this to force fit
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
# Fixed pairing: Noto Sans TC for Chinese/proportional text, Consolas for technical mono.
# Verify both are installed before building; do not silently substitute another family.
FONT_CJK = "Noto Sans TC"
FONT_MONO = "Consolas"

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
TABLE_HEADER_H = Inches(0.52)
TABLE_CELL_MARGIN_X = Inches(0.12)
TABLE_CELL_MARGIN_Y = Inches(0.06)
TABLE_BORDER_W = Pt(1.0)
