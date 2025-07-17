import aiohttp
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import model_validator, BaseModel

__all__ = ["config", "http_request", "WeatherResponseDTM", "JokeDTM"]


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=False
    )

    OPEN_WEATHER_API_KEY: str
    TELEGRAM_API_KEY: str
    CITY_ID: int
    USERS_IDS: str

    @model_validator(mode="after")
    def parse_users_ids(self):
        if isinstance(self.USERS_IDS, str):
            self.USERS_IDS = [int(uid) for uid in self.USERS_IDS.split(",")]
        return self


class Weather(BaseModel):
    id: int
    main: str
    description: str
    icon: str


class Main(BaseModel):
    temp: float
    feels_like: float
    temp_min: float
    temp_max: float
    pressure: int
    humidity: int
    sea_level: int
    grnd_level: int


class Wind(BaseModel):
    speed: float
    deg: int
    gust: float


class Clouds(BaseModel):
    all: int


class Sys(BaseModel):
    country: str
    sunrise: int
    sunset: int


class Coord(BaseModel):
    lon: float
    lat: float


class WeatherResponseDTM(BaseModel):
    coord: Coord
    weather: list[Weather]
    base: str
    main: Main
    visibility: int
    wind: Wind
    clouds: Clouds
    dt: int
    sys: Sys
    timezone: int
    id: int
    name: str
    cod: int


class JokeDTM(BaseModel):
    setup: str
    delivery: str


async def http_request(path: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(path) as response:
            res = await response.text()
            return res


config = Config()
