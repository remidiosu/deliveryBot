from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder

from states.auth_states import Onboard
from services.user_api_service import verify_user


router = Router()


@router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    tg_id = message.from_user.id # pyright: ignore[reportOptionalMemberAccess]

    # check if user already exists 
    verified = await verify_user(tg_id)
    data = verified.get("data")

    if data.get('registered'):
        await message.answer(f"Вы уже зарегистрированы как {data.get('role')} ✅")
        return

    await state.clear()
    await state.set_state(Onboard.waiting_role)

    kb = InlineKeyboardBuilder()
    kb.button(text="Курьер", callback_data="role:courier")
    kb.button(text="Администратор", callback_data="role:controller")
    kb.adjust(2)
    await message.answer("Кто вы?", reply_markup=kb.as_markup())
