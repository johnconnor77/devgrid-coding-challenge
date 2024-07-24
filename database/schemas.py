from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Dict, Any


class WeatherRequest(BaseModel):
    user_id: str = Field(..., description="User defined ID")


class WeatherData(BaseModel):
    user_id: str
    timestamp: datetime
    data: List[Dict[str, Any]]

    class Config:
        orm_mode = True