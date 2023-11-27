import asyncio
import sys
from os import remove
from app.middlewares.misc import *
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
from app.utils.callback_factories import LogsInfo

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

#Upload backup
@router.callback_query(RoleCheck("admin"), F.data == "backup_upload")
async def upload_backup(callback: types.CallbackQuery, state: FSMContext):
    tables = ['users', 'devices', 'problematicdevices', 'software', 'notes']
    await state.set_state(BackupUpload.users)
    await state.update_data(tables = tables)

    await callback.message.answer("Делаю резервное копирование данных...")
    for table in tables:
        await do_backup(table)
        filepath = types.FSInputFile(f'app/backups/{table}.csv')
        try:
            await callback.message.answer_document(document=filepath, filename=f'{table}.csv', caption=f'Таблица {table}')
        except Exception as e:
            await callback.message.answer(f'Непредвиденная ошибка: {e}')

    await callback.message.answer(
        """⚠️ Backup upload ⚠️\n\nВ ходе загрузки бэкапа все нынешние данные удалятся.
        \nЧтобы их не потерять, скачайте резервные копии, актуальные на текущий момент.
        \nБэкапы в этой версии бота сохраняются как .csv файлы, что требует внимательной обработки данных и деления её на правильные столбцы.
        \nНЕ ИСПОЛЬЗУЙТЕ HEADER (заголовки/названия столбцов).
        \nФормат записи вы можете найти в актуальных бэкапах.
        \nПомните, что все действия производятся сугубо на ваш страх и риск и могут привести к полной потере данных.
        \n\nЗагрузите таблицу с пользователями (users.csv):""", reply_markup=reply_row_menu(["Отмена"])
    )
    await callback.answer()

@router.message(RoleCheck("admin"), BackupUpload.users, F.document)
async def upload_backup_users_process(message: types.Message, state: FSMContext):
    try:
        document = message.document
        await bot.download(document, destination="app/uploaded_backups/users.csv")
        await do_upload_backup("users")
        await state.set_state(BackupUpload.devices)
        await message.answer("Загрузите таблицу с устройствами (devices.csv):", reply_markup=reply_row_menu(["Отмена"]))
    except Exception as e:
        await state.clear()
        await message.answer(f"Непредвиденная ошибка: {e}", reply_markup=get_menu())

@router.message(RoleCheck("admin"), BackupUpload.devices, F.document)
async def upload_backup_devices_process(message: types.Message, state: FSMContext):
    try:
        document = message.document
        await bot.download(document, destination="app/uploaded_backups/devices.csv")
        await do_upload_backup("devices")
        await state.set_state(BackupUpload.problematicDevices)
        await message.answer("Загрузите таблицу с проблемными устройствами (problematicdevices.csv):", reply_markup=reply_row_menu(["Отмена"]))
    except Exception as e:
        await state.clear()
        await message.answer(f"Непредвиденная ошибка: {e}", reply_markup=get_menu())

@router.message(RoleCheck("admin"), BackupUpload.problematicDevices, F.document)
async def upload_backup_problematic_devices_process(message: types.Message, state: FSMContext):
    try:
        document = message.document
        await bot.download(document, destination="app/uploaded_backups/problematicdevices.csv")
        await do_upload_backup("problematicdevices")
        await state.set_state(BackupUpload.software)
        await message.answer("Загрузите таблицу с программным обеспечением (software.csv):", reply_markup=reply_row_menu(["Отмена"]))
    except Exception as e:
        await state.clear()
        await message.answer(f"Непредвиденная ошибка: {e}", reply_markup=get_menu())

@router.message(RoleCheck("admin"), BackupUpload.software, F.document)
async def upload_backup_software_process(message: types.Message, state: FSMContext):
    try:
        document = message.document
        await bot.download(document, destination="app/uploaded_backups/software.csv")
        await do_upload_backup("software")
        await state.set_state(BackupUpload.notes)
        await message.answer("Загрузите таблицу с заметками (software.csv):", reply_markup=reply_row_menu(["Отмена"]))
    except Exception as e:
        await state.clear()
        await message.answer(f"Непредвиденная ошибка: {e}", reply_markup=get_menu())

