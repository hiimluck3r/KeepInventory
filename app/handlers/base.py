import asyncio
from aiogram import types, Router, F
from app.dispatcher import dp, bot
from app import greet_stranger_text, greet_user_text
from app.roles import spectator
from app.keyboards.reply import main_menu, stranger_menu
from aiogram.filters.command import Command

router = Router()

@router.message(Command("start"))
async def get_start(message: types.Message):
    if message.from_user.id not in spectator:
        await message.answer(greet_stranger_text, parse_mode='HTML', reply_markup = stranger_menu())
    else:
        await message.answer(greet_user_text, parse_mode='HTML', reply_markup = main_menu())