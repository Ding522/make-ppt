# make-ppt

`make-ppt` 是一個可攜式 Agent Skill，可將報告、專案紀錄、技術分享、POC、弱點改善資料與其他專案素材，整理成有來源依據、可編輯的 PowerPoint 簡報。

它不只輸出 `.pptx`，也會保留大綱、證據紀錄、可維護的產生程式、逐頁預覽與 contact sheet，讓簡報能被檢查、修改與持續維護。

> [!IMPORTANT]
> [`skill/make-ppt`](skill/make-ppt) 是本專案唯一的 canonical skill package。請修改這裡的來源檔，不要把使用者目錄中的安裝副本、暫存備份或產出資料夾複製回 repository。

## 主要能力

- 根據專案素材建立可追溯的 evidence pack，避免無來源的結論與數字。
- 先規劃敘事與 `outline.md`，經使用者確認後才開始製作投影片。
- 先產生 1–2 頁 style sample，確認視覺方向後再完成全份簡報。
- 輸出物件層級可編輯的 PowerPoint，而不是整頁圖片。
- 支援 `editorial-light` 與 `report-dark` 兩種受控封面變體。
- 提供 timeline、status matrix 等關係型版面元件。
- 修改既有簡報時先判斷影響範圍，小修改維持局部更新。
- 檢查台灣繁體中文用語，不自動取代需要人工判斷的詞彙。
- 可安裝到 Codex、Claude Code、Kiro、GitHub Copilot 與 Google Antigravity。

## 快速開始

需求：Python 3.9 或更新版本。

先預覽安裝位置，再安裝到你使用的 client：

```powershell
git clone https://github.com/Ding522/make-ppt.git
cd make-ppt

python .\install.py --client codex --scope user --dry-run
python .\install.py --client codex --scope user
python .\doctor.py --client codex --scope user
```

把 `codex` 改為 `claude`、`kiro`、`copilot` 或 `antigravity`，即可安裝到其他 client。使用 `--client all` 可一次處理所有已註冊的 client。

接著在含有來源資料的專案目錄中提出需求：

```text
使用 make-ppt，把這個資料夾的素材整理成 10 頁、面向工程主管的台灣繁體中文技術簡報。主軸聚焦交付成果，最後提出下一階段的資源需求。
```

支援 skills 指令的 client 也可能提供 `/make-ppt` 或 `$make-ppt`；使用自然語言呼叫不依賴特定指令格式。

## 工作流程

```text
來源素材
  -> evidence pack
  -> 敘事方向（必要時提供 Narrative Fork）
  -> outline.md
  -> 使用者確認大綱
  -> 1–2 頁 style sample
  -> 使用者確認風格
  -> 完整 PPTX、逐頁預覽與 contact sheet
```

`presentation/outline.md` 是簡報的 source of truth。Planner 負責證據、敘事與大綱；Builder 只依照已核准的大綱實作，不自行改變論點、證據或順序。即使同一個 agent 依序執行兩個角色，這個界線仍然成立。

預設產出結構：

```text
presentation/
├── narrative-forks.md          # 方向不明或 explore 模式時產生
├── outline.md                  # 已規劃的簡報規格與內容來源
├── edit-impact.md              # 非小型既有簡報修改時產生
├── evidence/
│   ├── manifest.md
│   ├── manifest.json
│   └── sources/*.md
├── presentation.pptx           # 可編輯簡報
├── src/                        # 可維護的產生程式
├── preview/slide-01.png ...    # 逐頁預覽
└── preview-contact-sheet.png
```

原始來源素材不會被覆寫。

## 敘事與成本模式

| 模式 | 適用情境 | 行為 |
|---|---|---|
| `standard` | 預設 | 方向清楚時直接規劃；不清楚時先提供三個精簡的 Narrative Fork。 |
| `explore` | 想比較不同說法 | 即使需求相對清楚，仍先比較三種敘事軸線；不會產生三份完整簡報。 |
| `strict` | 明確要求節省成本或快速完成 | 不主動展開替代方向；資訊不足時提出聚焦問題。 |

所有模式都會停在大綱與 style sample 兩個確認點。敘事方向、主要章節的新增、刪除或重排，以及投影片的新增或刪除，都會讓先前的核准失效並觸發新的大綱確認；純文案修正與不影響結構的視覺微調則不會。

Policy contract（穩定措辭）：

```text
Narrative changes, major-section additions/removals/reordering, or slide
additions/removals invalidate prior approval.
```

更完整的規則請見 [`cost-control-workflow.md`](skill/make-ppt/references/cost-control-workflow.md)。

