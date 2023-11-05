import asyncio
import sys
from aiogram import types, Router, F
from app.loader import dp, bot
from app import greet_stranger_text, greet_user_text, ROOT
from app.keyboards.reply import *
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from app.db.operations import get_users_by_role

router = Router()

@router.message(Command("start"))
@router.message(F.text.lower()=="главное меню")
async def get_start(message: types.Message, state: FSMContext):
    await state.clear()
    if message.from_user.id not in (await get_users_by_role("spectator")) and (message.from_user.id != ROOT):
        await message.answer(greet_stranger_text, parse_mode='HTML', reply_markup = reply_column_menu(["Контакты", "GitHub"]))
    else:
        await message.answer(greet_user_text, parse_mode='HTML', reply_markup = get_menu())

@router.message(Command("id"))
async def my_id(message: types.Message):
    await message.answer(f"```{message.from_user.id}```", parse_mode="MarkdownV2")