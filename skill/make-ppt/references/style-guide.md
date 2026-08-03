# Style Guide — Fixed Visual Grammar

Extracted from the primary visual reference `AI_Agentic_Coding_導入實戰.pdf`
(28 pages, actual rendered pages inspected, colors sampled from pixels). This is the
design system for every deck this skill produces. The target language is
**Internal Technical Share / Engineering Editorial** — an engineer writing up a real
implementation, a real problem, and a real decision **for teammates (同仁)**. It is NOT
generic corporate blue, consulting style, Microsoft/Google marketing, or Apple
minimalism. Decks should feel manually composed: bold, sometimes information-dense,
opinionated when evidence supports it.

**Register: a share with colleagues, not a hosted session.** The deck is a written
artifact colleagues read and discuss — closer to good engineering notes than to a
keynote script. It never addresses a crowd, never plays host, never builds suspense.
See "Voice & register" in `title-philosophy.md` for the wording rules; they are as
binding as the visual rules below.

## 1. Canvas & page scaffold

- 16:9 widescreen (13.333" × 7.5").
- Content slides: warm off-white background `#FAF8F4`; ~0.62" left/right margins.
- Standard content-slide skeleton, top to bottom:
  1. **Eyebrow** (upper-left, mono, orange): `// NN    section · context`
  2. **Argument title** (large, heavy, near-black, phrase-level orange emphasis)
  3. **Supporting sentence** (muted gray, key phrases bolded in dark ink)
  4. thin warm hairline `#DED8CE` separating header zone from the working area
  5. **Working area** (the diagram / evidence / comparison — the dominant element)
  6. optional, **default-off Takeaway line**: thin orange rule + concrete implication;
     optional right-aligned muted mono cross-reference (`→ 解法詳見 P12`)
- Do not reserve takeaway space when it is omitted. Let the working area extend to the
  normal bottom margin; an empty bottom band is not part of the page scaffold.
- Cover / section / closing slides invert to near-black `#1A1714` background with a
  white top hairline, mono header row (the deck's own **real context** — topic, team,
  or date, e.g. `技術分享 / 2026-07` — plus a page or badge), and huge display
  typography. The context line states what this deck actually is; **never invent event
  branding** (no fabricated summit/conference names, no `20XX XXX SUMMIT / TAIWAN`
  chrome). Pass it via `add_section_slide(..., context=…)`.

## 2. Palette (sampled values — use exactly these)

| Token | Hex | Semantics |
|---|---|---|
| BG | `#FAF8F4` | warm off-white page background |
| INK | `#1A1714` | primary text; also dark-slide & dark-panel background |
| INK_SOFT | `#4A443D` | body text on light bg |
| MUTED | `#8A8177` | supporting sentences, inactive labels, captions |
| HAIRLINE | `#DED8CE` | thin dividers, light panel borders |
| ORANGE | `#D75F00` | **the** emphasis color |
| GREEN | `#3E8E5A` | positive / success / accepted / completed / human checkpoint |
| RED | `#C13227` | risk / rejection / vulnerability / security concern / failure |
| BLUE | `#3972DA` | information / technical category / tool semantics |
| DARK_PANEL | `#1F1B17` | terminal & root-cause panels |

**Color is semantics, never decoration.** Never alternate colors for variety. Never
color a whole slide orange — orange is an emphasis device: the decisive phrase in a
title, an important number, the active flow, a key arrow, a mechanism name, an
emphasized conclusion, an accent rule. The reference uses orange in perhaps 5–10% of
any slide's area; the rest is ink, muted gray, and whitespace.

## 3. Typography

