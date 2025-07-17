from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from utils import format_weather_message, get_weather

router = Router()


@router.message(Command("get_weather"))
async def weather(message: Message) -> None:
    weather = await get_weather()
    response = format_weather_message(weather)
    await message.answer(response)
