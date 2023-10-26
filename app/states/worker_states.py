from aiogram.fsm.state import State, StatesGroup

class NewDevice(StatesGroup):
    category = State()
    subcategory = State()
    name = State()
    quantity = State()
    productionYear = State()
    accountingYear = State()
    location = State()
    ownership = State()
    photo = State()