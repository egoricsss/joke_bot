from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import Message

from utils import config

__all__ = ["AllowedOnlyMiddleware"]


class AllowedOnlyMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: dict[str, Any],
    ) -> Any:
        user_id = event.from_user.id
        if user_id in config.USERS_IDS:
            return await handler(event, data)
        return None
