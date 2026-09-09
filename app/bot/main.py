import asyncio
import logging
import os
import sqlite3

from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.exceptions import TelegramNetworkError

from app.bot.handlers import start, common, trip, car_settings, debug


logger = logging.getLogger(__name__)


async def run_bot(token, container, proxy):
    session = AiohttpSession(proxy=proxy) if proxy else AiohttpSession()
    bot = Bot(token=token, session=session)
    dp = Dispatcher()

    dp["trip_service"] = container.trip_service
    dp["car_settings_service"] = container.car_settings_service

    dp.include_router(start.router)
    dp.include_router(common.router)
    dp.include_router(trip.router)
    dp.include_router(car_settings.router)
    dp.include_router(debug.router)

    while True:
        try:
            logger.info("Starting polling...")
            await dp.start_polling(bot)
            logger.warning(
                "Polling stopped. Restarting in 10 seconds..."
            )

        except TelegramNetworkError as e:
            logger.warning(
                "Telegram недоступен: %s. Повтор через 10 секунд.",
                e,
            )

        except asyncio.CancelledError:
            logger.info("Polling cancelled.")
            raise

        except Exception:
            logger.exception(
                "Неожиданная ошибка в polling. Повтор через 10 секунд."
            )

        await asyncio.sleep(10)


async def health(request):
    try:
        db_path = os.getenv("DB_PATH", "db.sqlite3")

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        cursor.fetchone()
        conn.close()

        return web.Response(text="ok")

    except Exception:
        logger.exception("Health check failed")
        return web.Response(status=500, text="db error")


async def start_health_server():
    app = web.Application()
    app.router.add_get("/healthz", health)

    runner = web.AppRunner(app)
    await runner.setup()

    site = web.TCPSite(runner, "0.0.0.0", 8080)
    await site.start()

    logger.info("Health server started on port 8080")