from aiogram import Router, F
from aiogram.types import (
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove,
)
from aiogram.fsm.context import FSMContext

from states.auth_states import Onboard
from routes.auth_routes.util import normalize_phone
from services.user_api_service import create_user


router = Router()


@router.message(Onboard.ask_full_name, F.text)
async def collect_full_name(message: Message, state: FSMContext):
    name = message.text.strip() # pyright: ignore[reportOptionalMemberAccess]
    if len(name) < 2:
        await message.answer("Имя слишком короткое. Введите полное ФИО.")
        return

    await state.update_data(full_name=name)

    kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📱 Отправить номер", request_contact=True)]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
    await state.set_state(Onboard.ask_phone)
    await message.answer(
        "Отправьте номер телефона (кнопкой ниже) или введите вручную в формате +7707XXXXXXX.",
        reply_markup=kb,
    )


@router.message(Onboard.ask_phone, F.contact)
async def collect_phone_contact(message: Message, state: FSMContext):
    phone = normalize_phone(getattr(message.contact, "phone_number", ""))
    if not phone:
        await message.answer("Номер не распознан. Введите вручную в формате +7707XXXXXXX.")
        return
    await _finalize_save(message, state, phone)


@router.message(Onboard.ask_phone, F.text)
async def collect_phone_text(message: Message, state: FSMContext):
    phone = normalize_phone(message.text or "")
    if not phone:
        await message.answer("Номер некорректен. Пример: +77071234567")
        return
    await _finalize_save(message, state, phone)


async def _finalize_save(message: Message, state: FSMContext, phone: str):
    data = await state.get_data()
    full_name = data.get("full_name")
    role = data.get("role")

    print(message.from_user.id)

    await create_user(
        telegram_id=message.from_user.id,  # type: ignore
        role=role,  # type: ignore
        full_name=full_name,  # type: ignore
        phone_number=phone
    )

    who = "админ" if role == "controller" else "курьер"
    await state.clear()
    await message.answer(
        f"Готово ✅ \n Вы зарегистрированы как *{who}*.\n Имя: {full_name} \n Телефон: {phone}",
        parse_mode="Markdown",
        reply_markup=ReplyKeyboardRemove(),
    )
