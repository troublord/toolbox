"""YouTube 影片轉重點：餵 YouTube 網址給 Gemini API，回傳重點/逐字稿。"""
import re
import sys
from pathlib import Path

from dotenv import dotenv_values
from google import genai
from google.genai import types

_config = dotenv_values(Path(__file__).parent / ".env")

MODEL = "gemini-flash-latest"
DEFAULT_PROMPT = "請整理這部影片的重點摘要，用條列式呈現，保留關鍵數字、名詞與結論。"
OUTPUT_DIR = Path(__file__).parent / "output"


def extract_video_id(youtube_url: str) -> str:
    match = re.search(r"(?:v=|youtu\.be/)([\w-]+)", youtube_url)
    return match.group(1) if match else "output"


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
    if len(sys.argv) < 2:
        print("用法：python summarize.py <youtube_url> [prompt]")
        sys.exit(1)

    url = sys.argv[1]
    custom_prompt = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_PROMPT
    summary = summarize_video(url, custom_prompt)
    print(summary)

    OUTPUT_DIR.mkdir(exist_ok=True)
    out_path = OUTPUT_DIR / f"{extract_video_id(url)}.txt"
    out_path.write_text(summary, encoding="utf-8")
    print(f"\n已存到 {out_path}")
