# ⚡ Smart Weather Assistant API

> A FastAPI-powered backend that delivers live weather information, intelligent weather recommendations, and structured API responses for the Smart Weather Assistant frontend.

---

## 🌐 Live API

**Production API**

https://smart-weather-assistant-backend.onrender.com

Interactive API Documentation

https://smart-weather-assistant-backend.onrender.com/docs

Alternative Documentation

https://smart-weather-assistant-backend.onrender.com/redoc

---

# ✨ Features

- 🌍 Real-time weather retrieval
- 📍 City-based weather search
- 🌤 Weather condition mapping
- 💡 Intelligent weather recommendations
- 🌙 Local timezone support
- 📦 Structured JSON responses
- ⚡ FastAPI asynchronous endpoints
- 🔒 CORS support
- 🚀 Production deployment on Render

---

# 🛠 Tech Stack

## Backend

- Python 3.12
- FastAPI
- Pydantic
- Uvicorn
- HTTPX

## External Services

- Open-Meteo Forecast API
- Open-Meteo Geocoding API

---

# 🏗 Architecture

```text
                Client
                   │
                   ▼
        Smart Weather Assistant
             React Frontend
                   │
          GET /weather?city=
                   │
                   ▼
              FastAPI API
                   │
        Geocoding Request
                   │
                   ▼
        Open-Meteo Geocoding
                   │
          Latitude/Longitude
                   │
                   ▼
       Open-Meteo Forecast API
                   │
           Weather Response
                   │
                   ▼
     Recommendation Generator
                   │
                   ▼
          Structured JSON
```

---

# 📂 Project Structure

```text
backend/

├── app/
│   ├── api/
│   ├── services/
│   ├── schemas/
│   ├── utils/
│   ├── main.py
│   └── config.py
│
├── requirements.txt
│
└── README.md
```

---

# 🚀 Getting Started

## Clone Repository

```bash
git clone https://github.com/NhartyInnovate/smart-weather-assistant-backend.git
```

---

## Create Virtual Environment

Windows

```bash
python -m venv .venv
```

Activate

```bash
.venv\Scripts\activate
```

macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Run Development Server

```bash
uvicorn app.main:app --reload
```

The API will be available at

```
http://localhost:8000
```

---

# 📡 API Endpoints

## Health Check

Lightweight endpoint used for automated uptime monitoring (e.g., UptimeRobot) and service availability checks. It performs no external calls or database queries.

```http
GET /health
```

### Successful Response

```json
{
  "status": "ok"
}
```

---

## Get Weather

```http
GET /weather?city=Abuja
```

Example

```
GET /weather?city=London
```

---

## Successful Response

```json
{
  "location": {
    "city": "London",
    "country": "United Kingdom",
    "timezone": "Europe/London"
  },
  "weather": {
    "temperature": {
      "value": 18.4,
      "unit": "°C"
    },
    "humidity": {
      "value": 74,
      "unit": "%"
    },
    "wind_speed": {
      "value": 14.8,
      "unit": "km/h"
    },
    "condition": "Partly Cloudy",
    "weather_code": 2,
    "is_day": true
  },
  "advice": "Nice weather for outdoor activities.",
  "metadata": {
    "local_time": "2026-07-14T12:25+01:00",
    "last_updated": "2026-07-14T12:25+01:00"
  }
}
```

---

# ❌ Error Responses

## City Not Found

```json
{
    "detail": "City not found"
}
```

---

## Internal Server Error

```json
{
    "detail": "Unable to retrieve weather information."
}
```

---

# 🌍 Deployment

The API is deployed on **Render**.

Deployment includes

- Automatic builds
- HTTPS
- Public REST endpoint
- Automatic documentation
- CORS configuration

---

# 📖 Interactive Documentation

FastAPI automatically generates API documentation.

Swagger UI

```
/docs
```

ReDoc

```
/redoc
```

---

# 🔄 Request Flow

```text
User Request

      │

      ▼

Validate Input

      │

      ▼

Geocode City

      │

      ▼

Retrieve Weather

      │

      ▼

Generate Recommendation

      │

      ▼

Return Structured Response
```

---

# 🔒 CORS

Cross-Origin Resource Sharing is configured to allow requests from the frontend deployment.

---

# 🧪 Local Testing

Example using curl

```bash
curl "http://localhost:8000/weather?city=Abuja"
```

---

# 📈 Future Improvements

- Weather caching
- Rate limiting
- API authentication
- Redis support
- Docker deployment
- Unit tests
- Integration tests
- Weather history
- Air Quality Index
- Multiple weather providers

---

# 🤝 Contributing

1. Fork the repository

2. Create a new branch

```bash
git checkout -b feature/my-feature
```

3. Commit changes

```bash
git commit -m "Add my feature"
```

4. Push

```bash
git push origin feature/my-feature
```

5. Open a Pull Request

---

# 📄 License

Licensed under the MIT License.

---

# 👨‍💻 Maintainer

## NKay Labs

**AI Engineer • Full Stack Developer**

Building intelligent software powered by AI and scalable backend systems.

---

# 🙏 Acknowledgements

- FastAPI
- Open-Meteo
- Render
- Python
- Pydantic

---

## ⭐ If you found this API useful, consider starring the repository.
