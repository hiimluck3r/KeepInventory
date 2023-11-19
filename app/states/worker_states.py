from aiogram.fsm.state import State, StatesGroup

class NewDevice(StatesGroup):
    article = State()
    category = State()
    subcategory = State()
    name = State()
    quantity = State()
    productionYear = State()
    accountingYear = State()
    location = State()
    ownership = State()
    photo = State()
    confirmation = State()

class RedactDeviceState(StatesGroup):
    change = State()

class ProblematicDeviceCreation(StatesGroup):
    description = State()

class RedactProblematicDeviceState(StatesGroup):
    change = State()