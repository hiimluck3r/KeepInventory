from aiogram.fsm.state import State, StatesGroup

class BarcodeImage(StatesGroup):
    image = State()

class ArticleSearch(StatesGroup):
    article = State()
    confirmation = State()

class ProblematicDevices(StatesGroup):
    init = State()