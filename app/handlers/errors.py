import asyncio
from aiogram import types, Router, F
from app.loader import dp, bot
from app import greet_stranger_text, greet_user_text
from app.roles import spectator
from app.keyboards.reply import reply_column_menu
from aiogram.filters.command import Command

router = Router()