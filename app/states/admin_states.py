from aiogram.fsm.state import State, StatesGroup

class GreetText(StatesGroup):
    text = State()

class Logs(StatesGroup):
    confirmation = State()