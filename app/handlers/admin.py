import asyncio
from aiogram import types, Router, F
from app.dispatcher import dp, bot
from app.roles import admin, root
from app.keyboards.reply import *
from app.keyboards.inline import *
from aiogram.filters.command import Command

router = Router()

@router.message(Command("admin"))
