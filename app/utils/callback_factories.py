from typing import Optional
from aiogram.filters.callback_data import CallbackData

class RedactDevice(CallbackData, prefix="redact"):
    action: str
    articleNumber: str

class RedactProblematicDevice(CallbackData, prefix="redact"):
    action: str
    articleNumber: str

class RedactSoftware(CallbackData, prefix="redact"):
    action: str
    id: int

class RedactNotes(CallbackData, prefix="redact"):
    action: str
    id: int

class PaginationValues(CallbackData, prefix="pagination"):
    action: str
    page: Optional[int] | None = None

class LogsInfo(CallbackData, prefix="log"):
    action: str
    path: Optional[str] | None = None