- **Fixed 2pt-stepped type ladder** (defined in `theme.py`; do not invent sizes):
  content-slide **title 28pt, kept to ONE line** → 20pt takeaway → 16pt supporting
  sentence / sub-heading → 14pt body → 12pt eyebrow, labels & mono metadata. Two hard
  rules: **no text below 12pt**, and **every size on the 2pt grid** (all even).
  `theme.snap_pt()` enforces both at run time. **Titles stay on one line**: write them
  concise enough to fit one line at 28pt across the content width; `add_argument_title`
  auto-fits by stepping down the 2pt grid to `S_TITLE_MIN` (22pt) only when a title is
  genuinely too long, rather than wrapping. Cover / section-divider **display hero**
  titles are a separate register and keep their large sizes (`S_TITLE_BIG` 40pt,
  `S_SECTION_NUM` 150pt) — the 28pt one-line rule applies to content slides, not to the
  hero display type.
- CJK family: verify availability before use (`theme.pick_font()`, cross-platform).
  Preference order:
  Noto Sans TC → Noto Sans CJK TC → Microsoft JhengHei → PingFang TC. Never reference
  a nonexistent font and rely on fallback. Heavy weights must exist (titles are bold).
- Mono family (verify likewise): JetBrains Mono → Cascadia Code → IBM Plex Mono →
  Noto Sans Mono → DejaVu Sans Mono. Mono is used for: eyebrows, commands, code,
  file paths, RFC identifiers, protocol names, config keys, technical metadata,
  numbering (`// 16`, `01`, page counters), section header rows on dark slides.
- Body text left-aligned. No decorative fonts.

## 4. The technical eyebrow

Nearly every content slide opens with `// NN    label` in the upper-left: orange (or
blue on a few information-category slides), mono, ~12pt, number bold. The label is
short metadata: section (`流程統一 · CI`), mechanism (`機制一 · RFC 8628`), category
(`MCP 推廣的阻力`). Visually secondary; one reusable primitive, identical placement on
every slide — never redesigned per slide.

## 5. Titles & supporting sentences

See `title-philosophy.md` for the editorial rules. Visually: titles are near-black,
bold, tight line spacing (~1.05–1.1), with ONLY the decisive phrase in orange (a rare
risk-emphasis title uses red, e.g. 資安審查). Long dash `——` joins tension halves.
The supporting sentence sits directly under the title in `#8A8177`, with the pivotal
technical phrase bolded in dark ink. It clarifies scope/mechanism/context; it never
repeats the title verbatim.

## 6. Density follows slide role (deliberate variation)

- **Tension / transition**: nearly empty — one giant claim or figure
  (`5x → 2xx → 1xxx 個專案`), enormous whitespace, takeaway question. Never fill the
  space with cards.
- **Argument**: large claim title + short support + one dominant comparison.
- **Workflow**: medium-high density; strict horizontal/vertical structure, numbered
  stages, directional connectors, explicit role ownership; human vs AI stages
  visually distinguished (orange pill = 人為把關, plain = AI 主導; the reference
  boxes the AI-loop stages inside a thin-bordered "自動迭代迴圈" frame).
- **Architecture**: diagram dominates; large blocks, labeled boundaries (mono
  uppercase zone labels like `C-DOMAIN · 開發者端`), connectors with meaning; the
  central gateway is a dark panel with orange mono label.
- **Mechanism / protocol**: swimlane sequence diagram; actor boxes across the top
  (key actor dark/orange), dashed vertical lifelines, numbered circle markers,
  request/response arrows with mono annotations, RFC names in the eyebrow. Technical
  detail welcome — never degrade into marketing cards.
- **Evidence / operational**: screenshot / Kanban / logs / metrics dominate;
  annotations state what the evidence proves.
- **Comparison / before-after**: immediate A/B contrast. The reference's strongest
  form: half-dark half-light split slide (一年前 on dark, 今天 on light), or two
  panels with colored semantic headers, or strikethrough on the rejected idea
  (`MCP 已死` struck through in title).

## 7. Technical UI motifs (use only when content supports them)

Dark terminal panels (mac traffic lights, muted mono path in header, `RISK` badge,
red-highlighted secrets, gray `#` comments); code/config panels; protocol labels;
status pills (期待/現實/主導/專責/最致命); numbered circles; thin solid arrows for
active flow, dashed for inactive/background; bordered system nodes (thin ink border,
white fill); large dark gateway blocks; `✓ 接受` green / `✗ 拒絕` red states; inline
mono metadata (`aud = mcp://gitea`). All implemented as editable PowerPoint objects.
No terminal panel in an HR deck just because the style has one — form follows content.

