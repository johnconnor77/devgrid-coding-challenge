import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.context_manager import SessionLocal
from database.base import Base
from main import app
import json
from unittest.mock import patch
import httpx

# Create a test database and session
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[SessionLocal] = override_get_db
client = TestClient(app)


@pytest.fixture(scope="module")
def client_fixture():
    yield client


@pytest.fixture(scope="module")
def setup_db_fixture():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def mock_fetch_weather_data(city_id):
    return {
        "coord": {"lon": 139, "lat": 35},
        "weather": [{"id": 800, "main": "Clear", "description": "clear sky", "icon": "01n"}],
        "base": "stations",
        "main": {"temp": 281.52, "feels_like": 278.99, "temp_min": 280.15, "temp_max": 283.71, "pressure": 1016, "humidity": 93},
        "wind": {"speed": 0.47, "deg": 107.538},
        "clouds": {"all": 2},
        "dt": 1560350192,
        "sys": {"type": 3, "id": 2019346, "message": 0.0065, "country": "JP", "sunrise": 1560281377, "sunset": 1560333478},
        "timezone": 32400,
        "id": city_id,
        "cod": 200
    }


@patch('services.services.fetch_weather_data', side_effect=mock_fetch_weather_data)
def test_post_weather(mock_fetch, client_fixture, setup_db_fixture):
    response = client_fixture.post("/weather/", json={"user_id": "test_user"})
    assert response.status_code == 200
    assert response.json() == {"message": "Weather data collection started"}


@patch('services.services.fetch_weather_data', side_effect=mock_fetch_weather_data)
def test_post_weather_duplicate_user_id(mock_fetch, client_fixture, setup_db_fixture):
    client_fixture.post("/weather/", json={"user_id": "test_user"})
    response = client_fixture.post("/weather/", json={"user_id": "test_user"})
    assert response.status_code == 400
    assert response.json() == {"detail": "User ID already exists"}


@patch('services.services.fetch_weather_data', side_effect=mock_fetch_weather_data)
def test_get_weather(mock_fetch, client_fixture, setup_db_fixture):
    client_fixture.post("/weather/", json={"user_id": "test_user"})
    response = client_fixture.get("/weather/test_user")
    assert response.status_code == 200
    assert "percentage_uploaded" in response.json()


def test_get_weather_user_id_not_found(client_fixture, setup_db_fixture):
    response = client_fixture.get("/weather/non_existent_user")
    assert response.status_code == 404
    assert response.json() == {"detail": "User ID not found"}


@patch('services.services.fetch_weather_data', side_effect=mock_fetch_weather_data)
def test_get_weather_percentage_uploaded(mock_fetch, client_fixture, setup_db_fixture):
    client_fixture.post("/weather/", json={"user_id": "test_user"})
    response = client_fixture.get("/weather/test_user")
    assert response.status_code == 200
    assert "percentage_uploaded" in response.json()
    assert "100%" in response.json()["percentage_uploaded"]


def test_get_weather_percentage_user_id_not_found(client_fixture, setup_db_fixture):
    response = client_fixture.get("/weather/non_existent_user")
    assert response.status_code == 404
    assert response.json() == {"detail": "User ID not found"}
