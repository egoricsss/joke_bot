from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.enums import ParseMode

from utils import get_joke

router = Router()


@router.message(Command("get_joke"))
async def request_joke(message: Message) -> None:
    joke = await get_joke()
    response = f"<b>Анекдот для Ярослава:</b>\n{joke.setup}\n{joke.delivery}😂😂😂"
    await message.answer(response, parse_mode=ParseMode.HTML)
