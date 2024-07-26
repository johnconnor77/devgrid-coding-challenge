from fastapi import FastAPI, HTTPException
from models.models import WeatherData
from database.schemas import WeatherRequest, GetWeatherResponse, PostWeatherResponse
from services.services import fetch_and_store_weather_data
from database.context_manager import SessionLocal
from services.services import CITIES
import json


app = FastAPI()


@app.post("/weather/", response_model=PostWeatherResponse)
async def post_weather(request: WeatherRequest):
    db = SessionLocal()
    existing_record = db.query(WeatherData).filter(WeatherData.user_id == request.user_id).first()
    if existing_record:
        raise HTTPException(status_code=400, detail="User ID already exists")

    await fetch_and_store_weather_data(request.user_id)

    result = {"message": "Weather data collection started"}

    return result


@app.get("/weather/{user_id}", response_model=GetWeatherResponse)
async def get_weather(user_id: str):

    if user_id == " ":
        raise HTTPException(status_code=422, detail="User ID cannot be empty")

    db = SessionLocal()
    total_cities = len(CITIES)
    record = db.query(WeatherData).filter(WeatherData.user_id == user_id).first()

    if not record:
        raise HTTPException(status_code=404, detail="User ID not found")

    entries_count = len(json.loads(record.data))

    percentage_uploaded = int((entries_count / total_cities) * 100)

    result = db.query(WeatherData).filter(WeatherData.user_id == user_id).first()

    result_data = {
        "user_id": result.user_id,
        "timestamp": result.timestamp,
        "data": result.data,
        "percentage_uploaded": f"{percentage_uploaded}% is being uploaded"
    }
    return result_data
