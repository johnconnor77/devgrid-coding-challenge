import httpx
import asyncio
from datetime import datetime
from typing import Dict, Any
from models.models import WeatherData
from database.context_manager import SessionLocal
import os

OPEN_WEATHER_API_KEY = os.getenv("OPEN_WEATHER_API_KEY")
CITIES = ["London", "Paris", "New York", "Tokyo"]  # Example city names


async def fetch_weather_data(city_name: str) -> Dict[str, Any]:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"http://api.openweathermap.org/data/2.5/weather",
            params={"q": city_name, "appid": OPEN_WEATHER_API_KEY, "units": "metric"}
        )
        response.raise_for_status()
        weather_data = response.json()
        return {
            "city_name": city_name,
            "temperature": weather_data["main"]["temp"],
            "humidity": weather_data["main"]["humidity"]
        }


async def fetch_and_store_weather_data(user_id: str):
    db = SessionLocal()
    data = []
    for city_name in CITIES:
        weather_info = await fetch_weather_data(city_name)
        data.append(weather_info)
        await asyncio.sleep(1)

    weather_data = WeatherData(
        user_id=user_id,
        timestamp=datetime.utcnow(),
        data=data
    )
    db.add(weather_data)
    db.commit()
    db.refresh(weather_data)