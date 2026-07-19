import os
import requests
from langchain.tools import tool

@tool
def weather_tool(location: str) -> str:
    """Get current weather for a city or location using OpenWeatherMap. Use this when the user asks about temperature, rain, humidity, wind, or weather conditions."""
    print("🌦️ WEATHER TOOL CALLED")
    api_key = os.environ.get("OPENWEATHER_API_KEY")

    if not api_key:
        return "OPENWEATHER_API_KEY is missing. Please set the API key first."

    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": location,
        "appid": api_key,
        "units": "metric"
    }

    try:
        response = requests.get(url, params=params, timeout=20)
        if response.status_code != 200:
            return f"Weather API error: {response.status_code} - {response.text}"

        data = response.json()
        city = data.get("name", location)
        country = data.get("sys", {}).get("country", "")
        weather = data.get("weather", [{}])[0].get("description", "unknown")
        temp = data.get("main", {}).get("temp", "unknown")
        feels_like = data.get("main", {}).get("feels_like", "unknown")
        humidity = data.get("main", {}).get("humidity", "unknown")
        wind_speed = data.get("wind", {}).get("speed", "unknown")

        return (
            f"Current weather in {city}, {country}:\n"
            f"- Condition: {weather}\n"
            f"- Temperature: {temp}°C\n"
            f"- Feels like: {feels_like}°C\n"
            f"- Humidity: {humidity}%\n"
            f"- Wind speed: {wind_speed} m/s"
        )
    except Exception as e:
        return f"Error executing weather request: {e}"
