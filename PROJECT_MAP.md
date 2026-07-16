# PROJECT_MAP — toolbox

> 這份文件給「未來的我」和「AI 助手」看。
> 目的：想確認「有沒有現成工具可以用/擴充」時，先看這裡，不用重新翻每個資料夾。
> 最後更新：2026-07-16

---

## 1. 這個 repo 是什麼

累積各種一次性/實驗性的小工具，每個工具一個獨立子資料夾，彼此不互相依賴。

不追求產品化，每個工具的完成標準是「自己能重複使用」，不是「給別人用」。

**本機路徑**：`D:\workspace\toolbox\`
**GitHub**：（尚未建立）

**依賴管理**：根目錄 `requirements.txt` 是所有工具共用的基本依賴（requests、python-dotenv）。個別工具若有額外依賴，在該工具資料夾內另建 `requirements.txt` 補充。

**環境變數**：每個工具若需要 API key，在自己資料夾內放 `.env`（不進 git，已在 `.gitignore` 排除）+ `.env.example`（進 git，當範本）。

---

## 2. 工具清單

### tdx/ — TDX 運輸資料流通服務 API 封裝

**狀態**：完成，天氣模組可用；交通/地點/推播延伸構想已擱置。

**用途**：查詢台灣 TDX 平台的天氣預報＋空氣品質資料（給定經緯度）。原本目標是練習串接政府開放資料 API（OAuth2.0 Client Credentials 認證），後來收斂出可重複使用的天氣查詢模組。

**核心檔案**：
- `auth.py` — OAuth2.0 Client Credentials 取得並快取 access token（24 小時效期）
- `client.py` — 封裝 TDX REST API GET 請求（公車/鐵路等基礎服務用）
- `cwa.py` — 氣象資料開放鏈結服務封裝（GraphQL，需額外的 `TDX_CWA_SUBSCRIPTION_KEY`）
- `weather.py` — 對外主要介面：`get_weather(lat, lon, periods=4)` 回傳結構化天氣＋空品資料，`format_weather(report)` 轉可讀文字
- `demo.py` / `demo_weather.py` — 使用範例

**執行方式**：在 `D:\workspace\toolbox\` 根目錄下 `python -m tdx.demo_weather`（需先在 `tdx/.env` 填入 `TDX_CLIENT_ID`／`TDX_CLIENT_SECRET`／`TDX_CWA_SUBSCRIPTION_KEY`，參考 `tdx/.env.example`）。

**擱置的延伸構想**：曾規劃「每日通勤決策簡報」（天氣＋交通＋地點清單＋LINE 推播整合），因交通模組（公車/捷運/高鐵）實用性低（平常不常搭大眾運輸）而擱置。若之後有明確需求可重啟，完整討論脈絡見 Treasury-Vault `05-Log/工作紀錄/2026-07-05 Python 串接 TDX 運輸資料流通服務 API.md`。

---

### youtube-summarizer/ — YouTube 影片轉重點（規劃中，尚未動工）

**狀態**：規劃中。

**用途**：Research 時常遇到 YouTube 影片沒有逐字稿，想用 Gemini API 直接餵 YouTube 網址（`fileData: { fileUri }`），讓 AI 讀影片內容產出重點/逐字稿，取代人工聽打。

詳細待辦見 Treasury-Vault `00-Capture/待辦｜YouTube 影片轉重點小工具.md`。
