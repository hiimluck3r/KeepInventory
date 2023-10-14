from aiogram.fsm.state import State, StatesGroup

class BarcodeImage(StatesGroup):
    image = State()