# 簡報敘事與生成

這個 context 定義本專案如何把工程素材整理成有證據、可閱讀、也有人味的技術簡報。

## Language

**黃金圈規劃框架**：
所有新簡報都用 Why → How → What 作為隱性的規劃檢查表：先確認為什麼值得在意，再說明如何處理，最後落到具體內容與證據。不要求投影片顯式分成三段。
_Avoid_: 黃金圈三段式模板、每份簡報固定切成 Why／How／What 三章

**自然工程語氣**：
讓投影片用具體、有脈絡、有判斷的語言表達工程發現與取捨；可以呈現摩擦、限制與改善 stakes，但不要求人物故事或情緒，也不靠虛構內容製造溫度。
_Avoid_: AI 感套話、行銷金句、機械式三段排比、煽情、虛構案例或未被來源支持的結果

**敘事分岔檢查點（Narrative Fork checkpoint）**：
在完整 outline 前比較三個精簡、由證據支持的敘事軸線。只比較 thesis、適用對象與情境、高階 flow、證據基礎及風險，不展開成三份完整 outline 或 deck。
_Avoid_: 一開始就平行生成多份完整簡報、方向未確認便進入 builder

**成本模式（cost mode）**：
`standard` 為預設，方向明確時直接進 outline；`explore` 明確要求時才主動提供敘事分岔；`strict` 只有使用者明講省錢、快速或少探索等意圖才啟用。Prompt 明確只會讓 standard 跳過敘事分岔，不會自動切成 strict。
_Avoid_: 用 prompt 清楚度猜測 strict、用 strict 跳過 outline 確認

**修改影響分類（Edit Impact Classification）**：
修改現有簡報前，先區分小型局部修改、單頁結構修改、跨頁修改、敘事重整與 full rebuild candidate。非小型修改先留下 `edit-impact.md`；高成本重建需明確確認。
_Avoid_: 把局部要求擴張成 redesign、未回到文字階段就直接重做整份 deck
