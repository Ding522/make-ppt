# make-ppt

`make-ppt` is one portable Agent Skill for producing source-grounded, editable
PowerPoint decks in a fixed engineering editorial style. The canonical package is
[`skill/make-ppt`](skill/make-ppt); client-specific integrations are generated from it.

## Install

Install for every supported client in the current user account:

```powershell
python .\install.py --client all --scope user
```

Install for one client:

```powershell
python .\install.py --client claude --scope user
python .\install.py --client kiro --scope user
python .\install.py --client codex --scope user
python .\install.py --client copilot --scope user
```

Install into a project instead of the user profile:

```powershell
python .\install.py --client all --scope project --project-dir C:\path\to\project
```

Reinstall an updated version with `--force`. Preview targets first with `--dry-run`.
Installation also generates or refreshes the planner and builder agents in each
client's native agent directory. These files are generated from the canonical role
references plus client-specific metadata; edit the source files in this repository
rather than the installed copies.

| Client | User scope | Project scope |
|---|---|---|
| Codex | `~/.agents/skills/make-ppt` | `.agents/skills/make-ppt` |
| Claude Code | `~/.claude/skills/make-ppt` | `.claude/skills/make-ppt` |
| Kiro | `~/.kiro/skills/make-ppt` | `.kiro/skills/make-ppt` |
| GitHub Copilot | `~/.copilot/skills/make-ppt` | `.github/skills/make-ppt` |

Agent files use these native locations: Codex `~/.codex/agents` / `.codex/agents`,
Claude `~/.claude/agents` / `.claude/agents`, Kiro `~/.kiro/agents` / `.kiro/agents`,
and GitHub Copilot `~/.copilot/agents` / `.github/agents`.

Other Agent Skills compatible clients can import the canonical
`skill/make-ppt` folder directly or copy it into their documented skills directory.
The core skill remains client-neutral; integrations under `integrations/` adapt it to
native client features such as Codex UI metadata and Claude Code subagents.

## Use

Use a client-neutral prompt:

```text
Use the make-ppt skill to turn the materials in this folder into a 10-slide
Traditional Chinese technical presentation.
```

Clients that expose skills as slash commands may also support `/make-ppt`; Codex may
expose it as `$make-ppt`. The natural-language form works without relying on either
client convention.

## Cost-control modes

`standard` is the default. It skips narrative alternatives when the prompt clearly
states at least two of the purpose, audience, and narrative angle. Otherwise it first
writes three compact alternatives to `presentation/narrative-forks.md` and waits for
the user to select or combine a direction.

```text
Use make-ppt to prepare a deck for engineering managers. Focus on delivery outcomes
and end by requesting resources for the next phase.
```

Use `explore` when comparing narrative directions is worth the small up-front cost.
It creates the same three-axis Narrative Fork even when the initial prompt is fairly
clear; it never creates three full decks or three full outlines.

```text
Use make-ppt in explore mode. Show me different narrative directions before outlining.
```

Use `strict` only by stating strict or equivalent cost intent such as save cost, move
quickly, or minimize exploration. A clear prompt does not activate strict by itself.
When strict direction is unclear, the skill asks focused questions instead of
proactively generating alternatives.

```text
Use make-ppt in strict mode. Keep exploration minimal and optimize for generation cost.
```

Every mode always pauses for approval of the current `outline.md` and the two-slide
style sample. Narrative changes, major-section additions/removals/reordering, or slide
additions/removals invalidate the prior approval and require a fresh outline checkpoint.

For existing decks, small edits stay localized. Larger edits create
`presentation/edit-impact.md` first. Changes affecting more than 30% of slides, shared
theme/primitives, the narrative axis, or major-section order require the explicit
reply `確認 full rebuild` before rebuilding.

The skill requires file read/write access and Python 3. Rendering uses Microsoft
PowerPoint on Windows, Microsoft PowerPoint plus Poppler on macOS, or LibreOffice plus
Poppler as the portable fallback.
