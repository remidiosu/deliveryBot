from aiogram.fsm.state import State, StatesGroup


class AddCourierFSM(StatesGroup):
    waiting_for_phone = State()
    confirming = State()
