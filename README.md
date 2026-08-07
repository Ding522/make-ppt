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

The workflow pauses after the outline and after a two-slide style sample. It requires
file read/write access and Python 3. Rendering uses Microsoft PowerPoint on Windows,
Microsoft PowerPoint plus Poppler on macOS, or LibreOffice plus Poppler as the portable
fallback.
