# Taiwan language guide

Use this guide for every piece of visible Traditional Chinese in the deck. The target
locale is **Taiwan (`zh-TW`)**, not merely Traditional Chinese character conversion.

## Decision rule

Write the wording a technical team in Taiwan would naturally use. Prefer Taiwan's
common software, interface, and engineering terminology; keep established English
technical terms when they are clearer. Judge terms by context rather than applying
blind search-and-replace.

Priority when wording conflicts:

1. Preserve official product/UI labels exactly when the slide is telling the reader
   what to click or showing a matching screenshot.
2. Preserve verbatim source quotations and label them as quotations.
3. Preserve a user's explicitly requested project term or proper noun.
4. Localize all other explanatory copy to natural Taiwan usage.

## Common choices

| Avoid in ordinary Taiwan-facing copy | Prefer in Taiwan usage | Context note |
|---|---|---|
| 雙擊 | 按兩下／連按兩下 | Use the UI label if a product itself says otherwise. |
| 點擊 | 按一下；點選 | `按一下` for a button/link action; `點選` for selecting an item. |
| 配置 | 設定；組態；配置 | Software options → `設定`; configuration as a technical noun → `組態`; physical or layout arrangement may legitimately be `配置`. |
| 配置文件 | 設定檔／組態檔 | Choose the term already used by the product or team. |
| 文件 | 檔案；文件 | Computer file → `檔案`; formal or written document may remain `文件`. |
| 創建 | 建立 | `新增` when adding an item to an existing collection. |
| 添加 | 新增／加入 | Choose by action. |
| 保存 | 儲存 | `保留` only when meaning keep/retain. |
| 加載 | 載入 | |
| 運行 | 執行 | `運作` when describing how a system operates rather than issuing a command. |
| 構建 | 建置 | Keep `build` when that is the team's normal technical term. |
| 默認 | 預設 | |
| 用戶 | 使用者 | Keep `user` when it is the established technical label. |
| 信息 | 資訊；訊息 | General information → `資訊`; message/notification → `訊息`. |
| 數據 | 資料 | `data` is acceptable when it is the team's established technical term. |
| 代碼 | 程式碼 | Identifier/code value may still be `代碼` (for example, error code). |
| 組件 | 元件 | |
| 視頻 | 影片 | |
| 網絡 | 網路 | |
| 服務器 | 伺服器 | |
| 鼠標 | 滑鼠 | |
| 屏幕 | 螢幕 | |
| 鏈接 | 連結 | |
| 搜索 | 搜尋 | |
| 打印 | 列印 | |
| 導入／導出 | 匯入／匯出 | |
| 支持 | 支援 | For capability/compatibility; `支持` remains valid for endorsing a position. |
| 應用（noun） | 應用程式 | As a verb, use `套用` when applying a setting or change. |
| 內存 | 記憶體 | |
| 硬盤 | 硬碟 | |
| 反饋 | 回饋 | |

## Final language pass

Before approving an outline or reporting a completed build, scan all newly written or
modified visible text for non-Taiwan wording. Check titles, supporting sentences,
labels, table headers/cells, annotations, callouts, instructions, and takeaway lines.
Do not alter evidence, official labels, quotations, code, commands, paths, identifiers,
or URLs during this pass.

Run the bundled checker as a read-only verification step:

```text
scripts/run_python.sh scripts/lint_zh_tw.py presentation/outline.md --outline-visible-only
scripts/run_python.sh scripts/lint_zh_tw.py presentation/presentation.pptx
```

Use `scripts/run_python.ps1` from PowerShell. High-confidence findings return a non-zero
status and must be resolved or explicitly allowed with `--allow-term` or an allowlist.
Context-dependent terms such as `配置` are reported for review but do not fail by
default. The checker never rewrites content.
