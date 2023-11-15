import asyncio
from aiogram import types, Router, F
from app.loader import dp, bot
from app import greet_stranger_text, greet_user_text
from app.keyboards.reply import reply_column_menu, reply_row_menu
from app.keyboards.inline import inline_column_menu, inline_row_menu
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from app.filters.role_filter import RoleCheck
from app.states.worker_states import *
from app.db.operations import *

router = Router()

@router.callback_query(F.data.startswith('create'), RoleCheck("worker"))
async def create_device_callback(callback: types.CallbackQuery, state: FSMContext):
    articleNumber = int(callback.data.split(".")[1])
    await state.update_data(articleNumber=articleNumber)
    await state.set_state(NewDevice.category)

    await callback.message.answer(f"Укажите категорию устройства:", reply_markup=reply_row_menu(["Отмена"]))
    await callback.answer()

@router.callback_query(NewDevice.category, RoleCheck("worker"), F.text)
async def create_device_category_callback(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(category=callback.message.text)
    await state.set_state(subcategory)

    await callback.message.answer(f"Укажите категорию устройства:", reply_markup=reply_row_menu(["Отмена"]))
    await callback.answer()

@router.callback_query(NewDevice.subcategory, RoleCheck("worker"), F.text)
async def create_device_subcategory_callback(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(subcategory=callback.message.text)
    await state.set_state(name)

    await callback.message.answer(f"Укажите название устройства:", reply_markup=reply_row_menu(["Отмена"]))
    await callback.answer()

@router.callback_query(NewDevice.name, RoleCheck("worker"), F.text)
async def create_device_name_callback(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(name=callback.message.text)
    await state.set_state(quantity)

    await callback.message.answer(f"Укажите количество устройств:", reply_markup=reply_row_menu(["Отмена"]))
    await callback.answer()

@router.callback_query(NewDevice.quantity, RoleCheck("worker"), F.text)
async def create_device_quantity_callback(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(quantity=callback.message.text)
    await state.set_state(productionYear)

    await callback.message.answer(f"Укажите год производства устройства:", reply_markup=reply_row_menu(["Отмена"]))
    await callback.answer()

@router.callback_query(NewDevice.productionYear, RoleCheck("worker"), F.text)
async def create_device_productionYear_callback(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(productionYear=callback.message.text)
    await state.set_state(accountingYear)

    await callback.message.answer(f"Укажите год постановки устройства на учёт:", reply_markup=reply_row_menu(["Отмена"]))
    await callback.answer()

@router.callback_query(NewDevice.accountingYear, RoleCheck("worker"), F.text)
async def create_device_accountingYear_callback(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(accountingYear=callback.message.text)
    await state.set_state(location)

    await callback.message.answer(f"Укажите фактическое местонахождение устройства (прим. 404/1):", reply_markup=reply_row_menu(["Отмена"]))
    await callback.answer()

@router.callback_query(NewDevice.location, RoleCheck("worker"), F.text)
async def create_device_location_callback(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(location=callback.message.text)
    await state.set_state(ownership)

    await callback.message.answer(f"Укажите владельца устройства:", reply_markup=reply_row_menu(["Отмена"]))
    await callback.answer()

@router.callback_query(NewDevice.ownership, RoleCheck("worker"), F.text)
async def create_device_ownership_callback(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(location=callback.message.text)
    await state.set_state(photo)

    await callback.message.answer(f"Прикрепите фотографию устройства. Если таковой нет, отправьте любое текстовое сообщение:", reply_markup=reply_row_menu(["Отмена"]))
    await callback.answer()

@router.callback_query(NewDevice.photo, RoleCheck("worker"))
async def create_device_photo_callback(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(photo=callback.message.text)
    await state.set_state(confirmation)
    data = await state.get_data()
    answer_text = f"Вы собираетесь создать новое устройство:\n"

    answer_text+=f"\nID устройства: {data['id']}"
    answer_text+=f"\nАртикул: {data['articleNumber']}"
    answer_text+=f"\nКатегория: {data['category']}"
    answer_text+=f"\nПодкатегория: {data['subcategory']}"
    answer_text+=f"\nНазвание: {data['name']}"
    answer_text+=f"\nКоличество (шт.): {data['quantity']}"
    answer_text+=f"\nГод производства: {data['productionYear']}"
    answer_text+=f"\nГод постановки на учёт: {data['accoutingYear']}"
    answer_text+=f"\nМестонахождение: {data['location']}"
    answer_text+=f"\nВладение: {data['ownership']}"

    answer_text+=f"\n\nОтправьте 'Да' (в любом регистре) для подтверждения своих действий."
    await callback.message.answer(answer_text, reply_markup=reply_row_menu(["Отмена"]))
    await callback.answer()

@router.callback_query(NewDevice.confirmation, RoleCheck("worker"), F.text.lower()=="да")
async def create_device_confirmation_callback(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    sql = f"""INSERT INTO devices(articleNumber, 
    category, subcategory, 
    name, quantity, productionYear, 
    accoutingYear, location, 
    ownership, photo)
    VALUES ('{data['articleNumber']}', '{data['category']}', '{data['subcategory']}', 
    '{data['name']}', {data['quantity']}, {data['productionYear']}, 
    {data['accountingYear']}, '{data['location']}', '{data['ownership']}', 
    '{data['photo']}')""" #that's a mess, ngl, but you should deal with it

    try:
        await custom_sql(sql, execute=True)
    except Exception as e:
        answer_text = f"Возникла ошибка при создании записи: {e}"
    await callback.message.answer(answer_text, reply_markup=reply_row_menu(["Главное меню"]))
    await state.clear()
    await callback.answer()