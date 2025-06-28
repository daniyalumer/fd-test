import requests
from models.weather import (
    CurrentWeatherResponse,
    WeatherForecastResponse,
    Location,
    CurrentWeather,
    HourlyForecast,
)

# Dummy city-to-coordinates mapping for demonstration
CITY_COORDS = {
    "berlin": (52.52, 13.41),
    "london": (51.51, -0.13),
    "paris": (48.85, 2.35),
}

def city_to_coordinates(city: str) -> tuple:
    # Simple mapping; in production, use a geocoding API
    return CITY_COORDS.get(city.lower(), (52.52, 13.41))

def get_weather_data(city: str) -> dict:
    latitude, longitude = city_to_coordinates(city)
    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={latitude}&longitude={longitude}"
        f"&current=temperature_2m,weather_code,humidity_2m,wind_speed_10m"
    )
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch weather data for {city}. Status code: {response.status_code}")
    return response.json()

def get_weather_forecast(city: str) -> dict:
    latitude, longitude = city_to_coordinates(city)
    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={latitude}&longitude={longitude}"
        "&hourly=temperature_2m,precipitation_probability,wind_speed_10m,weather_code"
    )
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch weather forecast for {city}. Status code: {response.status_code}")
    return response.json()

def transform_weather_data(city: str, raw: dict) -> CurrentWeatherResponse:
    current = raw.get("current", {})
    # Fallbacks for missing data
    temperature = current.get("temperature_2m", 0.0)
    humidity = current.get("humidity_2m", 50.0)
    wind_speed = current.get("wind_speed_10m", 0.0)
    weather_code = current.get("weather_code", 0)
    # Simple feels_like approximation
    feels_like = temperature - (wind_speed * 0.7)

    # Map weather_code to a string condition (simplified)
    condition = str(weather_code)

    location = Location(city=city.title(), country="Unknown")
    current_weather = CurrentWeather(
        temperature=temperature,
        condition=condition,
        humidity=humidity,
        wind_speed=wind_speed,
        feels_like=feels_like,
    )
    return CurrentWeatherResponse(location=location, current_weather=current_weather)

def transform_forecast_data(city: str, raw: dict) -> WeatherForecastResponse:
    hourly = raw.get("hourly", {})
    times = hourly.get("time", [])
    temps = hourly.get("temperature_2m", [])
    wind_speeds = hourly.get("wind_speed_10m", [])
    precip_probs = hourly.get("precipitation_probability", [])
    weather_codes = hourly.get("weather_code", [])

    hourly_forecast = [
        HourlyForecast(
            time=times[i],
            temperature_2m=temps[i] if i < len(temps) else 0.0,
            condition=str(weather_codes[i]) if i < len(weather_codes) else "0",
            precipitation_probability=precip_probs[i] if i < len(precip_probs) else 0,
            feels_like=(temps[i] if i < len(temps) else 0.0) - ((wind_speeds[i] if i < len(wind_speeds) else 0.0) * 0.7),
        )
        for i in range(min(len(times), 24))
    ]

    location = Location(city=city.title(), country="Unknown")
    return WeatherForecastResponse(location=location, hourly_forecast=hourly_forecast)