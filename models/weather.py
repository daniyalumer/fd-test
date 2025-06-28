from pydantic import BaseModel

class Location(BaseModel):
    city: str
    country: str = "Unknown"  

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
    location: Location
    current_weather: CurrentWeather

class WeatherForecastResponse(BaseModel):
    location: Location
    hourly_forecast: list[HourlyForecast]