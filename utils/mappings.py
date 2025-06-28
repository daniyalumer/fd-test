WMO_CODE_MAP = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Drizzle: Light",
    53: "Drizzle: Moderate",
    55: "Drizzle: Dense",
    56: "Freezing Drizzle: Light",
    57: "Freezing Drizzle: Dense",
    61: "Rain: Slight",
    63: "Rain: Moderate",
    65: "Rain: Heavy",
    66: "Freezing Rain: Light",
    67: "Freezing Rain: Heavy",
    71: "Snow fall: Slight",
    73: "Snow fall: Moderate",
    75: "Snow fall: Heavy",
    77: "Snow grains",
    80: "Rain showers: Slight",
    81: "Rain showers: Moderate",
    82: "Rain showers: Violent",
    85: "Snow showers: Slight",
    86: "Snow showers: Heavy",
    95: "Thunderstorm: Slight or moderate",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail",
}

def wmo_code_to_string(code: int) -> str:
    return WMO_CODE_MAP.get(code, "Unknown")

# Dummy city-to-coordinates mapping for demonstration
CITY_COORDS = {
    "berlin": (52.52, 13.41),
    "london": (51.51, -0.13),
    "paris": (48.85, 2.35),
}

def city_to_coordinates(city: str) -> tuple:
    # Simple mapping; in production, use a geocoding API
    return CITY_COORDS.get(city.lower(), (52.52, 13.41))