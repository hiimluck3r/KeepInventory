from typing import Optional
from aiogram.filters.callback_data import CallbackData

class RedactProblematicDevice(CallbackData, prefix="redact"):
    action: str
    articleNumber: int

class RedactDevice(CallbackData, prefix="redact"):
    action: str
    articleNumber: int

class PaginationValues(CallbackData, prefix="pagination"):
    action: str
    page: Optional[int] | None = None