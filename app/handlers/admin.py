import asyncio
from aiogram import types, Router, F
from app.dispatcher import dp, bot
from app.roles import admin
from app import ROOT
from app.keyboards.reply import *
from app.keyboards.inline import get_dashboard_menu
from aiogram.filters.command import Command

router = Router()

@router.message(Command("admin"), F.from_user.id.in_(admin))
async def get_admin_dashboard(message: types.Message):
    await message.answer("Админ-меню", reply_markup=get_dashboard_menu())