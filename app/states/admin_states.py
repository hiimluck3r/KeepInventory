from aiogram.fsm.state import State, StatesGroup

class GreetText(StatesGroup):
    text = State()