from fastapi.testclient import TestClient
from app.main import app

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
    response = client.get("/weather")
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data
    assert any("city" in str(err.get("loc", [])) for err in data["detail"])


if __name__ == "__main__":
    test_health_check_returns_200()
    print("PASS: GET /health returns 200 OK and {'status': 'ok'}")
    test_root_endpoint_returns_200()
    print("PASS: GET / returns 200 OK and expected welcome message")
    test_weather_endpoint_is_registered()
    print("PASS: GET /weather is registered and validates parameters (422 for missing city)")
    print("\nAll tests passed successfully!")
