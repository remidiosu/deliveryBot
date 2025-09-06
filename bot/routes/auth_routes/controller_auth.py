import os

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from states.auth_states import Onboard
from routes.auth_routes.start_cmd import start


router = Router()


@router.message(Command("cancel"))
async def cancel_any(m: Message, state: FSMContext):
    await state.clear()
    await m.answer("Отменено.")
    await start(m, state)


@router.callback_query(F.data == "role:controller", Onboard.waiting_role)
async def pick_controller(c: CallbackQuery, state: FSMContext):
    await state.update_data(role="controller")
    await state.set_state(Onboard.controller_code)
    await c.message.edit_text( # type: ignore
        "Введите код администратора (получен от владельца):\n`/code <секрет>` Пример: `/code 123321`",
        parse_mode="Markdown",
    )


@router.message(Onboard.controller_code, F.text)
async def controller_enter_code(m: Message, state: FSMContext):
    text = m.text.strip() # type: ignore
    parts = text.split(maxsplit=1)
    code = parts[1].strip() if parts and parts[0].lower() in ("/code", "code") and len(parts) > 1 else text
    master = os.getenv("CONTROLLER_MASTER_CODE", "")
    if not master:
        await m.answer("Мастер-код не настроен у сервера. Свяжитесь с владельцем.")
        return
    if code != master:
        await m.answer("Код неверный. Попробуйте ещё раз или /cancel.")
        return
    await state.set_state(Onboard.ask_full_name)
    await m.answer("Код принят ✅\nВведите ваше *ФИО*:", parse_mode="Markdown")
