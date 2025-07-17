import json
from datetime import datetime, timedelta, timezone

from .utils import WeatherResponseDTM, config, http_request

__all__ = ["get_weather", "format_weather_message"]


def format_weather_message(data: WeatherResponseDTM) -> str:
    sunrise = datetime.fromtimestamp(
        data.sys.sunrise, tz=timezone(timedelta(hours=3))
    ).strftime("%H:%M")
    sunset = datetime.fromtimestamp(
        data.sys.sunset, tz=timezone(timedelta(hours=3))
    ).strftime("%H:%M")

    weather_icon = {
        "Clear": "☀️",
        "Clouds": "☁️",
        "Rain": "🌧️",
        "Drizzle": "🌦️",
        "Thunderstorm": "⛈️",
        "Snow": "❄️",
        "Mist": "🌫️",
    }.get(data.weather[0].main, "🌤️")

    return f"""
<b>{data.name}, {data.sys.country}</b>
<i>{data.weather[0].description.capitalize()}</i> {weather_icon}

🌡️ Температура: {data.main.temp:.1f}°C
(feels like {data.main.feels_like:.1f}°C)

🌡️ Min/Max: 
{data.main.temp_min:.1f}°C / {data.main.temp_max:.1f}°C

💧 Влажность: {data.main.humidity}%
🌬️ Ветер: {data.wind.speed} м/с (порывы до {data.wind.gust} м/с)
☁️ Облачность: {data.clouds.all}%

🧭 Давление: {int(data.main.pressure * 0.750062)} мм рт.ст.
👀 Видимость: {data.visibility / 1000} км

🌅 Восход: {sunrise}
🌇 Закат: {sunset}

📍 Координаты: 
{data.coord.lon:.4f}°E, {data.coord.lat:.4f}°N
"""


async def get_weather() -> WeatherResponseDTM:
    weather = await http_request(
        f"https://api.openweathermap.org/data/2.5/weather?id={config.CITY_ID}&appid={config.OPEN_WEATHER_API_KEY}&units={config.UNITS}&lang={config.LANGUAGE}"
    )
    weatherDTM = WeatherResponseDTM.model_validate(json.loads(weather))
    return weatherDTM
