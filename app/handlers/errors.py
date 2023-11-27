import asyncio
from aiogram import types, Router, F
from app.loader import dp, bot
from app import greet_stranger_text, greet_user_text
from app.keyboards.reply import reply_column_menu
from aiogram.filters.command import Command
from app.filters.role_filter import RoleCheck

router = Router()