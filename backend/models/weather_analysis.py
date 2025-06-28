from pydantic import BaseModel

class Location(BaseModel):
    city: str
    country: str = "Unknown"

class CurrentWeatherSummary(BaseModel):
    temp: float
    condition: str
    humidity: float
    windSpeed: float
    feelsLike: float

class HourlyForecastSummary(BaseModel):
    time: str
    temp: float
    condition: str
    precipProbability: int

class ActivityRecommendation(BaseModel):
    timeSlot: str
    score: float
    reason: str

class ActivityRecommendationsResponse(BaseModel):
    location: Location
    current: CurrentWeatherSummary
    hourlyForecast: list[HourlyForecastSummary]
    activityRecommendations: list[ActivityRecommendation]