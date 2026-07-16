"""TDX OAuth2.0 Client Credentials 認證。"""
import time
from pathlib import Path

import requests
from dotenv import dotenv_values

TOKEN_URL = "https://tdx.transportdata.tw/auth/realms/TDXConnect/protocol/openid-connect/token"

_config = dotenv_values(Path(__file__).parent / ".env")
_cached_token = None
_expires_at = 0


def get_access_token() -> str:
    """回傳有效的 access token，過期前自動重新取得（token 效期 24 小時）。"""
    global _cached_token, _expires_at

    if _cached_token and time.time() < _expires_at:
        return _cached_token

    client_id = _config.get("TDX_CLIENT_ID")
    client_secret = _config.get("TDX_CLIENT_SECRET")
    if not client_id or not client_secret:
        raise RuntimeError(
            "缺少 TDX_CLIENT_ID / TDX_CLIENT_SECRET，請在 tdx/.env 設定（可參考 .env.example）"
        )

    resp = requests.post(
        TOKEN_URL,
        data={
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        timeout=10,
    )
    resp.raise_for_status()
    payload = resp.json()

    _cached_token = payload["access_token"]
    _expires_at = time.time() + payload["expires_in"] - 60  # 提前 60 秒視為過期
    return _cached_token
