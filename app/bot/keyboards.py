from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🚘 Добавить поездку")],
        [KeyboardButton(text="📊 Посмотреть все поездки")],
        [KeyboardButton(text="⚙️ Настройки автомобиля")],
    ],
    resize_keyboard=True,
)

car_settings_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="⛽ Изменить цену топлива")],
        [KeyboardButton(text="🔥 Изменить расход")],
        [KeyboardButton(text="🔧 Изменить амортизацию")],
        [KeyboardButton(text="⬅️ Назад")]
    ],
    resize_keyboard=True
)

car_settings_choice_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="✏️ Ввести новые настройки")],
        [KeyboardButton(text="📊 Установить средние значения")],
        [KeyboardButton(text="⬅️ Назад")]
    ],
    resize_keyboard=True
)