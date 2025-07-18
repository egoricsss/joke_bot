import os
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import ErrorEvent
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio

from handlers import joke_router, llm_router, weather_router
from middleware import AllowedOnlyMiddleware
from utils import config, format_weather_message, get_joke, get_weather

sys.path.insert(1, os.path.join(sys.path[0], ".."))


dp = Dispatcher()
bot = Bot(
    token=config.TELEGRAM_API_KEY,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
)


@dp.error()
async def handle_errors(event: ErrorEvent) -> None:
    error_text = f"⚠️ Произошла ошибка:\n\n{event.exception}"
    await bot.send_message(
        chat_id=config.ADMIN_ID,
        text=f"<b>🚨 Ошибка в боте:</b>\n<pre>{error_text}</pre>",
        parse_mode="HTML",
    )


async def send_weather() -> None:
    try:
        weather = await get_weather()
        text = format_weather_message(weather)
        for uid in config.USERS_IDS:
            try:
                await bot.send_message(
                    chat_id=uid, text=text, parse_mode=ParseMode.HTML
                )
            except Exception as e:
                await bot.send_message(
                    chat_id=config.ADMIN_ID,
                    text=f"Ошибка при отправке погоды:\n<code>{e}</code>",
                )
    except Exception as e:
        await bot.send_message(
            chat_id=config.ADMIN_ID,
            text=f"Ошибка при получении погоды:\n<code>{e}</code>",
        )


async def send_joke() -> None:
    try:
        joke = await get_joke()
        text = f"<b>Анекдот для Ярослава:</b>\n{joke.setup}\n{joke.delivery}😂😂😂"
        for uid in config.USERS_IDS:
            try:
                await bot.send_message(
                    chat_id=uid, text=text, parse_mode=ParseMode.HTML
                )
            except Exception as e:
                await bot.send_message(
                    chat_id=config.ADMIN_ID,
                    text=f"Ошибка при отправке анекдота:\n<code>{e}</code>",
                )
    except Exception as e:
        await bot.send_message(
            chat_id=config.ADMIN_ID,
            text=f"Ошибка при получении анекдота:\n<code>{e}</code>",
        )


scheduler = AsyncIOScheduler()


async def on_startup(bot: Bot) -> None:
    scheduler.start()
    scheduler.add_job(send_weather, "cron", hour=8, minute=0)
    scheduler.add_job(send_joke, "cron", hour=8, minute=0)
    scheduler.add_job(send_weather, "cron", hour=12, minute=0)
    scheduler.add_job(send_weather, "cron", hour=16, minute=0)
    scheduler.add_job(send_weather, "cron", hour=20, minute=0)
    await bot.set_webhook(
        url=f"{config.BASE_WEBHOOK_URL}{config.WEBHOOK_PATH}",
        secret_token=config.WEBHOOK_SECRET,
    )


async def main() -> None:
    await bot.set_my_commands(
        [
            {"command": "get_weather", "description": "Узнать погоду сейчас"},
            {"command": "get_joke", "description": "Запросить анекдот"},
        ]
    )

    dp.include_routers(joke_router, weather_router, llm_router)
    dp.message.middleware(AllowedOnlyMiddleware())
    dp.startup.register(on_startup)

    # Настройка веб-приложения
    app = web.Application()
    webhook_request_handler = SimpleRequestHandler(
        dispatcher=dp, bot=bot, secret_token=config.WEBHOOK_SECRET
    )
    webhook_request_handler.register(app, path=config.WEBHOOK_PATH)
    setup_application(app, dp, bot=bot)

    # Запуск веб-сервера
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host=config.WEB_SERVER_HOST, port=config.WEB_SERVER_PORT)
    await site.start()

    print(f"🚀 Бот запущен на http://{config.WEB_SERVER_HOST}:{config.WEB_SERVER_PORT}")

    try:
        # Удерживаем выполнение, пока не будет остановлено
        await asyncio.Event().wait()
    except asyncio.CancelledError:
        print("🛑 Остановка бота...")
    finally:
        # Закрываем ресурсы в любом случае
        print("🧹 Закрываем ресурсы...")
        await bot.session.close()  # Закрываем сессию бота
        await runner.cleanup()  # Очищаем веб-сервер
        scheduler.shutdown()  # Останавливаем планировщик


if __name__ == "__main__":
    asyncio.run(main())
