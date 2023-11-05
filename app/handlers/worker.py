import asyncio
from aiogram import types, Router, F
from app.loader import dp, bot
from app import greet_stranger_text, greet_user_text
from app.keyboards.reply import reply_column_menu, reply_row_menu
from app.keyboards.inline import inline_column_menu, inline_row_menu
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from app.filters.role_filter import RoleCheck

router = Router()

@router.callback_query(F.data.startswith('create'), RoleCheck("worker"))
async def create_device_callback(callback: types.CallbackQuery, state: FSMContext):
    articleNumber = int(callback.data.split(".")[1])
    await callback.message.answer(f"Код в коллбэке: {articleNumber}")
    await callback.answer()