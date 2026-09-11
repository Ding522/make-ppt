# outline-example.md — realistic example (excerpt of a 10-slide deck)

This example shows the required fidelity. The global section is complete; three
per-slide specifications are shown at full fidelity (the opening cover, a
tension/root-cause slide, and a mechanism slide). Real outlines specify every slide at
this level.

---

# Presentation Specification

## Presentation Brief

- Working Title: 內部 MCP 統一認證 — 從 Token 明碼到 Device Flow
- User Request: 幫我根據這些素材製作一份內部技術分享簡報，大約 10 頁，重點放在 MCP 認證治理
- Cost Mode: standard
- Direction Lock: 對內部工程團隊說明 MCP 認證治理的必要性，並以統一認證閘道作為採用主張
- Audience: 公司內部後端 / DevOps 工程師（依 user request 明示「內部技術分享」與素材中的內部系統名稱推定）
- Presentation Goal: 說服工程團隊採用統一認證閘道接入內部 MCP
- Presentation Context: 部門技術分享，約 25 分鐘
- Language: 台灣繁體中文（zh-TW；保留自然英文技術詞）
- Expected Duration: 25 min
- User Requested Slide Count: 大約 10
- Actual Planned Slide Count: 10
- Assumptions: 聽眾已熟悉 OAuth 基本概念（素材含 RFC 引用未附入門說明）
- Source Inventory: `mcp-auth-design.md` → 主要證據（架構、機制）· 權威最高；
  `settings-screenshot.png` → 佐證截圖（token 明碼）；`rollout-notes.docx` → 時程輔助
- Source Conflicts: rollout-notes 稱試點 3 團隊、design doc 稱 4；採 design doc（較新，
  含名單），衝突記錄於此，不上 slide

## Narrative Strategy

Start from the adoption symptom (everyone wants MCP, nobody ships it), reveal the
plaintext-token root cause with concrete client-side evidence, then introduce the
gateway only once the reader sees why it is necessary. Close with the mechanism
(Device Flow + PKCE) and the operational implication.

## Core Narrative

Demand for MCP grew → integration stalled → root cause: plaintext tokens on clients
→ unified auth gateway → Device Flow + PKCE removes keys from disk → adoption unblocked

## Narrative Review

- Status: Needs review
- Findings: Slides 06 -> 07; the architecture slide introduces the gateway, but the protocol slide can read like a new topic; Recommended Adjustment: keep the order and make Slide 07's title or supporting sentence explicitly name the gateway handoff; Requires User Confirmation: Yes

## Content Tone

technical · factual · concise · evidence-oriented · direct · implementation-grounded
· register: sharing with 同仁 — plain declarative, never a hosted session

## Deck Context Line

內部技術分享 / MCP 認證治理

## Cover Variant

`editorial-light` — technical implementation share; subtitle and presenter/date footer
are useful, but Footer Highlight is omitted.

## Design System

（同 outline-template.md 預設；CJK font: Noto Sans TC（已驗證）；Mono: Consolas（已驗證））

## Global Content Constraints

（同 template 全域規範）

## Slide Architecture

01 — Opening — 建立主題：MCP 認證是規模化的門檻
02 — Agenda — 三段結構：現象 → 根因 → 機制
03 — Context — MCP 需求成長的內部背景
04 — Tension/Root Cause — 想接全公司 MCP，卡在 Token 明碼
05 — Risk — 被 AI 放大的三大資安風險
06 — Architecture — 統一認證閘道：所有工具走同一個門
07 — Mechanism — Device Flow + PKCE 完整序列
08 — Governance — audience-bound token 限縮爆炸半徑
09 — Evidence — 試點團隊接入後的實際流程截圖
10 — Summary — 可複用的三條實作原則

---

## Slide 01 — MCP 認證是規模化的門檻

### Slide Role
Opening

### Purpose
Establish the deck as an internal implementation share about the authentication control
required before MCP can scale across teams.

### Argument
MCP 能不能擴大採用，關鍵不只在工具能力，而在認證能否安全地集中治理。

### Key Message
把 Token 留在各 Client 端，MCP 就無法安全地規模化。

### Title
MCP 認證是\n規模化的門檻

### Title Emphasis
None — the short orange rule carries cover emphasis.

### Eyebrow
`MCP AUTH · ADOPTION`

### Cover Variant
`editorial-light`

### Supporting Sentence
統一認證閘道、Device Flow 與 audience-bound token 的落地實作

### Visual Form
Editorial light cover

### Layout
暖白底；頂部真實 context 與頁碼；左側超大兩行標題；標題下短橘線；兩行內副標；
底部細線、講者與日期。無 Footer Highlight。

### Content
- Context: `內部技術分享 / MCP 認證治理`
- Page Marker: `01 / 10`
- Eyebrow: `MCP AUTH · ADOPTION`
- Presenter: `平台工程團隊`
- Date: `2026.07`

### Visual Hierarchy
1 兩行主標 → 2 短橘線 → 3 副標 → 4 context / 講者 / 日期

### Visual Elements
`add_cover_slide(variant="editorial-light")` ・ top hairline ・ mono context ・
oversized two-line title ・ short orange rule ・ muted subtitle ・ quiet footer

### Source Assets
None

### Source Facts
- Source file: mcp-auth-design.md
- Section: document title / executive summary
- Supporting text: 「統一認證是 MCP 規模化導入的必要控制層」

### Style Constraints
不可改成深色 section divider；不可加入活動品牌、圖片或 Footer Highlight filler。

