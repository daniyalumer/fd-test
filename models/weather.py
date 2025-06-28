from pydantic import BaseModel

class CurrentWeather(BaseModel):
    temperature: float
    condition: str
    humidity: float
    wind_speed: float
    feels_like: float
    precipitation_probability: int  

class HourlyForecast(BaseModel):
    time: str
    temperature_2m: float
    condition: str
    precipitation_probability: int
    feels_like: float

class CurrentWeatherResponse(BaseModel):
    city: str
    current_weather: CurrentWeather

class WeatherForecastResponse(BaseModel):
    city: str
    hourly_forecast: list[HourlyForecast]