import os
import sys
import asyncio
from datetime import datetime
from zoneinfo import ZoneInfo
from unittest.mock import AsyncMock, patch, MagicMock
from fastapi.testclient import TestClient
from app.main import app
from app.services.weather_service import get_weather

client = TestClient(app)


def test_health_check_returns_200():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_root_endpoint_returns_200():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Welcome to Smart Weather Assistant API"
    }


def test_weather_endpoint_is_registered():
    # Calling /weather without city parameter returns 422
    response = client.get("/weather")
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data
    assert any("city" in str(err.get("loc", [])) for err in data["detail"])


def test_iana_timezone_resolution():
    # Verify both European and African timezones resolve via zoneinfo / tzdata
    tz_london = ZoneInfo("Europe/London")
    assert str(tz_london) == "Europe/London"

    tz_lagos = ZoneInfo("Africa/Lagos")
    assert str(tz_lagos) == "Africa/Lagos"


def test_weather_service_timezone_fallback_and_schema():
    # Deterministic test: Invalid/Unknown timezone string falls back to UTC
    mock_geo_resp = MagicMock()
    mock_geo_resp.json.return_value = {
        "results": [
            {
                "name": "Atlantis",
                "country": "Atlantic Ocean",
                "timezone": "Invalid/Unknown_Zone",
                "latitude": 25.0,
                "longitude": -40.0,
            }
        ]
    }

    mock_weather_resp = MagicMock()
    mock_weather_resp.json.return_value = {
        "current": {
            "temperature_2m": 22.5,
            "relative_humidity_2m": 60,
            "wind_speed_10m": 12.0,
            "weather_code": 0,
            "is_day": 1,
        },
        "hourly": {
            "time": ["2026-10-21T18:00", "2026-10-21T19:00"],
            "temperature_2m": [22.0, 21.0],
            "weather_code": [0, 1],
        },
    }

    with patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get:
        mock_get.side_effect = [mock_geo_resp, mock_weather_resp]
        result = asyncio.run(get_weather("Atlantis_Fallback_Test"))

        assert result is not None
        assert result["location"]["city"] == "Atlantis"
        assert result["location"]["timezone"] == "UTC"
        assert "metadata" in result
        assert "local_time" in result["metadata"]
        assert "+00:00" in result["metadata"]["local_time"] or "Z" in result["metadata"]["local_time"]
        assert result["weather"]["temperature"]["value"] == 22.5
        assert result["weather"]["condition"] == "Clear Sky"


def test_deterministic_valid_city_weather_contract():
    # Deterministic test: Valid city with real timezone (Europe/London) and full contract
    mock_geo_resp = MagicMock()
    mock_geo_resp.json.return_value = {
        "results": [
            {
                "name": "London",
                "country": "United Kingdom",
                "timezone": "Europe/London",
                "latitude": 51.5085,
                "longitude": -0.1257,
            }
        ]
    }

    now_iso = datetime.now().strftime("%Y-%m-%dT%H:00")
    mock_weather_resp = MagicMock()
    mock_weather_resp.json.return_value = {
        "current": {
            "temperature_2m": 16.0,
            "relative_humidity_2m": 72,
            "wind_speed_10m": 14.5,
            "weather_code": 2,
            "is_day": 1,
        },
        "hourly": {
            "time": [now_iso],
            "temperature_2m": [16.0],
            "weather_code": [2],
        },
    }

    with patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get:
        mock_get.side_effect = [mock_geo_resp, mock_weather_resp]
        response = client.get("/weather?city=London_Deterministic_Test")
        assert response.status_code == 200
        data = response.json()

        # Verify full API contract schema
        assert data["location"]["city"] == "London"
        assert data["location"]["country"] == "United Kingdom"
        assert data["location"]["timezone"] == "Europe/London"

        assert data["weather"]["temperature"]["value"] == 16.0
        assert data["weather"]["temperature"]["unit"] == "°C"
        assert data["weather"]["humidity"]["value"] == 72
        assert data["weather"]["humidity"]["unit"] == "%"
        assert data["weather"]["wind_speed"]["value"] == 14.5
        assert data["weather"]["wind_speed"]["unit"] == "km/h"
        assert data["weather"]["condition"] == "Partly Cloudy"
        assert data["weather"]["is_day"] is True

        assert isinstance(data["hourly"], list)
        assert len(data["hourly"]) >= 1
        assert "time" in data["hourly"][0]
        assert "temperature" in data["hourly"][0]
        assert "condition" in data["hourly"][0]

        assert "advice" in data
        assert "metadata" in data
        assert "local_time" in data["metadata"]


def run_live_integration_test():
    """
    OPTIONAL: Integration test requiring live outbound internet connection to Open-Meteo.
    Run manually with:
        python tests/test_health.py --live
    """
    print("\nRunning optional live network integration test (requires internet access)...")
    response = client.get("/weather?city=London")
    assert response.status_code == 200
    data = response.json()
    assert data["location"]["city"] == "London"
    assert data["location"]["timezone"] == "Europe/London"
    print("PASS: run_live_integration_test")


if __name__ == "__main__":
    test_health_check_returns_200()
    print("PASS: test_health_check_returns_200")

    test_root_endpoint_returns_200()
    print("PASS: test_root_endpoint_returns_200")

    test_weather_endpoint_is_registered()
    print("PASS: test_weather_endpoint_is_registered")

    test_iana_timezone_resolution()
    print("PASS: test_iana_timezone_resolution (Europe/London & Africa/Lagos)")

    test_weather_service_timezone_fallback_and_schema()
    print("PASS: test_weather_service_timezone_fallback_and_schema")

    test_deterministic_valid_city_weather_contract()
    print("PASS: test_deterministic_valid_city_weather_contract")

    print("\nAll 6 deterministic core unit tests passed successfully!")

    if "--live" in sys.argv or os.environ.get("RUN_LIVE_TESTS") == "1":
        run_live_integration_test()
