from fastapi import APIRouter
from controllers import weather, weather_analysis

router = APIRouter()

router.include_router(
    weather.router,
    prefix="/api")

router.include_router(
    weather_analysis.router,
    prefix="/api")