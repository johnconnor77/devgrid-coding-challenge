import pytest
import httpx
import os

# Load environment variables
OPEN_WEATHER_API_KEY = os.getenv("OPEN_WEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


@pytest.mark.asyncio
async def test_weather_api():
    city_id = 3439525
    async with httpx.AsyncClient() as client:
        response = await client.get(
            BASE_URL,
            params={"id": city_id, "appid": OPEN_WEATHER_API_KEY, "units": "metric"}
        )

    assert response.status_code == 200
    data = response.json()

    # Checking response body
    assert "main" in data
    assert "temp" in data["main"]
    assert "humidity" in data["main"]
    assert "id" in data
    assert data["id"] == city_id

    print(f"City ID: {data['id']}")
    print(f"Temperature: {data['main']['temp']} °C")
    print(f"Humidity: {data['main']['humidity']} %")


if __name__ == "__main__":
    pytest.main()