### Editing Constraints
保留 `editorial-light` 構圖與兩行標題；講者、日期可局部更新。

---

## Slide 04 — 想從 Skill 對接全公司 MCP——卻卡在 Token 明碼躺在 Client 端

### Slide Role
Tension / Root Cause

### Purpose
Explain why internal MCP integration could not scale despite strong demand.

### Argument
The adoption bottleneck was not MCP capability; the real blocker was plaintext
authentication tokens stored on the client side.

### Key Message
Token 明碼躺在 Client 端，才是 MCP 無法規模化推廣的真正阻力。

### Title
想從 Skill 對接全公司 MCP——卻卡在 Token 明碼躺在 Client 端

### Title Emphasis
全公司 MCP ／ Token 明碼（僅此二短語，橘色）

### Eyebrow
`// 04    MCP 推廣的阻力`

### Supporting Sentence
團隊普遍想把內部 MCP 服務接給 Agent 用，但**認證 Token 是明文，直接躺在開發者的 Client 端**。

### Visual Form
Expectation → Reality → Root Cause + terminal/config evidence

### Layout
Header zone（eyebrow / title / supporting / hairline）之下 40/60 分割：左 40% 為
期待→現實→ROOT CAUSE 縱向鏈 + 佐證 bullets；右 60% 為深色 terminal 面板；底部
takeaway line（橘色細 rule）。

### Content
- 期待（綠 pill）：從 Skill 一鍵對接公司**所有 MCP 服務**
- ↓（muted 細箭頭）
- 現實（紅 pill）：MCP 推廣**相當困難**
- ROOT CAUSE（深色面板，橘 mono 標籤）：Token 明碼，就躺在 **Client 端**（橘）
- Bullets：寫死在 `settings.json` → 被 commit 進 Git ／ 用 CLI `--header` 加 →
  一樣明碼，還多一份 ／ 連 `shell history` 裡都撈得到
- Terminal 面板（標題 `~/.claude/settings.json`，RISK 徽章）：
  `"Authorization": "Bearer eyJhbGci…"`（紅）、`$ claude mcp add … --header \`、
  `$ history | grep Bearer`、灰色 `#` 註解
- Takeaway：明碼 Token 躺在 Client 端——正是**三大資安風險**（橘）裡最致命的那一條
  ／右側 muted 指標 `→ 解法詳見 P12`

### Visual Hierarchy
1 Title argument → 2 ROOT CAUSE 面板 → 3 深色 terminal 證據 → 4 佐證 bullets → 5 Takeaway

### Visual Elements
eyebrow ・ mixed-run title ・ supporting sentence ・ hairline ・ status pills（綠/紅）・
downward arrow ・ dark root-cause panel ・ terminal panel（traffic lights + RISK badge +
紅色 secret 高亮）・ mono runs ・ orange takeaway rule

### Source Assets
None — recreated terminal evidence is stronger than the low-resolution screenshot;
`settings-screenshot.png` held in reserve.

### Source Facts
- Source file: mcp-auth-design.md
- Section: “Why adoption stalled”
- Supporting text: 「目前所有 client 以明文 Bearer token 設定於 settings.json 或 CLI 參數」

### Style Constraints
Root-cause 面板深色近黑；不可使用一般企業藍卡片；無裝飾插圖。

### Editing Constraints
保留 40/60 構圖；title 措辭非經明示不得更動；保留 root-cause 強調與 terminal 證據內容。

---

## Slide 07 — Device Flow + PKCE：讓 CLI / MCP 不寫死金鑰

### Slide Role
Mechanism / Protocol

### Purpose
Show precisely how the gateway removes secrets from client disks.

### Argument
整個授權流程沒有任何寫死金鑰——帳密只出現在瀏覽器 SSO 一步。

### Key Message
Token 不落地 config，才能從源頭降低帳密流入 Git 的風險。

### Title
Device Flow + PKCE：讓 CLI / MCP 不寫死金鑰

### Title Emphasis
不寫死金鑰

### Eyebrow
`// 07    機制一 · RFC 8628`

### Supporting Sentence
（omit — the sequence diagram carries the context）

### Visual Form
Sequence diagram（3 actors、numbered interactions、request/response arrows）

### Layout
Actor 方塊橫列頂端（CLI/MCP 深色、使用者·瀏覽器 白、AuthGate 橘）；虛線 lifelines；
6 個編號圓圈訊息由上而下；工作區延伸至底部 margin，不保留 takeaway zone。

### Content
Actors: `CLI / MCP` ・ `使用者 · 瀏覽器` ・ `AuthGate 閘道`
1 要 device code + user code → 2 顯示 URL + user code，請開瀏覽器 →
3 瀏覽器登入並授權 ・ 帳密只在這步，走公司 SSO（橘）→
4 ↻ 同時在背景 polling，等待授權完成（muted, dashed）→
5 發 access token + refresh token → 6 ⤿ token 存進 OS keyring 加密，不落地 config（pill）

### Visual Hierarchy
1 sequence 訊息鏈 → 2 步驟 3 的橘色強調

### Visual Elements
actor nodes ・ dashed lifelines ・ numbered step markers ・ solid/dashed arrows ・
mono annotations ・ pill for keyring note

### Source Facts
- Source file: mcp-auth-design.md · Section “Device Flow”
- Supporting text: 「CLI 端全程不儲存明文金鑰，token 寫入 OS keyring」

### Editing Constraints
保留序列圖結構與訊息順序；不得以卡片替代序列圖。
