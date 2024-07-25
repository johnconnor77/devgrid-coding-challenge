import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from asynctest import CoroutineMock
from services.services import fetch_weather_data, fetch_and_store_weather_data
from utilities.constants import cities_id_list_test as CITIES_TEST
from models.models import WeatherData
from database.context_manager import engine
from database.base import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import json

# Set up the database URL for testing
DATABASE_URL = "sqlite:///./test_services.db"
# Create the engine and session for the test database
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function", autouse=True)
def create_test_database():
    # Create the database and tables before running tests
    Base.metadata.create_all(bind=engine)
    yield
    # Drop the database and tables after running tests
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def mock_open_weather_api_key(monkeypatch):
    monkeypatch.setenv("OPEN_WEATHER_API_KEY", "mock_api_key")


@pytest.fixture
def mock_weather_data():
    return {
        "main": {
            "temp": 20.0,
            "humidity": 60
        }
    }


@pytest.fixture
def db_session():
    session = TestingSessionLocal()
    yield session
    session.close()


@pytest.mark.asyncio
async def test_fetch_weather_data(mock_weather_data):

    async def mock_get(*args, **kwargs):
        mock_response = CoroutineMock()
        mock_response.json.return_value = mock_weather_data
        mock_response.raise_for_status = CoroutineMock()
        return mock_response

    with patch('httpx.AsyncClient.get', new=mock_get):
        city_id = 3439525
        weather_data = await fetch_weather_data(city_id)
        assert weather_data == {
            "city_id": city_id,
            "temperature": mock_weather_data['main']['temp'],
            "humidity": mock_weather_data['main']['humidity']
        }


@pytest.mark.asyncio
async def test_fetch_and_store_weather_data(mock_weather_data, db_session):
    async def mock_get(*args, **kwargs):
        mock_response = CoroutineMock()
        mock_response.json.return_value = mock_weather_data
        mock_response.raise_for_status = CoroutineMock()
        return mock_response

    with patch('httpx.AsyncClient.get', new=mock_get):
        user_id = "test_user"
        await fetch_and_store_weather_data(user_id, cities_list=CITIES_TEST)

        # Ensure data was inserted correctly
        record = db_session.query(WeatherData).filter_by(user_id=user_id).first()
        assert record is not None
        assert json.loads(record.data)[0]["city_id"] == CITIES_TEST[0]


@pytest.mark.asyncio
async def test_fetch_and_store_weather_data(mock_weather_data):
    mock_db_session = MagicMock()
    mock_db_session.query.return_value.filter.return_value.first.return_value = None
    mock_db_session.commit = MagicMock()
    mock_db_session.refresh = MagicMock()

    async def mock_get(*args, **kwargs):
        mock_response = CoroutineMock()
        mock_response.json.return_value = mock_weather_data
        mock_response.raise_for_status = CoroutineMock()
        return mock_response

    with patch('httpx.AsyncClient.get', new=mock_get), \
         patch('services.services.SessionLocal', return_value=mock_db_session):

        user_id = "test_user"
        await fetch_and_store_weather_data(user_id)

        # Ensure data was inserted correctly
        assert mock_db_session.add.called
        assert mock_db_session.commit.called
        assert mock_db_session.refresh.called

