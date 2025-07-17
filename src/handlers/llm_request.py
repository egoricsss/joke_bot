from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router()


@router.message(~Command())
async def echo(message: Message):
    await message.answer(message.text)
