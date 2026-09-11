# Cost-Control Workflow

Use this policy to protect presentation quality while avoiding expensive narrative
rebuilds. Cost modes change how much direction exploration happens before planning;
they never weaken source grounding, outline approval, style approval, or QA.

## Resolve the mode

- `standard` is the default.
- Use `explore` only when the user explicitly asks for explore mode, alternatives,
  multiple narrative directions, or equivalent up-front exploration.
- Use `strict` only when the user explicitly asks for strict mode, saving cost,
  speed, minimal exploration, or equivalent cost-control intent.
- A clear prompt never activates `strict`. It only lets `standard` skip the
  Narrative Fork checkpoint.
- If mode signals conflict, ask one concise question and stop.

All modes retain both mandatory checkpoints: approval of the current `outline.md`
and approval of the style sample.

## Assess direction clarity

Treat the direction as clear when at least two of these three fields are explicit:

1. Purpose: what the deck should accomplish.
2. Audience: who will read or hear it.
3. Narrative angle: the thesis or lens that should organize the evidence.

Record the resolved mode and a one-line Direction Lock in `outline.md`. Record a
missing third field as an assumption when needed.

Apply the modes as follows:

- `standard`, clear direction: skip Narrative Fork and proceed to one outline.
- `standard`, unclear direction: create a Narrative Fork and pause.
- `explore`: create a Narrative Fork and pause, even when the initial direction is
  reasonably clear, because the user explicitly requested alternatives.
- `strict`, clear direction: skip Narrative Fork and proceed to one outline.
- `strict`, unclear direction: ask one focused question at a time until at least two
  fields are explicit. Do not create alternatives unless the user asks for them.

## Narrative Fork checkpoint

Write `presentation/narrative-forks.md` using
`templates/narrative-forks-template.md`. Produce exactly three compact narrative
axes, grounded in the evidence pack and totaling no more than roughly one page.

For each axis include only:

- thesis;
- best-fit audience and use case;
- high-level flow;
- strongest evidence basis;
- trade-off or risk.

Do not write three outlines, slide-by-slide specifications, PPTX files, or generation
code. Present a compact comparison, then end the turn. Continue only after the user
selects one axis, combines named parts, or supplies a precise replacement direction.
Pass the chosen result to the planner as the Direction Lock.

## Outline approval validity

The current `outline.md` always requires explicit user approval before any builder
work. No mode may skip this checkpoint.

Invalidate prior approval when the outline changes in any of these ways:

- narrative thesis or axis changes;
- a major section is added, removed, or reordered;
- slides are added or removed.

After an invalidating change, rewrite the outline, present the complete outline
checkpoint again, and wait for a new approval. Typo fixes and wording changes that do
not affect meaning, order, or slide count do not invalidate approval.

## Edit impact classification

Assign one primary impact classification to every request to modify an existing
generated deck before editing:

- `small-localized`: explicit element-level change with no narrative, shared style,
  or slide-order impact. Apply the Localized Edit Principle directly.
- `single-slide-structural`: changes one slide's argument, content structure, or
  layout.
- `cross-slide`: changes multiple slides or a relationship between slides.
- `narrative-restructure`: changes the thesis, major section order, or deck-level
  logic.

Then evaluate `full-rebuild-candidate` as an additional flag, not a replacement for
the primary classification. A request may be both `narrative-restructure` and
`full-rebuild-candidate`; apply every gate that matches.

For every primary classification except `small-localized`, or whenever the
`full-rebuild-candidate` flag is present, write
`presentation/edit-impact.md` using `templates/edit-impact-template.md` before
touching maintained generation source. An impact note is not itself a hard stop unless
the change invalidates outline approval or triggers full rebuild confirmation.

For `narrative-restructure`, return to text planning before builder work. If the user
gave a precise replacement direction, rewrite only `outline.md`. Otherwise return to
the Narrative Fork checkpoint. Any resulting outline change must pass the outline
checkpoint again.

## Full rebuild confirmation

Require explicit full rebuild confirmation when any condition is true:

- affected slides exceed 30% of the deck;
- shared theme tokens or shared primitives change;
- the narrative axis changes;
- major sections are reordered.

Write `edit-impact.md`, explain the trigger and recommended rollback stage, then end
the turn. Require the user to reply with the explicit phrase `確認 full rebuild`
before performing the rebuild. Full rebuild confirmation never replaces a required
Narrative Fork or renewed outline approval.

When `narrative-restructure` and `full-rebuild-candidate` both apply, enforce both
gates. Obtain `確認 full rebuild` first so rejected rebuilds do not spend additional
planning cost; then complete the required Narrative Fork or precise outline rewrite
and renewed outline approval. Do not invoke the builder until every applicable gate
has passed.
