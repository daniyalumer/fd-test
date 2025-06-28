from fastapi import APIRouter, HTTPException
from models.weather import (
    CurrentWeatherResponse,
    WeatherForecastResponse,
)
from services.weather import (
    get_weather_data,
    get_weather_forecast,
    transform_weather_data,
    transform_forecast_data,
)

router = APIRouter()

@router.get("/weather/{city}", response_model=CurrentWeatherResponse)
def get_weather(city: str):
    try:
        raw = get_weather_data(city)
        data = transform_weather_data(city, raw)
        return data
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/forecast/{city}", response_model=WeatherForecastResponse)
def get_forecast(city: str):
    try:
        raw = get_weather_forecast(city)
        data = transform_forecast_data(city, raw)
        return data
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))