import asyncio
import sys
from aiogram import types, Router, F
from app.loader import dp, bot
from app import greet_stranger_text, greet_user_text
from app.keyboards.reply import reply_column_menu, reply_row_menu
from app.keyboards.inline import inline_column_menu, inline_row_menu
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from app.filters.role_filter import RoleCheck
from app.states.worker_states import *
from app.db.operations import *

router = Router()

"""
Create new device
"""

@router.callback_query(F.data.startswith('create'), RoleCheck("worker"))
async def create_device_callback(callback: types.CallbackQuery, state: FSMContext):
    articleNumber = int(callback.data.split(".")[1])
    await state.update_data(articleNumber=articleNumber)
    await state.set_state(NewDevice.category)
    await callback.message.answer(f"Укажите категорию устройства:", reply_markup=reply_row_menu(["Отмена"]))
    await callback.answer()

@router.message(NewDevice.category, RoleCheck("worker"), F.text)
async def create_device_category_callback(message: types.Message, state: FSMContext):
    await state.update_data(category=message.text)
    await state.set_state(NewDevice.subcategory)

    await message.answer(f"Укажите подкатегорию устройства:", reply_markup=reply_row_menu(["Отмена"]))

@router.message(NewDevice.subcategory, RoleCheck("worker"), F.text)
async def create_device_subcategory_callback(message: types.Message, state: FSMContext):
    await state.update_data(subcategory=message.text)
    await state.set_state(NewDevice.name)

    await message.answer(f"Укажите название устройства:", reply_markup=reply_row_menu(["Отмена"]))

@router.message(NewDevice.name, RoleCheck("worker"), F.text)
async def create_device_name_callback(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(NewDevice.quantity)

    await message.answer(f"Укажите количество устройств:", reply_markup=reply_row_menu(["Отмена"]))

@router.message(NewDevice.quantity, RoleCheck("worker"), F.text)
async def create_device_quantity_callback(message: types.Message, state: FSMContext):
    await state.update_data(quantity=message.text)
    await state.set_state(NewDevice.productionYear)

    await message.answer(f"Укажите год производства устройства:", reply_markup=reply_row_menu(["Отмена"]))

@router.message(NewDevice.productionYear, RoleCheck("worker"), F.text)
async def create_device_productionYear_callback(message: types.Message, state: FSMContext):
    await state.update_data(productionYear=message.text)
    await state.set_state(NewDevice.accountingYear)

    await message.answer(f"Укажите год постановки устройства на учёт:", reply_markup=reply_row_menu(["Отмена"]))

@router.message(NewDevice.accountingYear, RoleCheck("worker"), F.text)
async def create_device_accountingYear_callback(message: types.Message, state: FSMContext):
    await state.update_data(accountingYear=message.text)
    await state.set_state(NewDevice.location)

    await message.answer(f"Укажите фактическое местонахождение устройства (прим. 404/1):", reply_markup=reply_row_menu(["Отмена"]))

@router.message(NewDevice.location, RoleCheck("worker"), F.text)
async def create_device_location_callback(message: types.Message, state: FSMContext):
    await state.update_data(location=message.text)
    await state.set_state(NewDevice.ownership)

    await message.answer(f"Укажите владельца устройства:", reply_markup=reply_row_menu(["Отмена"]))

@router.message(NewDevice.ownership, RoleCheck("worker"), F.text)
async def create_device_ownership_callback(message: types.Message, state: FSMContext):
    await state.update_data(ownership=message.text)
    await state.set_state(NewDevice.photo)

    await message.answer(f"Прикрепите фотографию устройства. Если таковой нет, отправьте любое текстовое сообщение:", reply_markup=reply_row_menu(["Отмена"]))

@router.message(NewDevice.photo, RoleCheck("worker"))
async def create_device_photo_callback(message: types.Message, state: FSMContext):
    await state.update_data(photo=message.text)
    await state.set_state(NewDevice.confirmation)
    data = await state.get_data()
    answer_text = f"Вы собираетесь создать новое устройство:\n"

    answer_text+=f"\nАртикул: {data['articleNumber']}"
    answer_text+=f"\nКатегория: {data['category']}"
    answer_text+=f"\nПодкатегория: {data['subcategory']}"
    answer_text+=f"\nНазвание: {data['name']}"
    answer_text+=f"\nКоличество (шт.): {data['quantity']}"
    answer_text+=f"\nГод производства: {data['productionYear']}"
    answer_text+=f"\nГод постановки на учёт: {data['accountingYear']}"
    answer_text+=f"\nМестонахождение: {data['location']}"
    answer_text+=f"\nВладение: {data['ownership']}"

    answer_text+=f"\n\nОтправьте 'Да' (в любом регистре) для подтверждения своих действий."
    await message.answer(answer_text, reply_markup=reply_row_menu(["Отмена"]))

@router.message(NewDevice.confirmation, RoleCheck("worker"), F.text.lower()=="да")
async def create_device_confirmation_callback(message: types.Message, state: FSMContext):
    data = await state.get_data()
    sql = f"""INSERT INTO devices(articleNumber, 
    category, subcategory, 
    name, quantity, productionYear, 
    accountingYear, location, 
    ownership, photo)
    VALUES ('{data['articleNumber']}', '{data['category']}', '{data['subcategory']}', 
    '{data['name']}', {data['quantity']}, {data['productionYear']}, 
    {data['accountingYear']}, '{data['location']}', '{data['ownership']}', 
    '{data['photo']}')""" #that's a mess, ngl, but you should deal with it

    try:
        await custom_sql(sql, execute=True)
        answer_text = f"Запись внесена."
    except Exception as e:
        answer_text = f"Возникла ошибка при создании записи: {e}"
    await message.answer(answer_text, reply_markup=reply_row_menu(["Главное меню"]))
    await state.clear()

"""
Create new note record
"""

"""
Create new software record
"""

"""
Devices Manipulation
"""

"""
Problematic Devices Manipulation
"""