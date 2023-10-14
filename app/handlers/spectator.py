import asyncio
import os
from aiogram import types, Router, F
from app.dispatcher import dp, bot
from app.roles import spectator
from app import ROOT
from app.keyboards.reply import *
from app.keyboards.inline import get_dashboard_menu
from aiogram.filters.command import Command
from app.barcodes.barcode_reader import get_code
from app.states.spectator_states import BarcodeImage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

router = Router()

@router.message(F.text=="Поиск по штрих-коду", F.from_user.id.in_(spectator))
async def barcode_search(message: types.Message, state: FSMContext):
    await message.answer(f"Пришлите фотографию, на которой чётко видно штрих-код", reply_markup=reply_row_menu(["Главное меню"]))
    await state.set_state(BarcodeImage.image)

@router.message(F.from_user.id.in_(spectator), F.photo, BarcodeImage.image)
async def barcode_processing(message: types.Message, state: FSMContext):
    filepath = f"app/temp/{message.from_user.id}.jpg"
    #await state.update_data(photo = message.photo[-1])
    await bot.download(message.photo[-1], destination = filepath)
    status, data = await get_code(filepath)
    if status == 0:
        await message.answer(f"Код: {data}", reply_markup=reply_row_menu(["Главное меню"]))
        os.remove(filepath)
        await state.clear()
    else:
        await message.answer(f"Обнаружена ошибка: {data}. Попробуйте ещё раз.", reply_markup=reply_row_menu(["Главное меню"]))