"""demo：用經緯度查詢氣象資料開放鏈結服務（天氣預報 + 觀測 + 空氣品質）。"""
import sys

from tdx.cwa import query

GQL = """
query Weather($lon: Float!, $lat: Float!) {
  town(Longitude: $lon, Latitude: $lat) {
    ctyName
    townName
    forecast72hr {
      WeatherDescription { Time { StartTime EndTime WeatherDescription } }
      Temperature { Time { DataTime Temperature } }
      ProbabilityOfPrecipitation { Time { StartTime EndTime ProbabilityOfPrecipitation } }
    }
    aqi { sitename aqi status pm2_5 publishtime }
    station {
      StationName
      WeatherElement { AirTemperature Weather RelativeHumidity WindSpeed }
    }
  }
}
"""

# 前鎮（高雄）大概座標
LOCATIONS = {
    "前鎮": (22.582, 120.322),
}

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    name, (lat, lon) = next(iter(LOCATIONS.items()))
    result = query(GQL, {"lon": lon, "lat": lat})
    import json
    print(json.dumps(result, ensure_ascii=False, indent=2))
