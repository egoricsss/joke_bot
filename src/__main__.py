import os
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from handlers import joke_router, weather_router, llm_router
from middleware import AllowedOnlyMiddleware
from utils import config, get_weather, format_weather_message, get_joke

sys.path.insert(1, os.path.join(sys.path[0], ".."))


dp = Dispatcher()
bot = Bot(
    token=config.TELEGRAM_API_KEY,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
)


async def send_weather():
    weather = await get_weather()
    text = format_weather_message(weather)
    for uid in config.USERS_IDS:
        await bot.send_message(chat_id=uid, text=text, parse_mode=ParseMode.HTML)


async def send_joke():
    joke = await get_joke()
    text = f"<b>Анекдот для Ярослава:</b>\n{joke.setup}\n{joke.delivery}😂😂😂"
    for uid in config.USERS_IDS:
        await bot.send_message(chat_id=uid, text=text, parse_mode=ParseMode.HTML)


scheduler = AsyncIOScheduler()


async def on_startup(bot: Bot) -> None:
    scheduler.start()
    scheduler.add_job(send_weather, "interval", seconds=10)
    scheduler.add_job(send_weather, "cron", hour=8, minute=0)
    scheduler.add_job(send_joke, "cron", hour=8, minute=0)
    scheduler.add_job(send_weather, "cron", hour=12, minute=0)
    scheduler.add_job(send_weather, "cron", hour=16, minute=0)
    scheduler.add_job(send_weather, "cron", hour=20, minute=0)
    await bot.set_webhook(
        url=f"{config.BASE_WEBHOOK_URL}{config.WEBHOOK_PATH}",
        secret_token=config.WEBHOOK_SECRET,
    )


def main() -> None:
    dp.include_routers(joke_router, weather_router, llm_router)
    dp.message.middleware(AllowedOnlyMiddleware())
    dp.startup.register(on_startup)
    app = web.Application()
    webhook_request_handler = SimpleRequestHandler(
        dispatcher=dp, bot=bot, secret_token=config.WEBHOOK_SECRET
    )
    webhook_request_handler.register(app, path=config.WEBHOOK_PATH)
    setup_application(app, dp, bot=bot)
    web.run_app(app, host=config.WEB_SERVER_HOST, port=config.WEB_SERVER_PORT)


if __name__ == "__main__":
    main()
