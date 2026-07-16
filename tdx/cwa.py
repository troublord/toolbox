"""氣象資料開放鏈結服務（GraphQL）呼叫封裝。"""
from pathlib import Path

import requests
from dotenv import dotenv_values

from .auth import get_access_token

GRAPHQL_URL = "https://tdx.transportdata.tw/api/cwa/graphql"

_config = dotenv_values(Path(__file__).parent / ".env")


def query(gql: str, variables: dict | None = None) -> dict:
    resp = requests.post(
        GRAPHQL_URL,
        params={"Authorization": _config["TDX_CWA_SUBSCRIPTION_KEY"]},
        json={"query": gql, "variables": variables or {}},
        headers={
            "authorization": f"Bearer {get_access_token()}",
            "content-type": "application/json",
        },
        timeout=15,
    )
    resp.raise_for_status()
    return resp.json()
