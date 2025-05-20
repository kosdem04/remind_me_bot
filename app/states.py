from aiogram.fsm.state import State, StatesGroup


class AddEventState(StatesGroup):
    name = State()
    date = State()
    sure = State()

class DeleteEventState(StatesGroup):
    event_id = State()
    sure = State()