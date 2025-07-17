from .get_joke import router as joke_router
from .get_weather import router as weather_router
from .llm_request import router as llm_router

__all__ = ["joke_router", "weather_router", "llm_router"]
