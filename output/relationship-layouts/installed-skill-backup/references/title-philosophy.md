# title-philosophy.md — titles communicate points, not topics

One of the highest-priority rules of this skill.

## Voice & register (applies to ALL visible text, not just titles)

The deck is **one engineer sharing findings with 同仁** — teammates who will read it,
ask questions, and maybe act on it. It is a written artifact, not a script for a stage.

Write in **plain declarative statements**: state the fact, the mechanism, the finding,
the constraint, the implication. Do not perform.

Use **natural engineering language**: concrete nouns, active verbs, situated details,
and explicit trade-offs. Let warmth come from clarity and judgment rather than invented
people, emotions, anecdotes, or motivational language. Avoid generic AI filler, polished
marketing phrases, and mechanically parallel three-part sentences.

- **No hosting.** No welcoming, thanking, transitioning ("接下來讓我們…"), no
  crowd address (各位 / 大家), no opening or closing pleasantries, no session framing
  (全場主軸 / 本場重點 / 壓軸). A slide never announces what the deck is about to do;
  it just says the thing.
- **No suspense.** Never withhold a conclusion to hold attention. State findings where
  they belong; cross-reference plainly (`詳見 P8`) instead of teasing (`解法看後半段`).
- **Don't force first person.** Default to impersonal, fact-forward phrasing rather
  than narrating yourself ("我看到…", "我今天要講…"). `我們` is fine when it genuinely
  means this team and carries information ("我們目前卡在 X"), not as rapport-building.
- **Recommendations stay recommendations.** When content is a proposal rather than a
  shipped result, phrase it as such ("可以先從 X 試", "建議 …") — never present an
  untried idea in the voice of an achievement.
- Concrete nouns, active verbs, real numbers. Sentences short enough to scan.

| Host tone (banned) | Colleague share (use) |
|---|---|
| 全場主軸 · 企業演進三階段 | 企業演進三階段 |
| 接下來讓我們看 Gemini Enterprise 的四層架構 | Gemini Enterprise 用四層把 Agent 帶到生產規模 |
| → 解法看後半段 | → 詳見 P12 |
| 今天很榮幸跟大家分享我們的導入經驗 | 導入經驗：四輪掃描後弱點修復已可重複 |
| 以上就是我的分享，謝謝大家 | 三個可以立刻試的下一步 |

## The rule

A slide title should usually communicate a point: an argument, finding, contrast,
tension, root cause, technical conclusion, consequence, or turning point. A title is
not a topic label.

| Bad (topic label) | Better (argument) |
|---|---|
| CI 資安審查 | CI 流程最關鍵的一關：資安審查 |
| MCP Token 問題 | 想從 Skill 對接全公司 MCP——卻卡在 Token 明碼躺在 Client 端 |
| AlloyDB 效能 | 搬到 AlloyDB 不代表查詢會自動變快——第一個瓶頸其實在資料結構 |
| Fortify 弱點修改 | 四輪 Fortify 掃描後，弱點修復已從人工試錯變成可重複流程 |

Patterns the reference deck uses:
- Tension with `——`: expectation on the left, blocking reality on the right.
- Reframe: 「主管的兩難 = 缺一條『安全的路』」 (an equation, not a heading).
- Provocation + correction: 「Agent Skill 出現，~~MCP 已死~~？其實不然」.
- Consequence: 「CI 把開發流程統一成一條流水線——PM / Team Lead 才能做最好的 Tracking」.
- Threshold naming: 「全公司落地的真正門檻：專案爆炸」.

## The constraint

The title must remain defensible. Do not exaggerate weak evidence, and do not invent
conflict for drama. If the source only supports 「效能有改善」, the title cannot claim
a number or a breakthrough. Exceptions where a plain label is fine: agenda, speaker,
section dividers, thank-you.

## Title emphasis

When a title contains a decisive phrase, color ONLY that phrase orange (mixed color
runs inside one paragraph — never separate, misaligned text boxes unless technically
unavoidable). Usually one phrase, at most two short ones. Never the whole title;
never force orange into a title that has no decisive phrase. Emphasis must improve
scanability: the orange words alone should carry the point (`全公司 MCP` +
`Token 明碼`; `一條流水線`). Rare risk titles may use red for the risk phrase.

## Supporting sentence

A short muted sentence directly below many titles. It explains the title — clarifies
scope, establishes mechanism, provides factual context — and never repeats it
word-for-word. Muted gray, with the pivotal technical phrase bolded in dark ink:

> Title: CI 流程最關鍵的一關：資安審查
> Supporting: 同一個 PR，**三道並行的 code review** 同時把關——從靜態分析、漏洞掃描，到 AI 情境審查。
