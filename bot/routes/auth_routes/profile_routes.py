from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from aiogram.types import (
    Message,
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)

from states.profile_states import ProfileFSM
from keyboards.profile_kb import profile_menu_kb
from routes.auth_routes.start_cmd import start
from routes.auth_routes.util import normalize_phone
from services.api_service import fetch_user, update_user


router = Router()


@router.message(Command("profile"))
async def profile_entry(message: Message, state: FSMContext):
    tg_id = message.from_user.id  # type: ignore
    actor = await fetch_user(tg_id)

    if not actor.get('data'):
        await message.answer("Пройдите регистрицию по команде /start")
        await state.clear()
        await start(message, state)
        return
    
    profile = actor['data']
    full_name = profile.get("full_name")
    phone = profile.get("phone_number")

    text = (
        "📄 *Профиль*\n\n"
        f"Имя: {full_name}\n"
        f"Телефон: {phone}\n\n"
        "Что хотите изменить?"
    )
    await state.set_state(ProfileFSM.choose_field)
    await message.answer(text, reply_markup=profile_menu_kb(), parse_mode="Markdown")


@router.message(ProfileFSM.choose_field, F.text.lower().in_(["изменить имя", "изменить телефон", "отмена"]))
async def profile_choose(message: Message, state: FSMContext):
    choice = message.text.lower() # type: ignore

    if choice == "отмена":
        await state.clear()
        await message.answer("Ок, ничего не меняем.", reply_markup=ReplyKeyboardRemove())
        return

    if choice == "изменить имя":
        await state.set_state(ProfileFSM.ask_full_name)
        await message.answer("Введите новое *полное имя*:", parse_mode="Markdown", reply_markup=ReplyKeyboardRemove())
        return

    if choice == "изменить телефон":
        kb = ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="📱 Отправить номер", request_contact=True)]],
            resize_keyboard=True,
            one_time_keyboard=True,
        )
        await state.set_state(ProfileFSM.ask_phone)
        await message.answer(
            "Введите новый номер телефона в формате +7xxxxxxxxxx или отправьте контакт:",
            reply_markup=kb,
        )
        return


@router.message(ProfileFSM.ask_full_name, F.text)
async def profile_set_full_name(message: Message, state: FSMContext):
    telegram_id = message.from_user.id  # type: ignore
    new_name = (message.text or "").strip()
    if len(new_name) < 2:
        await message.answer("Имя слишком короткое. Введите полное ФИО.")
        return

    tg_id = message.from_user.id  # type: ignore
    actor = await fetch_user(tg_id)
    profile = actor.get('data')

    if not profile:
        await message.answer("Пройдите регистрицию по команде /start")
        await state.clear()
        await start(message, state)
        return

    profile["full_name"] = new_name
    await update_user(telegram_id, **profile)

    await state.clear()
    await message.answer("Готово! Имя обновлено ✅", reply_markup=ReplyKeyboardRemove())


@router.message(ProfileFSM.ask_phone)
async def profile_set_phone(message: Message, state: FSMContext):
    raw_phone = None
    if message.contact and message.contact.phone_number:
        raw_phone = message.contact.phone_number
    elif message.text:
        raw_phone = message.text.strip()

    if not raw_phone:
        await message.answer("Введите номер или отправьте контакт.")
        return

    phone = normalize_phone(raw_phone)
    if not phone:
        await message.answer("Неверный формат телефона. Повторите ещё раз.")
        return

    telegram_id = message.from_user.id #type: ignore
    actor = await fetch_user(telegram_id)
    profile = actor.get('data')

    if not profile:
        await message.answer("Пройдите регистрицию по команде /start")
        await state.clear()
        await start(message, state)
        return

    profile["phone_number"] = phone
    await update_user(telegram_id, **profile)

    await state.clear()
    await message.answer(f"Телефон обновлён: {phone} ✅", reply_markup=ReplyKeyboardRemove())
