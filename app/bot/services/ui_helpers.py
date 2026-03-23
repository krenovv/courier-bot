from aiogram.types import Message, ReplyKeyboardRemove

from app.bot.keyboards import car_settings_keyboard


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


async def send_car_settings(
    message: Message,
    settings,
    text: str = "Текущие настройки:",
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