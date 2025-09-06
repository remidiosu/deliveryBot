from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
)


def profile_menu_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Изменить имя")],
            [KeyboardButton(text="Изменить телефон")],
            [KeyboardButton(text="Отмена")],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
