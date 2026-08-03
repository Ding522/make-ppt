# information-visualization.md — visual form follows information shape

The planner's question for every slide is:
**"What visual structure explains this information fastest?"**
never "How can I turn these bullets into cards?"

## Selection procedure

1. Identify what the information actually IS: parallel categories? sequential stages?
   a causal chain? a contrast? a protocol interaction? a trend? evidence?
2. Pick the matching form from the catalog.
3. Decide what dominates the slide (title? diagram? screenshot? one number?).
4. Set density by slide role (see style-guide §6).

Three bullets in a source are NOT automatically three cards. Determine whether they
are three parallel categories (columns/matrix), three sequential stages (process map),
three risks (numbered risk list with severity badges), three mechanisms (one slide
each, or a labeled diagram), or three evidence sources (evidence layout).

## Catalog

**Narrative / contrast:** timeline (dated milestones above/below an axis, colored by
phase); before/after (half-dark half-light split); expectation → reality → root cause
(pills + downward arrow + dark root-cause panel); tension contrast (one giant figure,
e.g. `5x → 2xx → 1xxx`); comparison matrix; status matrix; A/B panels with semantic
headers; roadmap; decision tree.

**Process / flow:** horizontal or vertical process map with numbered stages and
directional connectors; workflow pipeline with role ownership (human stages in orange
pills, AI stages plain, AI-loop stages framed as an 自動迭代迴圈); role handoff
diagram; Kanban board (columns with count badges, cards with mono IDs, AI/human
ownership tags, per-column automation footer); state transition.

**Architecture / mechanism:** architecture diagram with labeled zone boundaries
(mono uppercase zone labels), large system nodes, central dark gateway block;
gateway topology; system boundary diagram; sequence diagram / protocol flow
(actor boxes, dashed lifelines, numbered circles, request/response arrows with mono
annotations); request/response flow; risk model.

**Evidence / data:** metric trend (native bar/column chart, orange primary series,
value labels, giant `66% → 97%` callout beside it); KPI emphasis (huge mono figure +
muted caption); screenshot + analysis (screenshot dominates, annotations state what it
proves); terminal panel; code/config panel; simple native tables.

**Native table boundary:** if content has column headers, repeated records, and values
that align across rows, it is a table and must be one native PowerPoint table object.
A matrix diagram is different: it may use free-positioned shapes only when cells need
connectors, overlapping elements, or materially different internal visual structures.
Do not use a matrix as an excuse to hand-build an ordinary table from text boxes.

## Rules

- Charts and semantic tables are native PowerPoint objects, not images or text-box grids.
- If a native table does not fit at 14pt body text, simplify its wording without
  changing meaning, then split it across slides and repeat the header.
- Screenshots are evidence, not decoration — always pair with what they prove.
- Architecture diagrams show the actual architecture; never add services for visual
  complexity. Process diagrams show actual processes; never dress bullets as a
  workflow.
- Cards are one implementation tool among many, never the default architecture, and
  never appear as the same 3–4-card grid on consecutive slides.
