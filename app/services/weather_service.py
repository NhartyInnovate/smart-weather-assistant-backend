import httpx
from app.utils.weather_utils import (
    get_weather_condition,
    generate_advice,
)
from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
from cachetools import TTLCache

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

weather_cache = TTLCache(maxsize=500, ttl=600)
geo_cache = TTLCache(maxsize=1000, ttl=86400)


async def get_weather(city: str):
    cache_key = city.lower().strip()
    if cache_key in weather_cache:
        return weather_cache[cache_key]

    async with httpx.AsyncClient(timeout=10) as client:

        # Step 1: Get city coordinates
        if cache_key in geo_cache:
            geo_data = geo_cache[cache_key]
        else:
            geo_response = await client.get(
                GEOCODING_URL,
                params={
                    "name": city,
                    "count": 1
                }
            )
            geo_data = geo_response.json()
            if "results" in geo_data:
                geo_cache[cache_key] = geo_data

        if "results" not in geo_data:
            return None

        location = geo_data["results"][0]

        timezone_str = location.get("timezone") or "UTC"
        try:
            tz = ZoneInfo(timezone_str)
        except (ZoneInfoNotFoundError, ValueError):
            # Fallback to UTC if timezone is unrecognized or invalid
            timezone_str = "UTC"
            tz = ZoneInfo("UTC")

        now = datetime.now(tz)
        local_time = now.isoformat(timespec="minutes")

        latitude = location["latitude"]
        longitude = location["longitude"]

        # Step 2: Get current weather & hourly forecast
        weather_response = await client.get(
            WEATHER_URL,
            params={
                "latitude": latitude,
                "longitude": longitude,
                "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code,is_day",
                "hourly": "temperature_2m,weather_code",
                "timezone": timezone_str
            }
        )

        weather_data = weather_response.json()

        current = weather_data["current"]
        condition = get_weather_condition(current["weather_code"])
        advice = generate_advice(condition, current["temperature_2m"])

        # Process hourly data for the next 12 available hours from current hour
        hourly = weather_data.get("hourly", {})
        hourly_forecast = []

        if hourly and "time" in hourly:
            times = hourly["time"]
            temps = hourly["temperature_2m"]
            codes = hourly["weather_code"]

            current_hour_floor = now.replace(minute=0, second=0, microsecond=0)

            for t, temp, code in zip(times, temps, codes):
                parsed_dt = datetime.fromisoformat(t)
                if parsed_dt.tzinfo is None:
                    dt = parsed_dt.replace(tzinfo=tz)
                else:
                    dt = parsed_dt.astimezone(tz)

                # Include future entries starting from current hour floor across midnight
                if dt >= current_hour_floor:
                    hourly_forecast.append({
                        "time": dt.strftime("%H:%M"),
                        "temperature": temp,
                        "condition": get_weather_condition(code),
                        "weather_code": code
                    })
                    if len(hourly_forecast) >= 12:
                        break

        result = {
            "location": {
                "city": location["name"],
                "country": location["country"],
                "timezone": timezone_str,
            },
            "weather": {
                "temperature": {
                    "value": current["temperature_2m"],
                    "unit": "°C",
                },
                "humidity": {
                    "value": current["relative_humidity_2m"],
                    "unit": "%",
                },
                "wind_speed": {
                    "value": current["wind_speed_10m"],
                    "unit": "km/h",
                },
                "condition": condition,
                "weather_code": current["weather_code"],
                "is_day": bool(current["is_day"]),
            },
            "hourly": hourly_forecast,
            "advice": advice,
            "metadata": {
                "local_time": local_time,
                "last_updated": local_time,
            },
        }

        weather_cache[cache_key] = result
        return result