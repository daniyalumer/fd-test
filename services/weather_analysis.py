import numpy as np
import requests
from datetime import datetime, timedelta
from typing import List
from models.weather_analysis import (
    ActivityRecommendation,
    ActivityRecommendationsResponse,
    Location,
    CurrentWeatherSummary,
    HourlyForecastSummary,
)
from services.weather import (
    get_weather_data,
)
from utils.mappings import wmo_code_to_string
from utils.mappings import city_to_coordinates, wmo_code_to_string

def get_past_7_days_hourly_weather(city: str) -> dict:
    latitude, longitude = city_to_coordinates(city)
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=6)  # last 7 days including today

    # Using the archive API to get historical weather data
    url = (
        f"https://archive-api.open-meteo.com/v1/archive"
        f"?latitude={latitude}&longitude={longitude}"
        f"&start_date={start_date}&end_date={end_date}"
        f"&hourly=temperature_2m,precipitation_probability,wind_speed_10m,weather_code,relative_humidity_2m"
        f"&timezone=auto"
    )

    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Failed to fetch historical weather data")

    return response.json()

def detect_temperature_anomalies(hourly_temps: List[float]) -> List[int]:
    avg = np.mean(hourly_temps)
    std = np.std(hourly_temps)
    anomalies = []
    for idx, temp in enumerate(hourly_temps):
        if abs(temp - avg) > std * 2:
            anomalies.append(idx)
    return anomalies

def recommend_activity_times(hourly_data: list[dict]) -> list[ActivityRecommendation]:
    recommendations = []
    for slot in hourly_data:
        temp = slot["temp"]
        precip = slot["precipProbability"]
        humidity = slot["humidity"]
        wind = slot["windSpeed"]
        time = slot["time"]

        score = 0
        reason = []

        if 15 <= temp <= 25:
            score += 4
            reason.append("Comfortable temperature")
        elif 10 <= temp < 15 or 25 < temp <= 28:
            score += 2
            reason.append("Acceptable temperature")
        else:
            reason.append("Temperature not ideal")

        if precip < 20:
            score += 3
            reason.append("Low chance of rain")
        else:
            reason.append("Possible rain")

        if 30 <= humidity <= 70:
            score += 2
            reason.append("Comfortable humidity")
        elif humidity < 30 or humidity > 80:
            reason.append("Uncomfortable humidity")

        if wind < 15:
            score += 1
            reason.append("Low wind")
        else:
            reason.append("Windy")

        if score >= 7:
            recommendations.append(
                ActivityRecommendation(
                    timeSlot=time,
                    score=score,
                    reason=", ".join(reason),
                )
            )
    recommendations.sort(key=lambda x: x.score, reverse=True)
    return recommendations[:5]

def analyze_weather_patterns(city: str) -> ActivityRecommendationsResponse:
    # Fetch current weather and past 7 days hourly data
    current_raw = get_weather_data(city)
    past_raw = get_past_7_days_hourly_weather(city)

    # Prepare location
    location = Location(city=city.title(), country="Unknown")

    # Prepare current summary
    current = current_raw.get("current", {})
    weather_code = current.get("weather_code", 0)
    current_summary = CurrentWeatherSummary(
        temp=current.get("temperature_2m", 0.0),
        condition=wmo_code_to_string(weather_code),
        humidity=current.get("relative_humidity_2m", 50.0),
        windSpeed=current.get("wind_speed_10m", 0.0),
        feelsLike=round(current.get("temperature_2m", 0.0) - (current.get("wind_speed_10m", 0.0) * 0.7), 1),
    )

    # Prepare hourly forecast summaries for the last 24 hours (for recommendations)
    hourly = past_raw.get("hourly", {})
    times = hourly.get("time", [])
    temps = hourly.get("temperature_2m", [])
    precip_probs = hourly.get("precipitation_probability", [])
    humidity = hourly.get("relative_humidity_2m", [])
    wind_speeds = hourly.get("wind_speed_10m", [])
    weather_codes = hourly.get("weather_code", [0] * len(times))

    hourly_data = [
        {
            "time": times[i],
            "temp": float(temps[i]) if i < len(temps) and temps[i] is not None else 0.0,
            "condition": wmo_code_to_string(weather_codes[i]) if i < len(weather_codes) and weather_codes[i] is not None else "Unknown",
            "precipProbability": int(precip_probs[i]) if i < len(precip_probs) and precip_probs[i] is not None else 0,
            "humidity": float(humidity[i]) if i < len(humidity) and humidity[i] is not None else 0.0,
            "windSpeed": float(wind_speeds[i]) if i < len(wind_speeds) and wind_speeds[i] is not None else 0.0,
        }
        for i in range(len(times))
    ]

    # Detect anomalies (not used in recommendations, but could be added)
    anomaly_indices = detect_temperature_anomalies([float(t) if t is not None else 0.0 for t in temps])

    # Filter out anomaly slots from hourly_data
    filtered_hourly_data = [
        slot for idx, slot in enumerate(hourly_data) if idx not in anomaly_indices
    ]

    # Pass this to your recommendation function
    activity_recs = recommend_activity_times(filtered_hourly_data)

    hourly_forecast = [
        HourlyForecastSummary(
            time=times[i],
            temp=float(temps[i]) if i < len(temps) and temps[i] is not None else 0.0,
            condition=wmo_code_to_string(weather_codes[i]) if i < len(weather_codes) and weather_codes[i] is not None else "Unknown",
            precipProbability=int(precip_probs[i]) if i < len(precip_probs) and precip_probs[i] is not None else 0,
        )
        for i in range(len(times))
    ]

    return ActivityRecommendationsResponse(
        location=location,
        current=current_summary,
        hourlyForecast=hourly_forecast,
        activityRecommendations=activity_recs,
    )