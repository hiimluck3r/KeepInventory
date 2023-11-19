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

class Software(StatesGroup):
    init = State()

class NewSoftware(StatesGroup):
    filename = State()
    fileurl = State()
    description = State()

class RedactSoftwareState(StatesGroup):
    change = State()

class Notes(StatesGroup):
    init = State()

class NewNote(StatesGroup):
    header = State()
    description = State()

class RedactNoteState(StatesGroup):
    change = State()