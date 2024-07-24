from fastapi import FastAPI, HTTPException
from models.models import WeatherData
from database.schemas import WeatherRequest, WeatherData as WeatherDataSchema
from services.services import fetch_and_store_weather_data
from database.context_manager import SessionLocal

# Ensure tables are created
#Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.post("/weather/")
async def post_weather(request: WeatherRequest):
    db = SessionLocal()
    existing_record = db.query(WeatherData).filter(WeatherData.user_id == request.user_id).first()
    if existing_record:
        raise HTTPException(status_code=400, detail="User ID already exists")

    await fetch_and_store_weather_data(request.user_id)
    return  {"message": "Weather data collection started"}

@app.get("/weather/{user_id}", response_model=WeatherDataSchema)
async def get_weather(user_id: str):
    db = SessionLocal()
    result = db.query(WeatherData).filter(WeatherData.user_id == user_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="User ID not found")
    return result
