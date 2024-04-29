from typing import Optional

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    weather_data = {
        "coord": {
            "lon": -0.1257,
            "lat": 51.5085
        },
        "weather": [
            {
                "id": 803,
                "main": "Clouds",
                "description": "broken clouds",
                "icon": "04n"
            }
        ],
        "base": "stations",
        "main": {
            "temp": 285.48,
            "feels_like": 284.44,
            "temp_min": 283.81,
            "temp_max": 286.23,
            "pressure": 1016,
            "humidity": 64
        },
        "visibility": 10000,
        "wind": {
            "speed": 3.09,
            "deg": 170
        },
        "clouds": {
            "all": 53
        },
        "dt": 1714419471,
        "sys": {
            "type": 2,
            "id": 2091269,
            "country": "GB",
            "sunrise": 1714365321,
            "sunset": 1714418402
        },
        "timezone": 3600,
        "id": 2643743,
        "name": "London",
        "cod": 200
    }

    return weather_data