@router.message(RoleCheck("admin"), BackupUpload.notes, F.document)
async def upload_backup_notes_process(message: types.Message, state: FSMContext):
    try:
        document = message.document
        await bot.download(document, destination="app/uploaded_backups/notes.csv")
        await do_upload_backup("notes")
        await state.clear()
        await message.answer("Загрузка данных успешно завершена. Проверьте целостность данных в ходе использования бота.", reply_markup=get_menu())
    except Exception as e:
        await state.clear()
        await message.answer(f"Непредвиденная ошибка: {e}", reply_markup=get_menu())

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
        role = await custom_sql(
            "SELECT role FROM users WHERE userid = $1", userid, fetchval=True
        )
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
        role = await custom_sql(
            "SELECT role FROM users WHERE userid = $1", userid, fetchval=True
        )
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
    await state.clear()
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
    exit(0)

"""
Logs
"""

@router.callback_query(F.data == 'logs', RoleCheck("admin"))
async def logs_callback(callback: types.CallbackQuery, state: FSMContext):
    
    directory = "/~/KeepInventory/logs"
    logs = get_filenames(directory)
    print(len(logs), file=sys.stderr)
    if len(logs) != 0:
        answer_text = f"<b>Список доступных логов:</b>\n\n"
        for index, log in enumerate(logs):
            answer_text+=f"{index+1}. {log}\n"

        answer_text+=f"\nОтправьте номер лога, который хотите прочитать:"
        await state.set_state(Logs.confirmation)
        await state.update_data(logs = logs)
    else:
        answer_text="Лог-файлов не обнаружено."
    await callback.message.answer(answer_text, reply_markup=reply_row_menu(["Отмена"]), parse_mode="HTML")
    await callback.answer()

@router.message(Logs.confirmation, RoleCheck("admin"), F.text)
async def logs_process(message: types.Message, state: FSMContext):
    data = await state.get_data()
    logs = data['logs']
    try:
        index = int(message.text)-1
        if index < len(logs) and index >= 0:
            path = f'/~/KeepInventory/logs/{logs[index]}'
            await state.clear()
            try:
                log_info = ''
                with open(path, 'r') as log:
                    log_info = log.read()
                
                for c in range(0, len(log_info), 4096):
                    await message.answer(log_info[c:c+4096], reply_markup=get_menu())
                
                await message.answer(
                    "Удалить лог-файл?",
                    reply_markup=delete_log_keyboard(path)
                )
            except Exception as e:
                await message.answer(f"Возникла непредвиденная ошибка: {e}", reply_markup=get_menu())
        else:
            await message.answer("Некорректные данные, попробуйте ещё раз:")
    except ValueError:
        await message.answer("Некорректные данные, попробуйте ещё раз:")

@router.callback_query(LogsInfo.filter(F.action == "delete_current_log"), RoleCheck("admin"))
async def delete_current_log_process(callback: types.CallbackQuery, callback_data=LogsInfo):
    path = callback_data.path
    try:
        remove(path)
        await callback.message.answer(f"Лог-файл {path} был удалён.", reply_markup=get_menu())
    except Exception as e:
        await callback.message.answer(f"Возникла непредвиденная ошибка: {e}.")
    finally:
        await callback.answer()

@router.callback_query(LogsInfo.filter(F.action == "delete_all_logs"), RoleCheck("admin"))
async def delete_all_logs_process(callback: types.CallbackQuery, callback_data=LogsInfo):
    directory = "/~/KeepInventory/logs"
    logs = get_filenames(directory)
    try:
        for log in logs:
            remove(f"{directory}/{log}")
        await callback.message.answer(
            "Лог-файлы были удалены.", reply_markup=get_menu()
        )
    except Exception as e:
        await callback.message.answer(f"Возникла непредвиденная ошибка: {e}.")
    finally:
        await callback.answer()