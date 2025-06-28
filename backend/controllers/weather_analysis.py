from fastapi import APIRouter, HTTPException
from models.weather_analysis import ActivityRecommendationsResponse
from services.weather_analysis import analyze_weather_patterns

router = APIRouter()

@router.get("/weather/analysis/{city}", response_model=ActivityRecommendationsResponse)
def weather_pattern_analysis(city: str):
    """
    Analyze weather patterns and recommend optimal outdoor activity times for a city.
    """
    try:
        result = analyze_weather_patterns(city)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))