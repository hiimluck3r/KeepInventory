import sys
import json
import psycopg2
import aiogram.utils.markdown as fmt

from bot.dispatcher import dp, bot
from bot.keyboards import *
from aiogram import types
from time import sleep
from bot import DB, USER, PASSWORD, HOST, ROOT, PORT
from aiogram.utils.exceptions import BotBlocked
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

with open('bot/admins.json', 'r') as admin_file:
    admins = json.loads(json.load(admin_file))['admins']

"""
Подключение к БД
"""
while True:
    try:
        conn = psycopg2.connect(dbname=DB, user=USER, password=PASSWORD, host=HOST, port=PORT) #указывать в .env
        print('Connection to database is established')
        break
        
    except Exception as e:
        print("Can't establish connection to database. Error:", e)
        sleep(3)

"""
/start
"""

@dp.message_handler(commands="start")
async def greeter(message: types.Message):
    greet = "Бот для инвентаризации."

    keyboard = goto_menu()
    await message.answer(greet, reply_markup=keyboard)

"""
Главное меню
"""
@dp.message_handler(Text(equals="Главное меню"))
async def main_menu(message: types.Message):
    keyboard = get_main_menu()
    await message.answer(f"Главное меню", reply_markup=keyboard)

