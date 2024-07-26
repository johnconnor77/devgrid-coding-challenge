import httpx
import json
from datetime import datetime
from typing import Dict, Any
from models.models import WeatherData
from database.context_manager import SessionLocal
from utilities.constants import cities_id_list
import os

OPEN_WEATHER_API_KEY = os.getenv("OPEN_WEATHER_API_KEY")

CITIES = cities_id_list


async def fetch_weather_data(city_id: int) -> Dict[str, Any]:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"http://api.openweathermap.org/data/2.5/weather",
            params={"id": city_id, "appid": OPEN_WEATHER_API_KEY, "units": "metric"}
        )
        response.raise_for_status()
        weather_data = response.json()
        return {
            "city_id": city_id,
            "temperature": weather_data["main"]["temp"],
            "humidity": weather_data["main"]["humidity"]
        }


async def fetch_and_store_weather_data(user_id: str, cities_list: list = CITIES) -> None:
    db = SessionLocal()
    for city_id in cities_list:
        weather_info = await fetch_weather_data(city_id)
        existing_record = db.query(WeatherData).filter(WeatherData.user_id == user_id).first()
        if existing_record:

            current_data = json.loads(existing_record.data) if existing_record.data else []
            current_data.append(weather_info)
            existing_record.data = json.dumps(current_data)
        else:

            weather_data = WeatherData(
                user_id=user_id,
                timestamp=datetime.utcnow(),
                data=json.dumps([weather_info])
            )
            db.add(weather_data)
        db.commit()
        db.refresh(existing_record or weather_data)
    db.close()
