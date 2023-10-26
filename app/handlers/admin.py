import asyncio
import sys
from aiogram import types, Router, F
from app.loader import dp, bot
from app.roles import admin, worker, spectator
from app import ROOT
from app.keyboards.reply import *
from app.keyboards.inline import get_dashboard_menu
from aiogram.filters import CommandObject
from aiogram.filters.command import Command
from app.keyboards import get_username
from app.db.operations import *

router = Router()

@router.message(Command("admin"), F.from_user.id.in_(admin))
async def get_admin_dashboard(message: types.Message):
    await message.answer("Админ-меню", reply_markup=get_dashboard_menu())

@router.message(Command("make"), F.from_user.id.in_(admin))
async def make_role(message: types.Message, command: CommandObject): # /make userid.role
    if command.args:
        userid, role = command.args.split('.')
        try:
            result = await add_user(int(userid), role)
            print(result, file=sys.stderr)
            users = await get_users_by_role(role)
            print(f"Users by role {role}: {users}", file=sys.stderr)
            await message.answer(f"Пользователь {await get_username(userid)} добавлен в группу {role}.") #защита на введение admin, ролей которых не существует
        except Exception as e:
            await message.answer(f"Exception found: {e}")
    else:
        pass

@router.message(Command("rm"), F.from_user.id.in_(admin))
async def remove_role(message: types.Message, command: CommandObject): # /rm userid
    if command.args:
        userid = int(command.args)
        try:
            result = await delete_user(userid)
            print(result, file=sys.stderr)
            await message.answer(f"Пользователь {await get_username(userid)} успешно удалён.")
        except Exception as e:
            await message.answer(f"Exception found: {e}")
    else:
        pass

#@router.message(Command("makeadmin"), F.from_user.id==ROOT)

#@router.message(Command("rmadmin"), F.from_user.id==ROOT)