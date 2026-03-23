from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from app.bot.keyboards import main_keyboard

router = Router()

@router.message((F.text == "⬅️ Назад") | (F.text.lower() == "отмена"))
async def back_to_main(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Выберите действие:", reply_markup=main_keyboard)