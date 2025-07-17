from utils import http_request, config, WeatherResponseDTM
import json

__all__ = ["get_weather"]


async def get_weather() -> WeatherResponseDTM:
    weather = await http_request(
        f"https://api.openweathermap.org/data/2.5/weather?id={config.CITY_ID}&appid={config.OPEN_WEATHER_API_KEY}&units=metric&lang=RU"
    )
    weatherDTM = WeatherResponseDTM.model_validate(json.loads(weather))
    return weatherDTM
