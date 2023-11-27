from aiogram.fsm.state import State, StatesGroup

class GreetText(StatesGroup):
    text = State()

class Logs(StatesGroup):
    confirmation = State()

class BackupUpload(StatesGroup):
    users = State()
    devices = State()
    problematicDevices = State()
    software = State()
    notes = State()