from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import List, Dict, Any


class WeatherRequest(BaseModel):
    user_id: str = Field(..., description="User defined ID")

    @field_validator('user_id')
    def user_id_not_empty(cls, v):
        if not v.strip():
            raise ValueError('user_id must not be empty')
        return v


class WeatherData(BaseModel):
    user_id: str
    timestamp: datetime
    data: List[Dict[str, Any]]

    class Config:
        orm_mode = True