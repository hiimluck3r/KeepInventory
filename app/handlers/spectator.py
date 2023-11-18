import asyncio
import os
import sys
from aiogram import types, Router, F
from app.loader import dp, bot
from app import ROOT
from app.middlewares.articles import *
from app.keyboards.reply import *
from app.db.operations import *
from app.keyboards.inline import *
from aiogram.filters import CommandObject
from aiogram.filters.command import Command
from app.keyboards import get_username
from app.barcodes.barcode_reader import get_code
from app.states.spectator_states import BarcodeImage, ArticleSearch
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from app.filters.role_filter import RoleCheck

router = Router()

"""
/users

Gives you a list with all users, including root
template: *nickname* - *userid* - *role*
"""

@router.message(Command("users"), RoleCheck("spectator"))
async def users_list(message: types.Message, command: CommandObject):
    users = await custom_sql("SELECT * FROM users", fetch=True)
    result = f"Список пользователей:"
    for row in users:
        role = None
        if row['role'] == 3:
            role = 'ROOT'
        elif row['role'] == 2:
            role = "Admin"
        elif row['role'] == 1:
            role = "Worker"
        elif row['role'] == 0:
            role = "Spectator"

        result+=f"\n{await get_username(row['userid'])} - {row['userid']} - {role}"
    await message.answer(result)

"""
Barcode search
"""

@router.message(F.text=="Поиск по штрих-коду", RoleCheck("spectator"))
async def barcode_search(message: types.Message, state: FSMContext):
    await message.answer(f"Пришлите фотографию, на которой чётко видно штрих-код", reply_markup=reply_row_menu(["Отмена"]))
    await state.set_state(BarcodeImage.image)

@router.message(RoleCheck("spectator"), F.photo, BarcodeImage.image)
async def barcode_processing(message: types.Message, state: FSMContext):
    filepath = f"app/temp/{message.from_user.id}.jpg"
    await bot.download(message.photo[-1], destination = filepath)
    status, data = await get_code(filepath) #if successful, then data == articleNumber
    os.remove(filepath)
    if status:
        if not(await article_guard(data)):
            #If article doesn't exist
            #If user is worker, then allow them to make records here
            if message.from_user.id in await get_users_by_role("worker"):
                buttons = [types.InlineKeyboardButton(text="Создать новую запись", callback_data=f"create.{data}")]
                await message.answer(f"Устройство с артикулом: {data} не было найдено.", reply_markup=inline_row_menu(buttons))
            else:
                await message.answer(f"Устройство с артикулом: {data} не было найдено.", reply_markup=reply_row_menu(["Отмена"]))
            await state.clear()
        
        #If article exists
        else:
            device_info, photo = await get_device_info(data)
            
            if message.from_user.id in await get_users_by_role("worker"):
                await message.answer(device_info, reply_markup=get_redact_menu(data), parse_mode="HTML")
                try:
                    await message.answer_photo(photo, caption=f"Фотография устройства {data}", reply_markup=get_menu())
                except Exception as e:
                    print(f'Exception found while trying to send photo of device: {photo}', file = sys.stderr)
                    await message.answer("Главное меню", reply_markup=get_menu())
            else:
                await message.answer(device_info, parse_mode="HTML")
                try:
                    await message.answer_photo(photo, caption=f"Фотография устройства {data}", reply_markup=get_menu())
                except Exception as e:
                    print(f'Exception found while trying to send photo of device: {photo}', file = sys.stderr)
                    await message.answer("Главное меню", reply_markup=get_menu())
                
            await state.clear()
    else:
        await message.answer(f"Обнаружена ошибка: {data}. Попробуйте ещё раз.", reply_markup=reply_row_menu(["Отмена"]))

"""
Article search
"""

@router.message(F.text=="Поиск по артикулу", RoleCheck("spectator"))
async def article_search(message: types.Message, state: FSMContext):
    await message.answer(f"Введите последние символы артикула (чем больше символов - тем меньше выборка):", reply_markup=reply_row_menu(["Отмена"]))
    await state.set_state(ArticleSearch.article)

@router.message(F.text, RoleCheck("spectator"), ArticleSearch.article)
async def article_process(message: types.Message, state: FSMContext):
    status, answer_text, articles = await multiple_articles(message.text)
    await state.update_data(articles=articles)
    if status:
        await message.answer(answer_text, reply_markup=reply_row_menu(["Отмена"]))
        await state.set_state(ArticleSearch.confirmation)
    else:
        await message.answer(answer_text, reply_markup=get_menu())
        await state.clear()

@router.message(F.text, RoleCheck("spectator"), ArticleSearch.confirmation)
async def confirmation_process(message: types.Message, state: FSMContext):
    data = await state.get_data()
    results = data['articles']
    articleNumber = results[int(message.text)-1]
    if not(await article_guard(articleNumber)):
        #If article doesn't exist
        #If user is worker, then allow them to make records here
        if message.from_user.id in await get_users_by_role("worker"):
            buttons = [types.InlineKeyboardButton(text="Создать новую запись", callback_data=f"create.{articleNumber}")]
            await message.answer(f"Устройство с артикулом: {articleNumber} не было найдено.", reply_markup=inline_row_menu(buttons))
        else:
            await message.answer(f"Устройство с артикулом: {articleNumber} не было найдено.", reply_markup=reply_row_menu(["Отмена"]))
        
    #If article exists
    else:
        device_info, photo = await get_device_info(articleNumber)
        if message.from_user.id in await get_users_by_role("worker"):
            await message.answer(device_info, reply_markup=get_redact_menu(articleNumber), parse_mode="HTML")
            try:
                await message.answer_photo(photo, caption=f"Фотография устройства {articleNumber}", reply_markup=get_menu())
            except Exception as e:
                print(f'Exception found while trying to send photo of device: {photo}', file = sys.stderr)
                await message.answer("Главное меню", reply_markup=get_menu())
        else:
            await message.answer(device_info, parse_mode="HTML")
            try:
                await message.answer_photo(photo, caption=f"Фотография устройства {articleNumber}", reply_markup=get_menu())
            except Exception as e:
                print(f'Exception found while trying to send photo of device: {photo}', file = sys.stderr)
                await message.answer("Главное меню", reply_markup=get_menu())

    await state.clear()