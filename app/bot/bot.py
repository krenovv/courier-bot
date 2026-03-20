from aiogram import Bot, Dispatcher, F
from aiogram.client.session.aiohttp import  AiohttpSession
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from app.bot.keyboards import main_keyboard, car_settings_keyboard, car_settings_choice_keyboard
from app.bot.states import AddTrip, CarSettings

from app.utils.validators import (
    validate_distance,
    validate_payment,
    validate_fuel_price,
    validate_fuel_consumption,
    validate_amortization
)

from app.models.defaults import (
    DEFAULT_FUEL_PRICE,
    DEFAULT_CONSUMPTION,
    DEFAULT_AMORTIZATION
)


async def run_bot(token, container, proxy):

    session = AiohttpSession(proxy=proxy) if proxy else AiohttpSession()
    bot = Bot(token=token, session=session)
    dp = Dispatcher()

    trip_service = container.trip_service
    car_settings_service = container.car_settings_service


    @dp.message(Command("start"))
    async def start_handler(message: Message, state: FSMContext):
        await state.clear()
        await message.answer(
            "Выберите действие:",
            reply_markup=main_keyboard
        )


    @dp.message(StateFilter("*"), F.text == "🚘 Добавить поездку")
    async def add_trip_handler(message: Message, state: FSMContext):
        await state.clear()

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


    @dp.message(StateFilter("*"), F.text == "📊 Посмотреть все поездки")
    async def show_trips(message: Message, state: FSMContext):
        await state.clear()
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
                f"Прибыль: {trip.profit:g} ₽ ({trip.profit_per_km:g} ₽/км)\n\n"
            )
        text = "\n".join(lines)
        await message.answer(text, reply_markup=main_keyboard)


    @dp.message(StateFilter("*"), F.text == "⚙️ Настройки автомобиля")
    async def car_settings_menu(message: Message, state: FSMContext):
        await state.clear()

        user_id = message.from_user.id
        settings = car_settings_service.get(user_id)

        if not settings:
            await message.answer(
                "Настройки не заданы.\n"
                "Можем ввести их или использовать средние значения.",
                reply_markup=car_settings_choice_keyboard
            )
        else:
            await send_car_settings(message, settings)


    @dp.message(F.text == "✏️ Ввести новые настройки")
    async def start_manual_car_settings(message: Message, state: FSMContext):
        await state.clear()
        await state.set_state(CarSettings.fuel_price)
        await ask_input(message,"Введите цену топлива (₽/л):")


    @dp.message(F.text == "📊 Установить средние значения")
    async def set_default_settings(message: Message, state: FSMContext):
        await state.clear()

        user_id = message.from_user.id

        settings = car_settings_service.set(
            user_id,
            DEFAULT_FUEL_PRICE,
            DEFAULT_CONSUMPTION,
            DEFAULT_AMORTIZATION
        )

        await send_car_settings(message, settings, "Установлены средние значения:", True)


    @dp.message(
        StateFilter("*"),
        (F.text == "⬅️ Назад") | (F.text.lower() == "отмена")
    )
    async def back_to_main(message: Message, state: FSMContext):
        await state.clear()
        await message.answer("Выберите действие:", reply_markup=main_keyboard)


    @dp.message(F.text == "⛽ Изменить цену топлива")
    async def edit_fuel_price(message: Message, state: FSMContext):
        await state.set_state(CarSettings.edit_fuel_price)
        await ask_input(message, "Введите цену топлива (₽/л):")



    @dp.message(F.text == "🔥 Изменить расход")
    async def edit_consumption(message: Message, state: FSMContext):
        await state.set_state(CarSettings.edit_consumption)
        await ask_input(message, "Введите расход (л/100 км):")


    @dp.message(F.text == "🔧 Изменить амортизацию")
    async def edit_amortization(message: Message, state: FSMContext):
        await state.set_state(CarSettings.edit_amortization)
        await ask_input(message,"Введите амортизацию (₽/км):")


    @dp.message(AddTrip.distance)
    async def process_distance(message: Message, state: FSMContext):
        try:
            distance = validate_distance(message.text)
        except ValueError as e:
            await message.answer(str(e))
            return

        await state.update_data(distance=distance)
        await state.set_state(AddTrip.payment)
        await ask_input(message,"Введите оплату за поездку (₽):")


    @dp.message(AddTrip.payment)
    async def process_payment(message: Message, state: FSMContext):
        try:
            payment = validate_payment(message.text)
        except ValueError as e:
            await message.answer(str(e))
            return

        data = await state.get_data()
        distance = data["distance"]
        user_id = message.from_user.id

        try:
            result = trip_service.create_trip(user_id, distance, payment)
        except ValueError as e:
            await message.answer(str(e), reply_markup=main_keyboard)
            return

        await message.answer(
            f"✅ Поездка добавлена\n"
            f"💰 Чистый доход: {result.profit} ₽\n\n",
            reply_markup=main_keyboard
        )

        await state.clear()

    @dp.message(CarSettings.edit_fuel_price)
    async def process_edit_fuel_price(message: Message, state: FSMContext):
        try:
            value = validate_fuel_price(message.text)
        except ValueError as e:
            await message.answer(str(e))
            return

        await update_single_setting(message, state, "fuel_price", value)

    @dp.message(CarSettings.edit_consumption)
    async def process_edit_consumption(message: Message, state: FSMContext):
        try:
            value = validate_fuel_consumption(message.text)
        except ValueError as e:
            await message.answer(str(e))
            return

        await update_single_setting(message, state, "consumption", value)

    @dp.message(CarSettings.edit_amortization)
    async def process_edit_amortization(message: Message, state: FSMContext):
        try:
            value = validate_amortization(message.text)
        except ValueError as e:
            await message.answer(str(e))
            return

        await update_single_setting(message, state, "amortization", value)


    @dp.message(CarSettings.fuel_price)
    async def process_fuel_price(message: Message, state: FSMContext):
        try:
            fuel_price = validate_fuel_price(message.text)
        except ValueError as e:
            await message.answer(str(e))
            return

        await state.update_data(fuel_price=fuel_price)
        await state.set_state(CarSettings.consumption)
        await ask_input(message, "Введите расход (л/100 км):")


    @dp.message(CarSettings.consumption)
    async def process_consumption(message: Message, state: FSMContext):
        try:
            consumption = validate_fuel_consumption(message.text)
        except ValueError as e:
            await message.answer(str(e))
            return

        await state.update_data(consumption=consumption)
        await state.set_state(CarSettings.amortization)
        await ask_input(message,"Введите амортизацию автомобиля (₽/км):")


    @dp.message(CarSettings.amortization)
    async def process_amortization(message: Message, state: FSMContext):
        try:
            amortization = validate_amortization(message.text)
        except ValueError as e:
            await message.answer(str(e))
            return

        await state.update_data(amortization=amortization)
        await save_full_settings(message, state)


    async def send_car_settings(
            message: Message,
            settings,
            text="Текущие настройки:",
            show_warning: bool = False
    ):
        warn = ""
        if show_warning:
            warn = "\n\n⚠️ Значения приблизительные.\nДля точных расчетов лучше задать свои."

        await message.answer(
            f"{text}\n\n"
            f"⛽ Топливо: {settings.fuel_price_per_l:g} ₽/л\n"
            f"🔥 Расход: {settings.fuel_consumption_per_100km:g} л/100 км\n"
            f"🛠 Амортизация: {settings.amortization_per_km:g} ₽/км"
            f"{warn}",
            reply_markup=car_settings_keyboard
        )


    @dp.message(F.text == "Удалить поездки")
    async def debug_reset_trips(message: Message, state: FSMContext):
        await state.clear()
        user_id = message.from_user.id

        trip_service.delete_all_trips(user_id)

        await message.answer("Все поездки удалены", reply_markup=main_keyboard)


    @dp.message(F.text == "Удалить настройки")
    async def debug_reset_settings(message: Message, state: FSMContext):
        await state.clear()
        user_id = message.from_user.id

        car_settings_service.delete(user_id)

        await message.answer("Настройки автомобиля удалены", reply_markup=main_keyboard)


    async def update_single_setting(message, state, field: str, value: float):
        user_id = message.from_user.id
        current = car_settings_service.get(user_id)

        # noinspection PyDictCreation
        data = {
            "fuel_price": current.fuel_price_per_l,
            "consumption": current.fuel_consumption_per_100km,
            "amortization": current.amortization_per_km,
        }

        data[field] = value

        settings = car_settings_service.set(
            user_id,
            data["fuel_price"],
            data["consumption"],
            data["amortization"]
        )

        await send_car_settings(message, settings, "Настройки обновлены:")
        await state.clear()


    async def save_full_settings(message: Message, state: FSMContext):
        data = await state.get_data()
        user_id = message.from_user.id

        settings = car_settings_service.set(
            user_id,
            data["fuel_price"],
            data["consumption"],
            data["amortization"]
        )

        await send_car_settings(message, settings, "Настройки обновлены:")
        await state.clear()


    async def ask_input(message: Message, text: str):
        full_text = (
            f"{text}\n\n"
            "<i>или «отмена» для выхода</i>"
        )

        await message.answer(
            full_text,
            parse_mode="HTML",
            reply_markup=ReplyKeyboardRemove()
        )



    await dp.start_polling(bot)