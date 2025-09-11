from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from keyboards.directory_kb import directories_kb, couriers_menu_kb, stores_menu_kb, products_menu_kb


router = Router()


# command: /directories - Справочники
@router.message(Command("directories"))
async def show_directories(m: Message, is_registered: bool, role: str):
    await m.answer(
        "📂 Справочники:\nВыберите категорию для управления.",
        reply_markup=directories_kb()
    )


@router.callback_query(F.data == "dir:couriers")
async def open_couriers(cb: CallbackQuery, is_registered: bool, role: str):
    await cb.message.edit_text("👤 Курьеры — выберите действие:", reply_markup=couriers_menu_kb())
    await cb.answer()


@router.callback_query(F.data == "dir:stores")
async def open_stores(cb: CallbackQuery, is_registered: bool, role: str):
    await cb.message.edit_text("🏪 Магазины — выберите действие:", reply_markup=stores_menu_kb())
    await cb.answer()


@router.callback_query(F.data == "dir:products")
async def open_products(cb: CallbackQuery, is_registered: bool, role: str):
    await cb.message.edit_text("📦 Товары — выберите действие:", reply_markup=products_menu_kb())
    await cb.answer()


@router.callback_query(F.data == "dir:root")
async def back_to_root(cb: CallbackQuery, is_registered: bool, role: str):
    await cb.message.edit_text("📂 Справочники:\nВыберите категорию для управления.", reply_markup=directories_kb())
    await cb.answer()
