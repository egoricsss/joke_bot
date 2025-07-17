from aiogram import F, Router
from aiogram.filters import and_f
from aiogram.types import Message

router = Router()


@router.message()
async def echo(message: Message):
    await message.answer(message.text)
