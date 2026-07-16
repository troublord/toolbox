"""TDX API 呼叫封裝。"""
import requests

from .auth import get_access_token

BASE_URL = "https://tdx.transportdata.tw/api/basic"


def get(path: str, params: dict | None = None) -> dict | list:
    """對 TDX API 發送 GET 請求，自動帶上 Authorization header。

    path 範例："/v2/Bus/EstimatedTimeOfArrival/City/Taipei"
    params 支援 OData 查詢語法，例如 {"$format": "JSON", "$top": 10}
    """
    params = dict(params or {})
    params.setdefault("$format", "JSON")

    resp = requests.get(
        f"{BASE_URL}{path}",
        params=params,
        headers={"authorization": f"Bearer {get_access_token()}"},
        timeout=10,
    )
    resp.raise_for_status()
    return resp.json()
