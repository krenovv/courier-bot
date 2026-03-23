from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession

from bot.handlers import start, trip, car_settings, common, debug

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