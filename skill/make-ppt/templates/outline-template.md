# outline-template.md — schema for presentation/outline.md

`outline.md` is the Presentation Intermediate Representation: a structured Slide DSL,
not a prose outline. The builder must be able to implement the entire deck from it.
Prose like "## Slide 5 — 介紹 DNS 問題" is insufficient. Omit fields that genuinely
don't apply to a slide — especially Takeaway and Table Schema — never fill them with
filler. The exact Markdown may evolve, but the semantic fields must be preserved.

---

# Presentation Specification

## Presentation Brief

- Working Title:
- User Request: <verbatim current user request>
- Audience: <inferred defensibly from request + sources; never invented against evidence>
- Presentation Goal:
- Presentation Context: <venue/occasion>
- Language: 繁體中文（保留自然英文技術詞）
- Expected Duration:
- User Requested Slide Count:
- Actual Planned Slide Count:
- Assumptions: <every material assumption made, explicitly>
- Source Inventory: <file → role → authority>
- Source Conflicts: <conflict, resolution, rationale — internal record>

## Narrative Strategy

<Concise English. Why this story order, e.g.: Start with the operational symptom
rather than the technical solution. Use the security constraint as the turning point.
Introduce the architecture only after the reader understands why a unified gateway
is required. End with implementation evidence and reusable lessons. Internal section.>

## Golden Circle Lens

- Why: <why this matters now; source-grounded stakes, friction, or consequence>
- How: <the mechanism, decision, or change that addresses the Why>
- What: <the concrete system, workflow, evidence, or next step>
- Natural Engineering Angle: <the specific judgment, trade-off, or constraint that keeps the story concrete>

## Core Narrative

<Short arrow flow, e.g.:
Adoption increased → project count exploded → internal access became the bottleneck
→ plaintext tokens blocked scale → unified authentication became necessary
→ Device Flow and audience-bound tokens provided the control layer>

## Narrative Review

<Required. Keep this compact. Review the order of slides within each section, not the
whole deck as one forced chain. Each slide should follow the previous slide's unresolved
question or premise, add a distinct step, and give the next slide a reason to follow.
Use only a short status when the sequence works. When it does not, record the affected
slide pair, the gap, and a recommended adjustment. Do not add visible transition copy or
a fixed previous/current/next field to every slide.>

- Status: <Pass / Needs review>
- Findings: <Omit when Status is Pass. Otherwise: Slides NN -> NN; Gap; Recommended Adjustment; Requires User Confirmation: Yes>

## Content Tone

technical · factual · concise · evidence-oriented · direct · implementation-grounded
· natural engineering language · slightly opinionated when supported by evidence
· **register: sharing with 同仁 — plain declarative, never a hosted session** (no
welcoming / thanking / transition lines, no crowd address 各位 / 大家, no session
framing 全場主軸 / 壓軸, no teasers that withhold a conclusion; see
`title-philosophy.md` → "Voice & register"). Avoid generic AI filler, marketing
phrases, mechanical three-part prose, and unsupported human stories or emotions.

## Deck Context Line

<the real mono context shown on dark cover/section slides — topic / team / date, e.g.
`技術分享 / 2026-07`. Must be true; never invented event or summit branding. The
builder sets this as `DECK_CONTEXT` in theme.py.>

## Design System

- Canvas: 16:9 (13.333" × 7.5")
- Background: #FAF8F4 warm off-white; dark slides #1A1714
- Primary Text: #1A1714 / body #4A443D
- Primary Accent: #D75F00 orange (emphasis device only)
- Success Semantic: #3E8E5A · Risk Semantic: #C13227 · Information Semantic: #3972DA
- Muted Semantic: #8A8177
- Eyebrow Style: `// NN    label`, mono, orange, upper-left
- Title Style: bold editorial argument, phrase-level orange emphasis
- Supporting Sentence Style: muted gray, key phrase bolded in ink
- Body Typography: <verified CJK font>
- Mono Typography: <verified mono font>
- Diagram Style: thin ink borders, semantic connectors (solid active / dashed inactive)
- Technical Panel Style: #1F1B17 dark panels, traffic lights, mono content
- Screenshot Style: aspect-preserved, thin hairline frame, annotated
- Line Style: hairline #DED8CE 1pt; accent rules #D75F00 2.25pt
- Takeaway Line Style: optional and default-off; orange rule + bold concrete implication
  + optional muted mono pointer only when the implication is distinct and necessary
- Spacing Principles: 0.62" page margins; header zone ends with hairline ~2.2–2.3";
  working area extends to the bottom margin unless a qualified takeaway is present
- Native Table Style: one editable PowerPoint table object; dark header, warm-white
  body, 1pt hairlines, 16pt header / 14pt body, no shadow

## Global Content Constraints

- Visible content in Traditional Chinese; keep natural technical English (token,
  scope, audience, Device Flow, PKCE, CI, PR, gateway, code review, schema…).
- No marketing slogans, decorative filler, or vague vision statements.
- Prefer concrete nouns, active verbs, evidence.
- Never invent source facts; never fabricate architecture complexity.
- Cards are not the default layout.

## Slide Architecture

<one line per slide — NN — Section — Role — informational purpose;
every slide's role unique, and adjacent slides in the same section must read as
consecutive narrative beats>

01 — Opening — …
02 — Agenda — …
03 — Context — …
…

---

## Slide NN — <title>

### Slide Role
<Opening / Agenda / Context / Tension / Root Cause / Argument / Architecture /
Mechanism / Workflow / Evidence / Comparison / Summary / Section / Closing>

### Purpose
<why this slide exists in one or two sentences>

### Argument
<the claim this slide makes>

### Key Message
<the one sentence a colleague should remember, in the slide's language>

### Title
<final visible title text>

### Title Emphasis
<exact phrase(s) to render in orange (or red for risk); never the whole title>

### Eyebrow
`// NN    <label>`

### Supporting Sentence
<final visible text; mark bolded phrases with **bold**>

### Visual Form
<from information-visualization.md catalog, e.g. Expectation → Reality → Root Cause + terminal evidence>

### Layout
<geometry: splits (e.g. 40/60), zones, what goes where, what dominates>

### Content
<the actual content, structured by zone/element — final wording, mono strings exact>

### Table Schema
<Include this entire section only when Visual Form is `native table`. Never describe
a semantic table only as prose.>
- Headers: <ordered column names>
- Rows: <one ordered cell list per record; exact visible wording>
- Column Width Ratios: <one positive ratio per column, e.g. 20 / 80>
- Column Alignment: <left / center / right per column; numeric columns right-aligned>
- Row Label Column: <column index/name or None; only this column is bolded>
- Merged Cells: <coordinates or None>
- Split Policy: <allowed split point(s); repeat headers on every continuation slide>

### Takeaway
<Optional and default-off. Omit this entire section unless the evidence supports a
concrete implication that is not already stated by the title or working area and that
changes interpretation or action. When omitted, reserve no takeaway space.>

### Visual Hierarchy
<numbered reading order, most dominant first>

### Visual Elements
<the native primitives/motifs required: eyebrow, mixed-run title, pills, panels,
terminal panel, arrows, step markers, native table, rules…>

### Source Assets
<screenshot/image files to place, or "None">

### Source Facts
- Source file:
- Page / slide / section:
- Supporting text: <verbatim source line each fact rests on>

### Style Constraints
<slide-specific constraints beyond the global design system>

### Editing Constraints
<what later localized edits must preserve, e.g. "preserve the 40/60 composition">
