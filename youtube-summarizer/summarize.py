"""YouTube 影片轉重點：餵 YouTube 網址給 Gemini API，回傳重點/逐字稿。"""
import re
import sys
from pathlib import Path

import requests
from dotenv import dotenv_values
from google import genai
from google.genai import types

_config = dotenv_values(Path(__file__).parent / ".env")

MODEL = "gemini-flash-latest"
DEFAULT_PROMPT = "請整理這部影片的重點摘要，用條列式呈現，保留關鍵數字、名詞與結論。"
TRANSCRIPT_PROMPT = "請提供這部影片完整逐字稿，盡量逐字呈現，不要摘要或省略。"
OUTPUT_DIR = Path(__file__).parent / "output"


def extract_video_id(youtube_url: str) -> str:
    match = re.search(r"(?:v=|youtu\.be/|shorts/)([\w-]+)", youtube_url)
    return match.group(1) if match else "output"


def get_video_title(youtube_url: str) -> str:
    """透過 YouTube oEmbed（免金鑰）取得影片標題，失敗則退回 video ID。"""
    try:
        resp = requests.get(
            "https://www.youtube.com/oembed",
            params={"url": youtube_url, "format": "json"},
            timeout=10,
        )
        resp.raise_for_status()
        return resp.json()["title"]
    except Exception:
        return extract_video_id(youtube_url)


def sanitize_filename(name: str, max_length: int = 80) -> str:
    name = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", name).strip().rstrip(".")
    return name[:max_length] or "untitled"


def summarize_video(youtube_url: str, prompt: str = DEFAULT_PROMPT) -> str:
    api_key = _config.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "缺少 GEMINI_API_KEY，請在 youtube-summarizer/.env 設定（可參考 .env.example）"
        )

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model=MODEL,
        contents=types.Content(
            parts=[
                types.Part(file_data=types.FileData(file_uri=youtube_url)),
                types.Part(text=prompt),
            ]
        ),
    )
    return response.text


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")

    if len(sys.argv) >= 2:
        url = sys.argv[1]
        mode = sys.argv[2] if len(sys.argv) > 2 else "summary"
        custom_prompt = sys.argv[3] if len(sys.argv) > 3 else None
    else:
        choice = input("選擇模式 1) 摘要 2) 逐字稿 (預設1)：").strip()
        mode = "transcript" if choice == "2" else "summary"
        url = input("Paste YouTube URL: ").strip()
        custom_prompt = None
        if not url:
            print("沒有輸入網址，結束。")
            sys.exit(1)

    if mode == "transcript":
        prompt = custom_prompt or TRANSCRIPT_PROMPT
        suffix = "_transcript"
    else:
        prompt = custom_prompt or DEFAULT_PROMPT
        suffix = ""

    print("處理中，請稍候（依影片長度可能需要 10 秒到數分鐘）...", flush=True)
    summary = summarize_video(url, prompt)
    print(summary)

    OUTPUT_DIR.mkdir(exist_ok=True)
    video_id = extract_video_id(url)
    safe_title = sanitize_filename(get_video_title(url))
    out_path = OUTPUT_DIR / f"{safe_title} [{video_id}]{suffix}.txt"
    out_path.write_text(summary, encoding="utf-8")
    print(f"\n已存到 {out_path}")
