# Relationship layouts

These are optional compositions within the fixed style, not a quota or a new theme.
Choose by relationships in the evidence, not by how much text a source contains.
Even a short source may support a timeline or matrix; a long source may only need a
plain list. Never add dates, statuses, categories or evidence merely to fill a layout.

## Selection and outline contract

| Evidence shape | Visual Form | Required content |
|---|---|---|
| Several workstreams with dated spans, overlap or resumption | `multitrack timeline` | Common axis/ticks, track labels, actual intervals, notes, semantic colors |
| Two categorical axes with comparable discrete states | `native table` with Table Variant `status-matrix` | Table Schema plus explicit state mapping/legend; optional row groups |
| Named categories or layers containing items and supporting examples | `layered list` | Group labels, optional descriptions, items and corresponding evidence |
| Repeated prose or numeric records | `native table` with Table Variant `standard` | Ordinary Table Schema; retain text and numeric values |

Record the selected form and one sentence explaining the relationship it exposes in
the outline's Layout field. Include the required content in structured Content (or
Table Schema). No need to document rejected alternatives. During narrative review,
check whether an existing dated, cross-category or hierarchical relationship was
flattened into generic bullets/cards. Change only when the relationship improves
understanding; do not force visual variety or require these forms in every deck.

## Multitrack timeline

Use one shared, proportional time axis. Put each project on a separate horizontal
track with its label, colored activity spans and a short muted evidence note.
Keep actual gaps and overlapping periods. Dashed connectors across gaps are optional:
only use them for source-supported continuity, and clarify that the gap is not active
work. With only dated events use a milestone timeline; without dates use a plain
sequence/list rather than inventing durations. Repeat axis/context if splitting.

## Status matrix

Preserve one native PowerPoint table for the complete grid. Use a near-black header,
light header text, near-white body, thin warm grid lines, a wider left label column,
and centered state symbols. Optional narrow category rails sit outside the grid and
align with body rows; category names belong in the row labels or an explicit legend.
Keep state symbols in the cells so table editing retains their meaning and alignment.

Define each symbol in the outline and a visible legend, for example orange `●` for
deep involvement and muted `○` for participation. These meanings are examples, not
universal defaults. Distinguish confirmed absence from unknown/unrecorded evidence;
never silently translate missing evidence into a negative state or faint dot.
Use color plus symbols, not color alone. Do not replace actual numbers, prose,
trade-offs or explanations with dots. Group rails are optional, not alternating row
decoration. Ordinary tables keep their existing standard style.

## Layered list

Use open horizontal groups, a narrow semantic color rail at the left, a bold group
heading and optional muted description. Place item names below on the left and their
supporting examples on the right. Use faint separators between groups; allocate height
by item count rather than equal-size cards. Two, three or more groups may be appropriate;
never invent a fixed three-layer taxonomy. If the content is a repeated column-header
dataset, use a native table instead. Long evidence may wrap only with sufficient row
height; shorten faithfully or split at a group boundary rather than shrink the font.

## Implementation and verification

Copy `assets/src-template/relationship_layouts.py` with the other starter modules.
It provides `add_multitrack_timeline`, `add_status_matrix`, and `add_layered_list`.
The functions document their data schemas; a runnable example is
`examples/relationship-layouts-sample.py`. The sample is a visual fixture, not factual
source material for future decks. Run it with an output PPTX path.

Keep existing type sizes and optional/default-off takeaway policy. Do not copy the
reference images' footer rule or summary onto every page. Render the selected forms
and check labels, wrapping, rails, legends and gaps. For status matrices also run the
native-table structural validator. Geometry checks do not replace visual inspection.
