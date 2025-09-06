from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)


def directories_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👤 Курьеры", callback_data="dir:couriers")],
        [InlineKeyboardButton(text="🏪 Магазины", callback_data="dir:stores")],
        [InlineKeyboardButton(text="📦 Товары", callback_data="dir:products")],
    ])


def couriers_menu_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📜 Список курьеров",  callback_data="dir:couriers:list")],
        [InlineKeyboardButton(text="➕ Добавить нового курьера", callback_data="dir:couriers:add")],
        [InlineKeyboardButton(text="⬅️ Назад",           callback_data="dir:root")],
    ])


def stores_menu_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📜 Список магазинов",  callback_data="dir:stores:list")],
        [InlineKeyboardButton(text="➕ Добавить магазин",   callback_data="dir:stores:add")],
        [InlineKeyboardButton(text="⬅️ Назад",             callback_data="dir:root")],
    ])


def products_menu_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📜 Список товаров",  callback_data="dir:products:list")],
        [InlineKeyboardButton(text="➕ Добавить товар",   callback_data="dir:products:add")],
        [InlineKeyboardButton(text="⬅️ Назад",           callback_data="dir:root")],
    ])
