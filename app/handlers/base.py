import asyncio
from aiogram import types, Router, F
from app.loader import dp, bot
from app import greet_stranger_text, greet_user_text
from app.roles import spectator
from app.keyboards.reply import reply_column_menu
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

router = Router()

@router.message(Command("start"))
@router.message(F.text=="Главное меню")
async def get_start(message: types.Message, state: FSMContext):
    await state.clear()
    if message.from_user.id not in spectator:
        await message.answer(greet_stranger_text, parse_mode='HTML', reply_markup = reply_column_menu(["Контакты", "GitHub"]))
    else:
        await message.answer(greet_user_text, parse_mode='HTML', reply_markup = reply_column_menu(["Поиск по штрих-коду", "Поиск по номеру",
    "Поиск по аудитории", "Заметки", "Программное обеспечение",
    "Проблемные устройства"]))

@router.message(Command("id"))
async def my_id(message: types.Message):
    await message.answer(f"```{message.from_user.id}```", parse_mode="MarkdownV2")