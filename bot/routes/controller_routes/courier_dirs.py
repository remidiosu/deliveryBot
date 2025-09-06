from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from keyboards.directory_kb import directories_kb, couriers_menu_kb, stores_menu_kb, products_menu_kb
from services.user_api_service import fetch_couriers, add_courier_to_controller

router = Router()


@router.callback_query(F.data == "dir:couriers:list")
async def list_courier(cb: CallbackQuery):
    await cb.message.edit_text("list")


@router.callback_query(F.data == "dir:couriers:add")
async def add_courier(cb: CallbackQuery):
    await cb.message.edit_text("add")
