import os
from dotenv import load_dotenv
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message

from main import trip_service
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Добавить поездку")],
        [KeyboardButton(text="Посмотреть все поездки")],
        [KeyboardButton(text="Изменить параметры автомобиля")],
    ],
    resize_keyboard=True
)


@dp.message(Command("start"))
async def start_handler(message: Message):
    await message.answer(
        "Выбери действие:",
        reply_markup=keyboard
    )


@dp.message(F.text == "Добавить поездку")
async def add_trip_handler(message: Message):

    await message.answer("Введи параметры поездки в формате:\n"
                         "<пробег (км)> <оплата>\n"
                         "Пример: 10.3 750"
                         )

@dp.message(F.text == "Посмотреть все поездки")
async def show_trips(message: Message):
    trips = trip_service.get_all_trips_with_results()

    text = ""

    if not trips:
        await message.answer("Поездок пока нет.")
        return

    for i, (trip, result) in enumerate(trips, start=1):

        text += (
            f"Поездка {i} от {trip.created_at.strftime('%d.%m.%Y %H:%M:%S')}\n"
            f"Пробег: {trip.distance_km:g} км\n"
            f"Потрачено топлива: {result.fuel_used:g} л ({result.fuel_cost} ₽)\n"
            f"Стоимость амортизации: {result.amortization} ₽\n"
            f"Оплата за заказ: {trip.payment} ₽\n"
            f"Чистый доход: {result.profit} ₽\n\n"
        )

    await message.answer(text)

@dp.message()
async def trip_input_handler(message: Message):

    text = message.text.strip()
    parts = text.split()

    if len(parts) != 2:
        await message.answer("Используй формат: <км> <оплата>\n"
                             "Пример: 10.3 750")
        return

    try:
        distance_km = float(parts[0])
        payment = int(parts[1])
    except ValueError:
        await message.answer("Дистанция и оплата должны быть числами\n"
                             "Пример: 10.3 750")
        return

    result = trip_service.add_trip(distance_km, payment)

    await message.answer(
        f"Поездка добавлена\n\n"
        f"Расход топлива: {result.fuel_used} л\n"
        f"Стоимость топлива: {result.fuel_cost} ₽\n"
        f"Амортизация: {result.amortization} ₽\n"
        f"Чистый доход: {result.profit} ₽"
    )

async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())