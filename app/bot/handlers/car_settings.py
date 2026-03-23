from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from app.bot.states import CarSettings
from app.bot.services.ui_helpers import ask_input, send_car_settings

from app.bot.keyboards import car_settings_choice_keyboard

from app.models.defaults import (
    DEFAULT_FUEL_PRICE,
    DEFAULT_CONSUMPTION,
    DEFAULT_AMORTIZATION
)

from app.utils.validators import (
    validate_fuel_price,
    validate_fuel_consumption,
    validate_amortization
)


router = Router()


# =============
# Меню настроек
# =============


@router.message(F.text == "⚙️ Настройки автомобиля")
async def car_settings_menu(message: Message, state: FSMContext, **data):
    await state.clear()

    car_settings_service = data["car_settings_service"]
    user_id = message.from_user.id
    settings = car_settings_service.get(user_id)

    if not settings:
        await message.answer(
            "Настройки автомобиля не заданы.\n"
            "Можем ввести их или использовать средние значения.",
            reply_markup=car_settings_choice_keyboard
        )
    else:
        await send_car_settings(message, settings)


# =======================
# Выбор способа настройки
# =======================

@router.message(F.text == "✏️ Ввести новые настройки")
async def start_manual_settings(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(CarSettings.fuel_price)
    await ask_input(message, "Введите цену топлива (₽/л):")


@router.message(F.text == "📊 Установить средние значения")
async def set_default_settings(message: Message, state: FSMContext, **data):
    await state.clear()

    car_settings_service = data["car_settings_service"]
    user_id = message.from_user.id

    settings = car_settings_service.set(
        user_id,
        DEFAULT_FUEL_PRICE,
        DEFAULT_CONSUMPTION,
        DEFAULT_AMORTIZATION
    )

    await send_car_settings(
        message,
        settings,
        text="Установлены средние значения:",
        show_warning=True
    )


# ===================================
# Редактирование отдельных параметров
# ===================================

@router.message(F.text == "⛽ Изменить цену топлива")
async def edit_fuel_price(message: Message, state: FSMContext):
    await state.set_state(CarSettings.edit_fuel_price)
    await ask_input(message, "Введите цену топлива (₽/л):")


@router.message(F.text == "🔥 Изменить расход")
async def edit_consumption(message: Message, state: FSMContext):
    await state.set_state(CarSettings.edit_consumption)
    await ask_input(message, "Введите расход (л/100 км):")


@router.message(F.text == "🔧 Изменить амортизацию")
async def edit_amortization(message: Message, state: FSMContext):
    await state.set_state(CarSettings.edit_amortization)
    await ask_input(message, "Введите амортизацию (₽/км):")


# ========================
# Обработка редактирования
# ========================

@router.message(CarSettings.edit_fuel_price)
async def process_edit_fuel_price(message: Message, state: FSMContext, **data):
    car_settings_service = data["car_settings_service"]

    try:
        value = validate_fuel_price(message.text)
    except ValueError as e:
        await message.answer(str(e))
        return

    await update_single_setting(
        message,
        state,
        car_settings_service,
        "fuel_price",
        value
    )


@router.message(CarSettings.edit_consumption)
async def process_edit_consumption(message: Message, state: FSMContext, **data):
    car_settings_service = data["car_settings_service"]

    try:
        value = validate_fuel_consumption(message.text)
    except ValueError as e:
        await message.answer(str(e))
        return

    await update_single_setting(
        message,
        state,
        car_settings_service,
        "consumption",
        value
    )

@router.message(CarSettings.edit_amortization)
async def process_edit_amortization(message: Message, state: FSMContext, **data):
    car_settings_service = data["car_settings_service"]

    try:
        value = validate_amortization(message.text)
    except ValueError as e:
        await message.answer(str(e))
        return

    await update_single_setting(
        message,
        state,
        car_settings_service,
        "amortization",
        value
    )

# =============================
# FSM: полное создание настроек
# =============================

@router.message(CarSettings.fuel_price)
async def process_fuel_price(message: Message, state: FSMContext):
    try:
        fuel_price = validate_fuel_price(message.text)
    except ValueError as e:
        await message.answer(str(e))
        return

    await state.update_data(fuel_price=fuel_price)
    await state.set_state(CarSettings.consumption)
    await ask_input(message, "Введите расход (л/100 км):")


@router.message(CarSettings.consumption)
async def process_consumption(message: Message, state: FSMContext):
    try:
        consumption = validate_fuel_consumption(message.text)
    except ValueError as e:
        await message.answer(str(e))
        return

    await state.update_data(consumption=consumption)
    await state.set_state(CarSettings.amortization)
    await ask_input(message, "Введите амортизацию (₽/км):")


@router.message(CarSettings.amortization)
async def process_amortization(message: Message, state: FSMContext, **data):

    car_settings_service = data["car_settings_service"]
    try:
        amortization = validate_amortization(message.text)
    except ValueError as e:
        await message.answer(str(e))
        return

    await state.update_data(amortization=amortization)
    await save_full_settings(message, state, car_settings_service)


# =======================
# Вспомогательные функции
# =======================

async def update_single_setting(
        message: Message,
        state: FSMContext,
        car_settings_service,
        field: str,
        value: float
):
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


async def save_full_settings(message: Message, state: FSMContext, car_settings_service):
    user_id = message.from_user.id
    data = await state.get_data()

    settings = car_settings_service.set(
        user_id,
        data["fuel_price"],
        data["consumption"],
        data["amortization"]
    )

    await send_car_settings(message, settings, "Настройки обновлены:")
    await state.clear()