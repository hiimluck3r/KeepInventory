from aiogram.filters.callback_data import CallbackData

class RedactDevice(CallbackData, prefix="redact"):
    action: str
    articleNumber: int