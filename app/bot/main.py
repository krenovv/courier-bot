from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from aiohttp import web

from app.bot.handlers import start, common, trip, car_settings, debug
import sqlite3
import os


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

    await dp.start_polling(bot)


async def health(request):
    try:
        db_path = os.getenv("DB_PATH", "db.sqlite3")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        cursor.fetchone()
        conn.close()
        return web.Response(text="ok")
    except Exception as e:
        print(f"Health check failed: {e}")  # для отладки
        return web.Response(status=500, text="db error")


async def start_health_server():
    app = web.Application()
    app.router.add_get("/healthz", health)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 8080)
    await site.start()
    print("Health server started on port 8080")