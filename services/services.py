import httpx
import asyncio
import json
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from typing import Dict, Any
from models.models import WeatherData
from database.context_manager import SessionLocal
import os

OPEN_WEATHER_API_KEY = os.getenv("OPEN_WEATHER_API_KEY")
# make a list of 20 cities
CITIES = ["London", "Paris", "New York", "Tokyo", "Beijing", "Moscow", "Berlin", "Madrid", "Rome", "Athens", "Cairo", "Nairobi", "Cape Town", "Sydney", "New Delhi", "Bangkok", "Singapore", "Jakarta", "Manila", "Seoul"]


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
    for city_name in CITIES:
        weather_info = await fetch_weather_data(city_name)
        existing_record = db.query(WeatherData).filter(WeatherData.user_id == user_id).first()
        if existing_record:
            # Load the existing data into a Python list
            current_data = json.loads(existing_record.data) if existing_record.data else []
            # Append the new weather info
            current_data.append(weather_info)
            # Convert the list back to JSON and update the record
            existing_record.data = json.dumps(current_data)
        else:
            # Insert a new record with the weather info
            weather_data = WeatherData(
                user_id=user_id,
                timestamp=datetime.utcnow(),
                data=json.dumps([weather_info])  # Store the list as JSON
            )
            db.add(weather_data)
        db.commit()  # Commit after each operation
        db.refresh(existing_record or weather_data)
        await asyncio.sleep(1)
    db.close()