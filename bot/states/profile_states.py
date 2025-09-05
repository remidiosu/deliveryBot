from aiogram.fsm.state import StatesGroup, State


class ProfileFSM(StatesGroup):
    choose_field = State()
    ask_full_name = State()
    ask_phone = State()
