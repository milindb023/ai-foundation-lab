import requests
from typing import Any
from ..config.settings import get_openweather_key
from ..schemas.weather import WeatherToolInput

def get_current_weather(location: str) -> dict[str, Any]:
    """
    Calls the OpenWeather API to retrieve the current weather information for a given city.
    """
    url = "https://api.openweathermap.org/data/2.5/weather"
    api_key = get_openweather_key()

    response = requests.get(
        url,
        params={
            "q": location,
            "appid": api_key,
            "units": "metric"
        },
        timeout=20
    )

    response.raise_for_status()
    data = response.json()

    return {
        "location": data["name"],
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "wind_speed": data["wind"]["speed"],
        "condition": data["weather"][0]["description"]
    }

# Tool metadata exposed to the LLM (using the Pydantic schema)
weather_tool_definition = {
    "type": "function",
    "function": {
        "name": "get_current_weather",
        "description": (
            "Get the current temperature, humidity, wind speed, "
            "and weather condition for a city using OpenWeather."
        ),
        "parameters": WeatherToolInput.model_json_schema(),
    },
}
