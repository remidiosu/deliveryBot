from aiogram.fsm.state import StatesGroup, State


class Onboard(StatesGroup):
    waiting_role = State()
    controller_code = State()
    ask_full_name = State()
    ask_phone = State()