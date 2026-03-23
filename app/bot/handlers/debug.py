from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from app.bot.keyboards import main_keyboard

router = Router()


@router.message(F.text == "Удалить поездки")
async def debug_reset_trips(message: Message, state: FSMContext, **data):
    await state.clear()

    trip_service = data["trip_service"]
    user_id = message.from_user.id

    trip_service.delete_all_trips(user_id)

    await message.answer("Все поездки удалены", reply_markup=main_keyboard)


@router.message(F.text == "Удалить настройки")
async def debug_reset_settings(message: Message, state: FSMContext, **data):
    await state.clear()

    car_settings_service = data["car_settings_service"]
    user_id = message.from_user.id

    car_settings_service.delete(user_id)

    await message.answer("Настройки автомобиля удалены", reply_markup=main_keyboard)