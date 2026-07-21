# youtube-summarizer

把公開 YouTube 影片的網址丟給 Gemini API，直接產出重點摘要或逐字稿（不用下載影片）。

逐字稿模式仍是 Gemini 生成式理解影片內容，不是專用語音辨識（ASR），可能出現意譯、跳句或不夠逐字精準，影片太長時也可能被截斷。

## 需求

- Python 3.10+
- Gemini API key（免費申請：https://aistudio.google.com/apikey）
- 影片必須是**公開**的 YouTube 影片（不支援私人/未公開連結）

## 安裝

在 `toolbox` 根目錄下執行：

**Windows**
```
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt -r youtube-summarizer\requirements.txt
```

**macOS / Linux**
```
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt -r youtube-summarizer/requirements.txt
```

然後複製 `youtube-summarizer/.env.example` 為 `youtube-summarizer/.env`，填入你自己的 key：

```
GEMINI_API_KEY=你的key
```

## 使用方式

### Windows

雙擊 `youtube-summarizer\run.bat` → 選擇模式（1=摘要 / 2=逐字稿，預設1）→ 貼上網址按 Enter。

或用指令：
```
.venv\Scripts\python.exe youtube-summarizer\summarize.py <youtube網址> [summary|transcript] [自訂prompt]
```

### macOS / Linux

`run.bat` 是 Windows 批次檔，這個平台改用 `run.sh`：

```
chmod +x youtube-summarizer/run.sh   # 第一次執行前需給執行權限
youtube-summarizer/run.sh
```

會依序問模式（1=摘要 / 2=逐字稿）和 `Paste YouTube URL:`。

或用指令：
```
.venv/bin/python youtube-summarizer/summarize.py <youtube網址> [summary|transcript] [自訂prompt]
```

### 輸出

終端機會印出結果，同時自動存成：
- 摘要模式 → `youtube-summarizer/output/{影片標題} [{影片ID}].txt`
- 逐字稿模式 → `youtube-summarizer/output/{影片標題} [{影片ID}]_transcript.txt`

影片標題透過 YouTube oEmbed（免金鑰）取得，若取得失敗則退回用影片 ID 當檔名；檔名中不合法字元會被替換成 `_`。兩種模式各自獨立存檔，不會互相覆寫；同模式重複執行同一支影片會覆寫舊檔。`output/` 資料夾不進 git。

### 自訂 prompt

第三個參數可以覆寫該模式的預設 prompt，例如：
```
summarize.py <網址> summary "用英文列出這部影片的三個重點"
summarize.py <網址> transcript "請提供逐字稿並標註大約的時間點"
```
不給的話依模式使用預設 prompt（摘要／逐字稿）。
