"""demo：查詢台北市公車即時到站資訊，驗證整條串接是否成功。"""
import sys

from tdx.client import get

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    data = get(
        "/v2/Bus/EstimatedTimeOfArrival/City/Taipei",
        params={"$top": 5},
    )
    for item in data:
        print(item["RouteName"]["Zh_tw"], "->", item.get("EstimateTime"), "秒")
