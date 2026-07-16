# youtube-summarizer

把公開 YouTube 影片的網址丟給 Gemini API，直接產出重點摘要（不用逐字稿、不用下載影片）。

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

雙擊 `youtube-summarizer\run.bat` → 跳出視窗問 `Paste YouTube URL:` → 貼上網址按 Enter。

或用指令：
```
.venv\Scripts\python.exe youtube-summarizer\summarize.py <youtube網址> [自訂prompt]
```

### macOS / Linux

`run.bat` 是 Windows 批次檔，這個平台改用 `run.sh`：

```
chmod +x youtube-summarizer/run.sh   # 第一次執行前需給執行權限
youtube-summarizer/run.sh
```

會問 `Paste YouTube URL:`，貼上網址按 Enter。

或用指令：
```
.venv/bin/python youtube-summarizer/summarize.py <youtube網址> [自訂prompt]
```

### 輸出

終端機會印出摘要，同時自動存成 `youtube-summarizer/output/{影片ID}.txt`（這個資料夾不進 git，每次執行都會覆寫同一支影片的舊檔）。

### 自訂摘要方式

第二個參數可以換成任何你想要的指令，例如：
```
summarize.py <網址> "請整理成逐字稿"
summarize.py <網址> "用英文列出這部影片的三個重點"
```
不給的話預設是條列式重點摘要。
