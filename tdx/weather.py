"""天氣模組：給定座標，回傳可讀的天氣預報＋空氣品質報告。"""
from tdx.cwa import query

GQL = """
query Weather($lon: Float!, $lat: Float!) {
  town(Longitude: $lon, Latitude: $lat) {
    ctyName
    townName
    forecast72hr {
      WeatherDescription { Time { StartTime EndTime WeatherDescription } }
    }
    aqi { sitename aqi status }
  }
}
"""


def get_weather(lat: float, lon: float, periods: int = 4) -> dict:
    """periods：回傳未來幾個 3 小時預報時段（4 段 = 未來 12 小時）。"""
    data = query(GQL, {"lon": lon, "lat": lat})["data"]["town"]
    return {
        "cty_name": data["ctyName"],
        "town_name": data["townName"],
        "forecast": data["forecast72hr"]["WeatherDescription"]["Time"][:periods],
        "aqi": data["aqi"],
    }


def format_weather(report: dict) -> str:
    lines = [f"{report['cty_name']}{report['town_name']} 天氣預報"]
    for period in report["forecast"]:
        start = period["StartTime"][11:16]
        end = period["EndTime"][11:16]
        lines.append(f"  {start}-{end}｜{period['WeatherDescription']}")

    lines.append(f"\n空氣品質（{report['cty_name']}全縣市測站，非最近點）")
    for site in report["aqi"]:
        lines.append(f"  {site['sitename']}：AQI {site['aqi']}（{site['status']}）")

    return "\n".join(lines)


if __name__ == "__main__":
    import sys

    sys.stdout.reconfigure(encoding="utf-8")
    report = get_weather(lat=22.582, lon=120.322)  # 前鎮
    print(format_weather(report))
