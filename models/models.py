from sqlalchemy import Column, String, DateTime, JSON
from database.base import Base


class WeatherData(Base):
    __tablename__ = "weather_data"
    user_id = Column(String, primary_key=True, index=True)
    timestamp = Column(DateTime)
    data = Column(JSON)

# Ensure tables are created
# Base.metadata.create_all(bind=engine)
