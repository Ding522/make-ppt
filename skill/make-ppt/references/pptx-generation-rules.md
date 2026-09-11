# PPTX Generation Rules

## Selected technology: python-pptx (verify at runtime)

Evaluated against PptxGenJS for this skill's needs:

| Criterion | python-pptx | PptxGenJS |
|---|---|---|
| Mixed color runs in one paragraph (title emphasis) | first-class (`run.font.color`) | supported but options objects are mutated in place; fragile |
| Native shapes/connectors/arrowheads | full, incl. oxml access for tailEnd | good |
| Deterministic regeneration | pure Python, no build step | needs Node runtime |
| Known corruption footguns | few | many (hex `#`, shadow offsets, stacked-bar labels, combo axes) |
| Reusable primitive layering | clean module imports | clean |

**Decision: python-pptx**, primarily for robust mixed-format text runs (the title
emphasis mechanism is the core of this style) and fewer file-corruption footguns.
At runtime, use the bundled `scripts/run_python.sh` from Bash/WSL/Git Bash or
`scripts/run_python.ps1` from PowerShell. Both select a real Python 3.9+ interpreter.
Check that `import pptx` succeeds; if unavailable, install `python-pptx` using the
active environment's package-management policy. The canonical Python dependencies are
listed in the bundled `requirements.txt`; do not silently switch generation runtimes,
because the validated primitives and structural QA depend on python-pptx.

## Source layout (maintained generation source)

```
presentation/src/
├── build.py          # entry point; deterministic; `run_python.sh build.py` regenerates the deck
├── theme.py          # ALL design tokens (colors, fonts, sizes, margins, rule weights)
├── primitives.py     # reusable grammar primitives (below)
├── relationship_layouts.py # optional timelines, status matrices, layered lists
└── slides/slideNN.py # one module per slide for decks > ~8 slides; smaller decks inline in build.py
```

Copy the validated starter from the skill's `assets/src-template/`. Centralize every
constant in `theme.py` — never redefine colors/sizes in slide code. Create primitives
for repeated grammar; avoid excessive abstraction — this is a portable skill with one
fixed presentation grammar, not a general-purpose presentation framework. Never
overwrite the user's original source materials.

The builder works from `presentation/outline.md` and the source assets it names. The
planner owns complete evidence reading; do not spend builder context re-reading the
full `presentation/evidence/` pack unless the user asks for source re-verification.

## Primitive inventory (assets/src-template/primitives.py — already validated)

`add_background`, `add_eyebrow(number,label)`, `add_argument_title(segments)` (mixed
runs; `[("…", {}), ("decisive", {"color": T.ORANGE}), …]`), `add_supporting_sentence`,
`add_hairline`, `add_takeaway_line(segments, note=)`, `add_panel`,
`add_native_table(headers, rows, col_widths=, alignments=, row_label_col=, merges=)`,
`add_status_pill`, `add_step_marker`, `add_arrow(dashed=, arrow=)`, `add_technical_node`,
`add_terminal_panel(title, lines, badge=)`, `add_metric_callout`,
`add_cover_slide(variant=)`, `add_section_slide`, `add_chip` (auto-width component label, never wraps),
`add_label_panel` (bordered panel with a centered label inside),
`add_photo_slot` (reserved photo region, placeholder by default),
`add_screenshot` (aspect-ratio-preserving fit; degrades to a placeholder if the file
is missing rather than crashing the build). `rich_par` / `textbox` are the text core.
Extend this file for additional grammar (sequence actors/messages, comparison labels,
Kanban columns, gateway blocks) rather than one-off code in slides.

**Use the right primitive — do not hand-roll these recurring structures:**
- An **opening cover** → `add_cover_slide` with the outline's `editorial-light` or
  `report-dark` variant. Never reuse `add_section_slide` for Slide 01. Pass optional
  subtitle/footer content only when the outline contains it.
- A **semantic table** (headers + repeated rows + aligned columns) →
  `add_native_table` (or `relationship_layouts.add_status_matrix` for the outlined
  status-matrix variant; it creates one native table). A grid of text boxes and lines is not an editable table and
  fails object-model QA.
- A **component/tech-name chip** (ADK, Sandbox, Gateway, Model Armor) → `add_chip`.
  Hand-rolling a rounded rectangle with the default `word_wrap=True` and a tight width
  makes short caps tokens break mid-word ("AD / K"). `add_chip` turns wrapping off and
  sizes to the text (CJK counted double).
