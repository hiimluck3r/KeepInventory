import sys
import json
import psycopg2
import aiogram.utils.markdown as fmt

from bot.dispatcher import dp, bot
from bot.keyboards import *
from aiogram import types
from bot import DB, USER, PASSWORD, HOST, ROOT, PORT
from aiogram.utils.exceptions import BotBlocked
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

with open('bot/admins.json', 'r') as admin_file:
    admins = json.loads(json.load(admin_file))['admins']

print(admins)