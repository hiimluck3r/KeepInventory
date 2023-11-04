import asyncio
import os
import sys
from aiogram import types, Router, F
from app.loader import dp, bot
from app.roles import spectator, worker
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

router = Router()


"""
Cancel FSMContext event
"""
@router.message(Command(commands=["cancel"]))
@router.message(F.text.lower() == "отмена")
async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="Действие отменено.",
        reply_markup=get_menu()
    )
"""
/users

Gives you a list with all users, including root
template: *nickname* - *userid* - *role*
"""
@router.message(Command("users"), F.from_user.id.in_(spectator))
async def users_list(message: types.Message, command: CommandObject):
    users = await custom_sql("SELECT * FROM users", fetch=True)
    result = f"Список пользователей:"
    result += f"\n{await get_username(ROOT)} - {ROOT} - ROOT"
    for row in users:
        result+=f"\n{await get_username(row[1])} - {row[1]} - {row[2]}"
    await message.answer(result)

"""
Barcode search
"""

@router.message(F.text=="Поиск по штрих-коду", F.from_user.id.in_(spectator))
async def barcode_search(message: types.Message, state: FSMContext):
    await message.answer(f"Пришлите фотографию, на которой чётко видно штрих-код", reply_markup=reply_row_menu(["Отмена"]))
    await state.set_state(BarcodeImage.image)

@router.message(F.from_user.id.in_(spectator), F.photo, BarcodeImage.image)
async def barcode_processing(message: types.Message, state: FSMContext):
    filepath = f"app/temp/{message.from_user.id}.jpg"
    await bot.download(message.photo[-1], destination = filepath)
    status, data = await get_code(filepath) #if successful, then data == articleNumber
    os.remove(filepath)
    if status == 0:
        if not(article_guard(data)):
            #If article doesn't exist
            #If user is worker, then allow them to make records here
            if message.from_user.id in worker:
                buttons = [types.InlineKeyboardButton(text="Создать новую запись", callback_data=f"create.{data}")]
                await message.answer(f"Устройство с артикулом: {data} не было найдено.", reply_markup=inline_row_menu(buttons))
            else:
                await message.answer(f"Устройство с артикулом: {data} не было найдено.", reply_markup=reply_row_menu(["Отмена"]))
        
        #If article exists
        else:
            device_info = get_device_info(data)
            await message.answer(device_info, reply_markup=get_menu())
            await state.clear()
    else:
        await message.answer(f"Обнаружена ошибка: {data}. Попробуйте ещё раз.", reply_markup=reply_row_menu(["Отмена"]))

"""
Article search
"""

@router.message(F.text=="Поиск по артикулу", F.from_user.id.in_(spectator))
async def article_search(message: types.Message, state: FSMContext):
    await message.answer(f"Введите последние символы артикула (чем больше символов - тем меньше выборка):", reply_markup=reply_row_menu(["Отмена"]))
    await state.set_state(ArticleSearch.article)

@router.message(F.text, F.from_user.id.in_(spectator), ArticleSearch.article)
async def article_process(message: types.Message, state: FSMContext):
    sql = f"SELECT articleNumber FROM devices WHERE articleNumber ILIKE '%{message.text}'"
    results = await custom_sql(sql, fetch=True)
    if len(results) == 0:
        #this is just bad, I need to refactor this asap
        await message.answer(f"Артикулов с подстрокой {message.text} не найдено.", reply_markup=get_menu())
        await state.clear()
    else:
        answer_text = f"Артикулы с подстрокой {message.text}:\n"
        await state.update_data(articles=results)
        for index, item in enumerate(results):
            answer_text+=f"{index+1}. {item}\n"
        answer_text+=f"\nВведите номер интересующего вас артикула:"
        await message.answer(answer_text, reply_markup=reply_row_menu(["Отмена"]))
        await state.set_state(ArticleSearch.confirmation)

@router.message(F.text, F.from_user.id.in_(spectator), ArticleSearch.confirmation)
async def confirmation_process(message: types.Message, state: FSMContext):
    data = await state.get_data()
    results = data['articles']
    try:
        index = int(message.text)
        await message.answer(f"Код: {results[index-1]}", reply_markup=get_menu())
    except Exception as e:
        await message.answer(f"Ошибка! Что-то явно пошло не так, перепроверьте вводимые данные.", reply_markup=get_menu())
        await message.answer(f"Found an exception at confirmation_process: {e}")
    state.clear()

"""
todo
"""