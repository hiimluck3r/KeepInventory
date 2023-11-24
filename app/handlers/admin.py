import asyncio
import sys
import os
from aiogram import types, Router, F
from app.loader import dp, bot
from app import ROOT
from app.db.operations import *
from app.keyboards.reply import *
from app.keyboards.inline import *
from app.keyboards import get_username
from app.states.admin_states import *
from aiogram.filters import CommandObject
from aiogram.filters.command import Command
from app.filters.role_filter import RoleCheck
from aiogram.fsm.context import FSMContext

router = Router()

"""
Admin Dashboard
"""

@router.message(Command("admin"), RoleCheck("admin")) #rewrite filters to access roles each time
async def get_admin_dashboard(message: types.Message):
    await message.answer("Админ-меню", reply_markup=get_dashboard_menu())

"""
Backup
"""

#Download backup
@router.callback_query(RoleCheck("admin"), F.data == "backup_download")
async def download_backup(callback: types.CallbackQuery):
    tables = ['users', 'devices', 'problematicdevices', 'software', 'notes']
    for table in tables:
        await do_backup(table)
        filepath = types.FSInputFile(f'app/backups/{table}.csv')
        try:
            await callback.message.answer_document(document=filepath, filename=f'{table}.csv', caption=f'Таблица {table}')
        except Exception as e:
            await callback.message.answer(f'Непредвиденная ошибка: {e}')
        await callback.answer()

"""
User Manipulation
"""

@router.message(Command("make"), RoleCheck("admin"))
async def make_role(message: types.Message, command: CommandObject): # /make userid.role
    if command.args:
        userid, role = command.args.split('.')
        if role in ["worker", "spectator"]:
            try:
                result = await add_user(int(userid), role)
                await message.answer(f"Пользователь {await get_username(userid)} добавлен в группу {role}.") #защита на введение admin, ролей которых не существует

            except Exception as e:
                await message.answer(f"Exception found: {e}")
        else:
            await message.answer(f"Вы не можете добавить пользователя с ролью {role}. Доступные роли: worker, spectator.")

@router.message(Command("rm"), RoleCheck("admin"))
async def remove_role(message: types.Message, command: CommandObject): # /rm userid
    if command.args:
        userid = int(command.args)
        role = await custom_sql(f"SELECT role FROM users WHERE userid = $1", userid, fetchval=True)
        if role!=2:
            try:
                result = await delete_user(userid)
                await message.answer(f"Пользователь {await get_username(userid)} успешно удалён.")

            except Exception as e:
                await message.answer(f"Exception found: {e}")
        else:
            await message.answer(f"Нет прав для удаления пользователя {get_username(userid)}, поскольку этот пользователь администратор.")

@router.message(Command("makeadmin"), F.from_user.id==ROOT)
async def make_admin(message: types.Message, command: CommandObject): # /makeadmin userid
    if command.args:
        userid = int(command.args)
        try:
            result = await add_user(userid, "admin")            
            
            await message.answer(f"Пользователь {await get_username(userid)} добавлен в список администраторов.")
        except Exception as e:
            await message.answer(f"Exception found: {e}")

@router.message(Command("rmadmin"), F.from_user.id==ROOT)
async def remove_admin(message: types.Message, command: CommandObject):
    if command.args:
        userid = int(command.args)
        role = await custom_sql(f"SELECT role FROM users WHERE userid = $1", userid, fetchval=True)
        if role==2:
            try:
                result = await delete_user(userid)
                await message.answer(f"Пользователь {await get_username(userid)} удалён из списка администраторов.")
                
            except Exception as e:
                await message.answer(f"Exception found: {e}")
        else:
            await message.answer(f"Пользователь {await get_username(userid)} не администратор.")

@router.message(Command("initroot"), F.from_user.id==ROOT)
async def remove_admin(message: types.Message, command: CommandObject):
    await add_user(ROOT, 'root')
    await message.answer(f"Добро пожаловать, {await get_username(ROOT)}")

"""
Greet message manipulation
"""

@router.callback_query(F.data.startswith("changegreet"), RoleCheck("admin"))
async def changegreet_callback(callback: types.CallbackQuery, state: FSMContext):
    action = callback.data.split("_")[-1]
    await state.set_state(GreetText.text)
    await state.update_data(action = action)

    await callback.message.answer("Введите текст приветственного сообщения:", reply_markup=reply_row_menu(["Отмена"]))
    await callback.answer()

@router.message(GreetText.text, RoleCheck("admin"), F.text)
async def changegreet_process(message: types.Message, state: FSMContext):
    data = await state.get_data()
    action = data['action']
    new_text = message.text
    with open(f"app/greet_{action}.txt", "w") as greet:
        greet.write(new_text)
    await message.answer(f"Файл greet_{action}.txt был перезаписан. Изменения вступят в силу после перезагрузки бота.", reply_markup=get_menu())

"""
Reboot
"""

@router.callback_query(F.data == 'reboot', RoleCheck("admin"))
async def reboot_callback(callback: types.CallbackQuery):
    await callback.message.answer("Перезагружаем бота...")
    await callback.answer()

    exit()