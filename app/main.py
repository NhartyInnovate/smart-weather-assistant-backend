from fastapi import FastAPI

from app.api.weather import router as weather_router

app = FastAPI(
    title="Smart Weather Assistant API",
    description="""
## Smart Weather Assistant

A lightweight REST API built with FastAPI that provides:

- 🌤 Current weather by city
- 📍 Geocoding support
- 💡 Smart weather recommendations
- 📦 Structured JSON responses
- ⚡ Powered by Open-Meteo

Designed as a clean backend portfolio project.
""",
    version="1.0.0",
    contact={
        "name": "Nathaniel Katugwa",
        "url": "https://github.com/NhartyInnovate",
    },
    license_info={
        "name": "MIT License",
    },
)


@app.get("/")
def home():
    return {
        "message": "Welcome to Smart Weather Assistant API"
    }


@app.get("/health")
def health():
    return {
        "status": "ok"
    }


app.include_router(weather_router)
