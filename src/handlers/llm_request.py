from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import and_f

router = Router()


@router.message()
async def echo(message: Message):
    await message.answer(message.text)
