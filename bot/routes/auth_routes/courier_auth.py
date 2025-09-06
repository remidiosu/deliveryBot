from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from states.auth_states import Onboard


router = Router()


@router.callback_query(F.data == "role:courier", Onboard.waiting_role)
async def pick_courier(c: CallbackQuery, state: FSMContext):
    await state.update_data(role="courier")
    await state.set_state(Onboard.ask_full_name)
    await c.message.edit_text("Введите ваше *ФИО* (как в документах):", parse_mode="Markdown") # type: ignore


from aiogram.filters import Command
from aiogram.types import Message

@router.message(Command("whoami"))
async def whoami(m: Message, role: str | None, is_registered: bool):
    await m.answer(f"role={role!r}, registered={is_registered}")