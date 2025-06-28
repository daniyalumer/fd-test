# Weather Analysis API

This project provides a FastAPI backend for weather analysis and activity recommendations based on historical and current weather data.

## Features

- Fetches current weather and past 7 days of hourly weather data for a city
- Maps weather codes to human-readable conditions
- Detects temperature anomalies
- Recommends optimal outdoor activity times based on temperature, precipitation probability, humidity, and wind speed
- Returns current weather summary and 24-hour forecast

## Endpoints

- `GET /weather/analysis/{city}`  
  Returns current weather, 7-day hourly forecast, and activity recommendations for the specified city.

- `GET /weather/{city}`  
  Returns only the current weather summary for the specified city.

- `GET /forecast/{city}`  
  Returns the 24-hour hourly weather forecast for the specified city.

## Project Structure

```
/backend   # (recommended future structure)
  /controllers
  /models
  /services
  /utils
  main.py
/frontend  # (to be added)
README.md
```

## Setup

1. Install dependencies using pipenv:
    ```bash
    pipenv install
    ```

2. Run the FastAPI server:
    ```bash
    pipenv run uvicorn main:app --reload
    ```

## To Do

- Add Angular frontend in `/frontend`
- Improve documentation and usage examples

---
*This README will be updated as