## 8. Takeaway line

**Default-off.** Use only when the slide has a concrete, source-grounded implication
that is not already carried by its title or working area and that changes how a
colleague should interpret or act on the evidence. Do not reserve takeaway space when
the condition is not met.

When qualified, place a thin orange rule (~2.25pt) across the content width,
then one concrete, source-grounded implication in bold `S_TAKEAWAY`, decisive phrase in
orange; optionally a right-aligned muted mono **cross-reference** to where a topic is
covered in detail (`→ Govern 詳見 P8`). It summarizes what the evidence implies and
links to the larger story. It is never a vision statement, slogan, or motivational
filler — and never a **tease** that withholds the answer to hold attention
(`→ 解法看後半段`, `→ 精彩的在後面`, `→ 敬請期待`): a colleague reading the deck can
just turn the page, so point plainly at the page (`詳見 P12`) or omit the pointer.
Cover, agenda, section, workflow, architecture, and ordinary table slides normally
omit it. A repeated title, summary sentence, or decorative closing line does not
qualify as a takeaway.

## 9. Native tables

Use one editable native PowerPoint table whenever content has column headers,
repeated records, and cross-row alignment. Never recreate that grid with independent
text boxes and lines. Default style: dark header with white 16pt text; warm-white body
with 14pt text; 1pt hairline borders; sufficient cell padding; vertically centered
content; left-aligned text and right-aligned numeric columns. Bold the first column
only when it is explicitly the row-label column. Use orange only for a real difference,
risk, or decision value. No rounded container and no shadow.

If content does not fit, first simplify wording without changing technical meaning,
then split the table across consecutive slides and repeat the header. Never shrink
body text below 14pt or fall back to a text-box grid.

## 10. Anti-patterns (hard bans)

- Marketing language: 賦能未來 / 引領創新 / 開啟新篇章 / 打造全新體驗 / 全面升級 /
  邁向卓越 / 智慧轉型新紀元 / 重新定義未來 / 創造無限可能 / 驅動企業成長 /
  釋放無限潛能 / 開創嶄新格局 — banned unless quoted from official branding.
- **Host / emcee language** (this deck is shared with 同仁, not hosted on a stage):
  歡迎大家 / 今天很榮幸 / 讓我們一起 / 接下來讓我們 / 進入下一個環節 / 敬請期待 /
  精彩可期 / 壓軸 / 開場 / 全場主軸 / 本場重點 / 大家好 / 謝謝大家的聆聽 /
  以上就是我的分享 — and any second-person address to a crowd (各位、大家、聽眾).
  Also banned: fabricated event branding on dark slides (invented summit/conference
  names), and teaser pointers that withhold an answer to hold attention.
- Generic AI slide patterns: 3–4 identical cards everywhere; icon+heading+paragraph
  repeated; process arrows on every slide; oversized title + meaningless whitespace as
  a default; gradients; glassmorphism; drop shadows; stock illustrations; hero images;
  glowing AI brains; floating 3D shapes; robots; network backgrounds; giant quote marks;
  fake dashboard widgets.
- **Drop shadows on anything** — shape, line, card, panel, pill, node, table, or
  picture. The grammar is **flat**: surfaces are separated by hairline borders
  (`#DED8CE`), never shadows. `primitives.py` strips shadows on every element via
  `no_shadow()`; any slide code that creates a shape directly must call
  `primitives.no_shadow(shape)`.
- Fake evidence: invented numbers, invented architecture services, bullet lists
  dressed up as workflows.
- **Fake tables:** column headers and repeated rows assembled from text boxes,
  rectangles, and lines instead of a native table object.
- Vary composition across the deck while preserving this grammar. Consistency ≠ the
  same layout on every slide.
