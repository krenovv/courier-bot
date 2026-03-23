from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from app.bot.states import AddTrip
from app.bot.keyboards import main_keyboard, car_settings_choice_keyboard
from app.utils.validators import validate_distance, validate_payment
from app.bot.services.ui_helpers import ask_input

router = Router()

@router.message(F.text == "🚘 Добавить поездку")
async def add_trip_handler(message: Message, state: FSMContext, **data):
    await state.clear()


    car_settings_service = data["car_settings_service"]
    user_id = message.from_user.id
    settings = car_settings_service.get(user_id)

    if not settings:
        await message.answer(
                "Не заданы настройки автомобиля.\n"
                "Можем ввести их или использовать средние значения.",
                reply_markup=car_settings_choice_keyboard
            )
        return

    await state.set_state(AddTrip.distance)
    await ask_input(message, "Введите пробег за поездку (км):")


@router.message(AddTrip.distance)
async def process_distance(message: Message, state: FSMContext):
    try:
        distance = validate_distance(message.text)
    except ValueError as e:
        await message.answer(str(e))
        return

    await state.update_data(distance=distance)
    await state.set_state(AddTrip.payment)
    await ask_input(message, "Введите оплату за поездку (₽):")


@router.message(AddTrip.payment)
async def process_payment(message: Message, state: FSMContext, **data):
    trip_service = data["trip_service"]

    try:
        payment = validate_payment(message.text)
    except ValueError as e:
        await message.answer(str(e))
        return

    data = await state.get_data()

    try:
        result = trip_service.create_trip(
            message.from_user.id,
            data["distance"],
            payment
        )
    except ValueError as e:
        await message.answer(str(e), reply_markup=main_keyboard)
        return

    await message.answer(
        f"✅ Поездка добавлена\n"
        f"💰 Чистый доход: {result.profit} ₽\n\n",
        reply_markup=main_keyboard
    )

    await state.clear()


@router.message(F.text == "📊 Посмотреть все поездки")
async def show_trips(message: Message, state: FSMContext, **data):
    await state.clear()

    trip_service = data["trip_service"]
    user_id = message.from_user.id

    trips = trip_service.get_all_trips(user_id)

    if not trips:
        await message.answer("Поездок пока нет.", reply_markup=main_keyboard)
        return

    lines = []

    for i, trip in enumerate(trips, start=1):
        lines.append(
            f"Поездка {i} от {trip.created_at.strftime('%d.%m.%Y %H:%M:%S')}\n"
            f"Пробег: {trip.distance_km:g} км\n"
            f"Оплата: {trip.payment} ₽\n"
            f"Расходы: {trip.total_expenses:g} ₽\n"
            f"Прибыль: {trip.profit:g} ₽ ({trip.profit_per_km:g} ₽/км)\n"
        )

    text = "\n".join(lines)

    await message.answer(text, reply_markup=main_keyboard)