## 安裝與更新

### 安裝位置

| Client | User scope | Project scope |
|---|---|---|
| Codex | `~/.agents/skills/make-ppt` | `.agents/skills/make-ppt` |
| Claude Code | `~/.claude/skills/make-ppt` | `.claude/skills/make-ppt` |
| Kiro | `~/.kiro/skills/make-ppt` | `.kiro/skills/make-ppt` |
| GitHub Copilot | `~/.copilot/skills/make-ppt` | `.github/skills/make-ppt` |
| Google Antigravity | `~/.gemini/config/skills/make-ppt` | `.agents/skills/make-ppt` |

安裝程式也會從 canonical role references 產生各 client 使用的 Planner 與 Builder agent 檔案。Client 路徑、格式、metadata overlay 與 legacy 位置的唯一登錄來源是 [`integrations/clients.json`](integrations/clients.json)。

### 常用指令

```powershell
# 安裝所有 client
python .\install.py --client all --scope user

# 安裝到指定專案
python .\install.py --client all --scope project --project-dir C:\path\to\project

# 更新已存在的安裝
python .\install.py --client all --scope user --force

# 同時安裝 skill 內附的 Python dependencies
python .\install.py --client all --scope user --install-python-deps

# 檢查環境與安裝狀態
python .\doctor.py --client all --scope user
```

安裝 Python dependencies 是明確選項，不會在一般安裝時自動執行。若要搬移舊版安裝，先用 `--dry-run --migrate-legacy` 預覽，再使用 `--force --migrate-legacy`；legacy installation 不會被靜默刪除。

## 渲染需求

Skill 需要檔案讀寫權限及 Python 3.9+。Python 套件定義於 [`requirements.txt`](skill/make-ppt/requirements.txt)。

- Windows：優先使用 Microsoft PowerPoint。
- macOS：使用 Microsoft PowerPoint，並以 Poppler 產生預覽。
- 可攜式 fallback：LibreOffice + Poppler。

執行 doctor 可確認 Python packages、renderer 與各 client 的安裝狀態：

```powershell
python .\doctor.py --client all --scope user
python .\doctor.py --client antigravity --scope project --project-dir C:\path\to\project
```

## 專案結構

```text
make-ppt/
├── skill/make-ppt/          # canonical skill package；主要修改位置
│   ├── SKILL.md             # orchestration contract
│   ├── assets/src-template/ # PPTX theme、primitives 與版面元件
│   ├── references/          # Planner、Builder、風格與品質規則
│   ├── scripts/             # evidence、render、lint 與 validation 工具
│   └── templates/           # outline、Narrative Fork、edit impact 範本
├── integrations/            # client registry 與 agent metadata
├── tests/                   # 安裝、政策、版面、語言與渲染測試
├── install.py               # 跨 client 安裝程式
├── doctor.py                # 環境與安裝診斷
└── client_registry.py       # client registry loader
```

### Source of truth 規則

1. Skill 本體只修改 `skill/make-ppt/`。
2. Client 差異只修改 `integrations/` 與 `integrations/clients.json`。
3. 不直接修改 `~/.agents/skills`、`~/.codex/agents` 等安裝結果；修改來源後重新執行 `install.py --force`。
4. 不把 installed skill backup、預覽圖片、測試輸出或完整 `presentation/` 產物當成 repository 來源。
5. 提交前先執行測試並檢查 `git status`，確認沒有複製產物混入。

## 開發與驗證

執行完整測試：

```powershell
python -m unittest discover -s tests -v
```

預覽所有 client 的安裝結果，不寫入檔案：

```powershell
python .\install.py --client all --scope user --dry-run
```

檢查大綱或簡報中的台灣用語：

```powershell
python .\skill\make-ppt\scripts\lint_zh_tw.py presentation\outline.md --outline-visible-only
python .\skill\make-ppt\scripts\lint_zh_tw.py presentation\presentation.pptx
```

高信心項目會使檢查失敗；例如「配置」這類需視上下文判斷的詞，只會列出供人工確認，不會被自動取代。

## 進一步閱讀

- [Skill orchestration contract](skill/make-ppt/SKILL.md)
- [Planner role](skill/make-ppt/references/ppt-planner-role.md)
- [Builder role](skill/make-ppt/references/ppt-builder-role.md)
- [Style guide](skill/make-ppt/references/style-guide.md)
- [Information visualization](skill/make-ppt/references/information-visualization.md)
- [Relationship layouts](skill/make-ppt/references/relationship-layouts.md)
- [PPTX generation rules](skill/make-ppt/references/pptx-generation-rules.md)