- A **panel with a label centered in it** (a "90% / 10%" badge, a boxed caption) →
  `add_label_panel`. `add_panel(...)` + a separate `textbox(...)` leaves the label
  TOP-anchored (floating at the panel's top edge) because that is the textbox default.
- An **on-site / illustrative photo** → `add_photo_slot` (see Photo policy below).

## Hard technical rules

1. **Blank layout only**: `prs.slide_layouts[6]`; set slide size 13.333"×7.5" before
   adding slides.
2. **Fonts**: use `Noto Sans TC` for all proportional text and `Consolas` for mono
   text. Before building, verify both fonts are installed; report a missing font rather
   than silently substituting another family. Set BOTH Latin and East Asian typefaces
   per run (primitives do this via the `a:ea` element).
3. **Text**: assign text via runs (never `text_frame.text =` on styled frames — it
   collapses formatting); zero the text-frame margins when aligning with shapes;
   left-align body text.
4. **Editability**: everything native except source screenshots/photos. Screenshots
   via `add_screenshot` (fit-inside, never stretched). Charts via python-pptx native
   charts, styled to the palette (orange primary series, hairline gridlines, value
   labels, no legend for a single series).
5. **Numbers on slides** come only from `outline.md` Source Facts. No placeholder
   numbers, ever.
6. **Overflow discipline & one-line title**: content-slide titles target **28pt
   (`T.S_TITLE`) and stay on ONE line**. Write titles concise enough to fit one line at
   28pt across the content width — `add_argument_title(..., fit=True)` (the default)
   auto-fits by stepping down the 2pt grid to `S_TITLE_MIN` (22pt) only if a title is too
   long, instead of wrapping; do not hand-shrink titles. Keep the title box full content
   width and leave ~10% slack. All other text uses the named ladder tokens; nothing goes
   below 12pt and every size is on the 2pt grid (`theme.snap_pt()` enforces this, so don't
   hand-tune to odd sizes). Cover/section hero display type (`S_COVER_TITLE_LIGHT`,
   `S_COVER_TITLE_DARK`, `S_TITLE_BIG`, `S_SECTION_NUM`) is exempt from the 28pt
   one-line rule.
7. **Integer coordinates only** (already enforced inside the primitives). Centering math
   like `node_h / 2` produces a Python float; python-pptx then writes a non-integer EMU
   (`y="3360420.0"`, `cx="0.0"`) that LibreOffice cannot parse, so the shape/connector
   collapses to the slide origin — the classic "arrows jumped to the top of the slide"
   bug. Every geometry primitive funnels its x/y/w/h through `_emu()`, so slide code may
   divide freely. If you ever create a shape/connector directly (not via a primitive),
   wrap each coordinate in `_emu(...)` yourself.
8. **Takeaway default-off**: call `add_takeaway_line()` only when the approved outline
   includes a Takeaway section. Otherwise allocate the full working height; never keep
   an empty 0.82" takeaway band.
9. **Native table object**: when the outline says `native table`, use
   `add_native_table()` with the structured Table Schema. Keep body text at 14pt or
   larger. If it does not fit, simplify without changing facts, then split across
   slides and repeat the header. Never substitute a text-box grid.

## Photo policy (reserve, don't auto-insert)

On-site and illustrative **photos are reserved as empty slots by default** — the user
decides later what (if anything) to paste. Add them with `add_photo_slot(slide, x, y,
w, h, caption=...)` and **do not pass an image path** unless the user explicitly points
to one: the primitive draws a dashed hairline placeholder holding the exact space, and
the user drops an image into that box in PowerPoint (or fills `img_path` and rebuilds).
This is separate from genuine **evidence screenshots** that prove a claim (Kanban, logs,
metrics, dashboards) — those still go through `add_screenshot` with a real path, because
the evidence itself is the argument.

## Render & preview pipeline

From macOS/Bash/WSL/Git Bash, use the bundled `scripts/render_pptx.sh`. From PowerShell
with Microsoft PowerPoint on Windows, use `scripts/render_ppt_com.ps1`. Render
`presentation/presentation.pptx` into `presentation/preview`, then execute the bundled
`scripts/create_contact_sheet.py` with arguments `presentation/preview` and
`presentation/preview-contact-sheet.png`.

For a localized edit, pass a slide selection as the fourth argument, for example
`render_pptx.sh deck.pptx preview 140 "3,7-9"`. Selected renders keep their original
`slide-NN.png` names; unaffected previews remain available for the contact sheet.

`render_pptx.sh` prefers native Microsoft PowerPoint: COM automation through
`render_ppt_com.ps1` on Windows, or AppleScript PDF export through
`render_ppt_mac.applescript` on macOS. Windows PowerPoint exports PNG directly; macOS
PowerPoint exports PDF and therefore requires Poppler's `pdftoppm`. If native PowerPoint
is unavailable or its automation fails, the wrapper falls back automatically to
LibreOffice headless → PDF → `pdftoppm`. Either way it emits
`slide-01.png`, `slide-02.png`, …. This selection is automatic — do not ask the user
which renderer to use. If NO renderer is available, report it and deliver the .pptx
anyway — do not fake previews.

## QA pass (bounded)

After a new full build, VIEW every slide image. For a localized edit, VIEW the affected
slides plus the full contact sheet. Fix implementation defects only: blank
slide, text outside the slide, severe overlap, missing source image, broken aspect
ratio, corrupted font rendering, unreadably tiny text, missing content, major
clipping. Re-render affected slides. A **reserved photo slot** (dashed placeholder box
from `add_photo_slot`) is intentional, not a defect — do not "fix" it by inventing an
image. Also confirm no connector/node has snapped to the top-left origin (the float-
coordinate symptom); if one has, it means a shape was created outside the primitives —
route its coordinates through `_emu()`. Maximum two fix passes — no subjective redesign
loop, no infinite regeneration. If a structural validator is available (e.g. a pptx
validate script), run it; otherwise confirm the file opens via a LibreOffice
conversion succeeding.

Visual QA cannot prove editability. Collect the one-based slide numbers whose outline
Visual Form is `native table`, then run:

```text
validate_pptx_structure.py presentation/presentation.pptx --require-table-slides "3,7-9"
```

Any listed slide without a native table object is a structural build failure. For an
unrelated localized edit, preserve a legacy text-box table; convert it only when the
user requests that table change or requests a full rebuild.
