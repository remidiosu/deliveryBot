from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from services.user_api_service import fetch_couriers, add_courier_to_controller, get_courier_by_phone

from states.controller_states import AddCourierFSM
from keyboards.directory_kb import add_courier_kb
from routes.auth_routes.util import normalize_phone
from routes.controller_routes.directories import show_directories

router = Router()


@router.callback_query(F.data == "dir:couriers:list")
async def list_couriers(cb: CallbackQuery):
    controller_id = cb.from_user.id 
    response = await fetch_couriers(controller_id)
    couriers = response["data"]["couriers"]

    if not couriers:
        await cb.message.edit_text("У вас пока нет прикрепленных курьеров.")
        return

    text = "📋 Ваши курьеры:\n\n"
    for c in couriers:
        text += f"• {c.get('full_name', 'Без имени')} (тел: {c.get('phone_number', '(ошибка, номер не доступен)')})\n"

    await cb.message.edit_text(text)


@router.callback_query(F.data == "dir:couriers:add")
async def add_courier(cb: CallbackQuery, state: FSMContext):
    await state.set_state(AddCourierFSM.waiting_for_phone)
    await cb.message.edit_text("Введите номер телефона курьера, которого хотите добавить:")


@router.message(AddCourierFSM.waiting_for_phone, F.text)
async def process_courier_phone(message: Message, state: FSMContext):
    raw = message.text.strip()
    phone_number = normalize_phone(raw)
    
    if not phone_number:
        await message.answer(
            "❌ Неверный формат номера. Введите номер ещё раз (разрешены 7–15 цифр, с '+')."
        )
        return await add_courier(message)
    
    try:
        response = await get_courier_by_phone(phone_number)
        preview = response.get("data")
    except Exception as e:
        await message.answer(f"⚠️ Ошибка при поиске курьера.")
        return await show_directories(message, is_registered=True, role='админ')

    if not preview: 
        await message.answer("Не нашёл курьера с таким номером.")
        return await show_directories(message, is_registered=True, role='админ')

    await state.update_data(phone=phone_number, preview=preview)
    await state.set_state(AddCourierFSM.confirming)

    name = preview.get("full_name") or "Без имени"
    tg_id = preview.get("telegram_id") or "—"
    text = (
        "Нашёл курьера:\n"
        f"• Имя: {name}\n"
        f"• Телефон: {phone_number}\n"
        f"• Telegram ID: {tg_id}"
    ) 

    await message.answer(text, reply_markup=add_courier_kb(phone_number))


@router.callback_query(F.data.startswith("dir:couriers:add:confirm:"))
async def confirm_add_courier(cb: CallbackQuery, state: FSMContext):
    controller_id = cb.from_user.id
    phone = cb.data.split("dir:couriers:add:confirm:", 1)[1].strip()

    # подстрахуемся состоянием: если есть сохранённый номер — используем его
    data = await state.get_data()
    phone = data.get("phone") or phone

    try:
        await add_courier_to_controller(controller_id, phone)
    except Exception as e:
        await cb.message.edit_text(f"❌ Не удалось добавить курьера")
        await state.clear()
        return 
    
    name = (data.get("preview") or {}).get("full_name") or "Курьер"
    await cb.message.edit_text(f"✅ {name} успешно добавлен к вашему списку.")
    await state.clear()


@router.callback_query(F.data == "dir:couriers:add:cancel")
async def cancel_add_courier(cb: CallbackQuery, state: FSMContext):
    await state.clear()
    await cb.message.edit_text("Отменено. Курьер не добавлен.")
