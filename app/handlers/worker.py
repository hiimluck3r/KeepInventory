import asyncio
import sys
from contextlib import suppress
from aiogram import types, Router, F
from app.loader import dp, bot
from app.keyboards.reply import *
from app.keyboards.inline import *
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from app.filters.role_filter import RoleCheck
from app.states.worker_states import *
from app.db.operations import *
from app.middlewares.articles import *
from app.middlewares.misc import *
from app.utils.callback_factories import RedactDevice, RedactSoftware
from aiogram.exceptions import TelegramBadRequest

router = Router()

"""
Create new device
"""

@router.message(F.text.lower() == "новое устройство", RoleCheck("worker"))
async def new_device_setup(message: types.Message, state: FSMContext):
    await message.answer(f"Введите номер артикула:", reply_markup=reply_row_menu(['Отмена']))
    await state.set_state(NewDevice.article)

@router.message(F.text, RoleCheck("worker"), NewDevice.article)
async def new_device_article_process(message: types.Message, state: FSMContext):
    article = message.text
    if not(await article_guard(article)):
        #If article doesn't exist
        buttons = [types.InlineKeyboardButton(text="Создать новую запись", callback_data=f"create.{article}")]
        await message.answer(f"Устройство с артикулом: {article} не было найдено.", reply_markup=inline_row_menu(buttons))
    else:
        await message.answer(f"Устройство с таким артикулом уже существует.", reply_markup=get_menu())

@router.callback_query(F.data.startswith('create'), RoleCheck("worker"))
async def create_device_callback(callback: types.CallbackQuery, state: FSMContext):
    articleNumber = callback.data.split(".")[1]
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
    try:
        await state.update_data(photo=message.photo[-1].file_id)
    except Exception as e:
        print('Exception at uploading photo for a new device. Using blank instead.', file = sys.stderr)
        await state.update_data(photo='-')
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
    await message.answer(answer_text, reply_markup=get_menu())
    await state.clear()

"""
Devices Manipulation
"""

@router.callback_query(RedactDevice.filter(F.action.startswith("change_")), RoleCheck("worker"))
async def change_device_callback(callback: types.CallbackQuery, state: FSMContext, callback_data: RedactDevice):
    await state.set_state(RedactDeviceState.change)
    action = callback_data.action.split('_')[-1]
    
    answers = {
        'articlenumber': 'Введите новый артикул устройства:',
        'category': 'Введите новую категорию устройства:',
        'subcategory': 'Введите новую подкатегорию устройства:',
        'name': 'Введите новое название устройства:',
        'quantity': 'Введите количество устройств:',
        'productionyear': 'Введите год производства устройства:',
        'accountingyear': 'Введите год постановки устройства на учет:',
        'location': 'Введите фактическое местонахождение устройства:',
        'ownership': 'Введите фактического владельца устройства:',
        'photo': 'Отправьте фотографию устройства:'
    }
    try:
        await callback.message.answer(answers[action], reply_markup=reply_row_menu(["Отмена"]))
        await state.update_data(articleNumber=callback_data.articleNumber, action=action)
    except Exception as e:
        await callback.message.answer(f"Возникла непредвиденная ошибка. Обратитесь к администратору.", reply_markup=reply_row_menu(["Главное меню"]))
    await callback.answer()

@router.message(RedactDeviceState.change, RoleCheck("worker"))
async def change_device_process(message: types.Message, state: FSMContext):
    data = await state.get_data()
    action = data['action']
    articleNumber = data['articleNumber']
    
    is_correct = True #incorrect info will be flagged as false
    sql = None

    if action == 'photo':
        if message.photo is not None:
            photo_id = message.photo[-1].file_id
        else:
            photo_id = '-'
        
        sql = f"UPDATE devices SET {action} = '{photo_id}' WHERE articleNumber = '{data['articleNumber']}'"
        pass
    elif action != 'photo' and message.text is not None:
        if action in ['quantity', 'productionyear', 'accountingyear']:
            sql = f"UPDATE devices SET {action} = {message.text} WHERE articleNumber = '{data['articleNumber']}'"
        else: #article, category, subcategory, etc.
            sql = f"UPDATE devices SET {action} = '{message.text}' WHERE articleNumber = '{data['articleNumber']}'"
    else:
        await message.answer("Ошибка: некорректная информация.", reply_markup=reply_row_menu(['Главное меню']))
        is_correct = False
    
    if is_correct:
        await custom_sql(sql, execute=True)
        await state.clear()
        await message.answer(f"Изменения внесены.", reply_markup=get_menu())

@router.callback_query(RedactDevice.filter(F.action.startswith("delete")), RoleCheck("worker"))
async def delete_device_process(callback: types.CallbackQuery, callback_data = RedactDevice):
    articleNumber = callback_data.articleNumber
    sql = f"DELETE FROM devices WHERE articleNumber = '{articleNumber}'"
    await custom_sql(sql, execute=True)
    await callback.message.answer("Устройство удалено.", reply_markup=get_menu())
    await callback.answer()
    
"""
Problematic Devices Manipulation
"""

@router.callback_query(RedactDevice.filter(F.action == "make_problematic"), RoleCheck("worker"))
async def make_problematic_callback(callback: types.CallbackQuery, state: FSMContext, callback_data = RedactDevice):
    await state.update_data(articleNumber = callback_data.articleNumber, userid = callback.message.chat.id)
    await state.set_state(ProblematicDeviceCreation.description)
    await callback.message.answer("Введите описание проблемы", reply_markup=reply_row_menu(["Отмена"]))
    await callback.answer()

@router.message(ProblematicDeviceCreation.description, RoleCheck("worker"), F.text)
async def make_problematic_process(message: types.Message, state: FSMContext):
    data = await state.get_data()
    sql = f"""INSERT INTO 
    problematicDevices(status, articleNumber, problemDescription, solutionDescription, userid) 
    VALUES(false, '{data['articleNumber']}', '{message.text}', 'Нет решения', {data['userid']}) 
    ON CONFLICT (articleNumber) DO UPDATE SET 
    userid = {data['userid']},
    status = false,
    problemDescription = '{message.text}'"""

    await custom_sql(sql, execute=True)
    await message.answer(f"Устройство {data['articleNumber']} обозначено как проблемное.", reply_markup=get_menu())
    await state.clear()

@router.callback_query(RedactProblematicDevice.filter(F.action == "problematic_change_problem"), RoleCheck("worker"))
async def redact_problem_callback(callback: types.CallbackQuery, state: FSMContext, callback_data = RedactProblematicDevice):
    await state.update_data(articleNumber = callback_data.articleNumber, action = callback_data.action)
    await state.set_state(RedactProblematicDeviceState.change)
    await callback.message.answer("Введите описание проблемы:", reply_markup=reply_row_menu(["Отмена"]))
    await callback.answer()

@router.callback_query(RedactProblematicDevice.filter(F.action == "problematic_change_solution"), RoleCheck("worker"))
async def redact_solution_callback(callback: types.CallbackQuery, state: FSMContext, callback_data = RedactProblematicDevice):
    await state.update_data(articleNumber = callback_data.articleNumber, action = callback_data.action)
    await state.set_state(RedactProblematicDeviceState.change)
    await callback.message.answer("Введите описание решения:", reply_markup=reply_row_menu(["Отмена"]))
    await callback.answer()

@router.message(RedactProblematicDeviceState.change, RoleCheck("worker"))
async def redact_problem_process(message: types.Message, state: FSMContext):
    data = await state.get_data()
    action = data['action'].split('_')[-1] #change action
    articleNumber = data['articleNumber']
    if action == 'solution':
        sql = f"UPDATE problematicDevices SET solutionDescription = '{message.text}' WHERE articleNumber = '{articleNumber}'"
    else:
        sql = f"UPDATE problematicDevices SET problemDescription = '{message.text}' WHERE articleNumber = '{articleNumber}'"
    await custom_sql(sql, execute=True)
    await message.answer("Изменения внесены.", reply_markup=get_menu())
    await state.clear()

@router.callback_query(RedactProblematicDevice.filter(F.action == "problematic_delete"), RoleCheck("worker"))
async def delete_problem_callback(callback: types.CallbackQuery, callback_data = RedactProblematicDevice):
    sql = f"DELETE FROM problematicDevices WHERE articleNumber = '{callback_data.articleNumber}'"
    await custom_sql(sql, execute=True)
    await callback.message.answer("Устройство удалено из списка проблемных.", reply_markup=get_menu())
    await callback.answer()

@router.callback_query(RedactProblematicDevice.filter(F.action == "problematic_complete"), RoleCheck("worker"))
async def complete_problem_callback(callback: types.CallbackQuery, callback_data = RedactProblematicDevice):
    sql = f"UPDATE problematicDevices SET status = true WHERE articleNumber = '{callback_data.articleNumber}'"
    await custom_sql(sql, execute=True)
    await callback.message.answer("Устройство обозначено как исправленное.", reply_markup=get_menu())
    await callback.answer()

"""
Notes
"""

"""
Software
"""

@router.message(F.text.lower() == "программное обеспечение", RoleCheck("worker"))
async def software_menu(message: types.Message):
    await message.answer(f"Здесь вы можете опубликовать свое ПО или найти уже опубликованное другими пользователями.", reply_markup=reply_row_menu(["Опубликовать ПО", "Доступное ПО", "Главное меню"]))

#Create new software record
@router.message(F.text.lower() == "опубликовать по", RoleCheck("worker"))
async def new_software_userid_process(message: types.Message, state: FSMContext):
    await state.update_data(userid = message.from_user.id)
    await state.set_state(NewSoftware.filename)
    await message.answer(f"Введите название ПО", reply_markup=reply_row_menu(["Отмена"]))

@router.message(NewSoftware.filename, RoleCheck("worker"))
async def new_software_name_process(message: types.Message, state: FSMContext):
    await state.update_data(filename = message.text)
    await state.set_state(NewSoftware.fileurl)
    await message.answer(f"Введите ссылку на ПО", reply_markup=reply_row_menu(["Отмена"]))

@router.message(NewSoftware.fileurl, RoleCheck("worker"))
async def new_software_url_process(message: types.Message, state: FSMContext):
    await state.update_data(fileurl = message.text)
    await state.set_state(NewSoftware.description)
    await message.answer(f"Введите описание ПО", reply_markup=reply_row_menu(["Отмена"]))

@router.message(NewSoftware.description, RoleCheck("worker"))
async def new_software_description_process(message: types.Message, state: FSMContext):
    data = await state.get_data()
    description = message.text
    userid = data['userid']
    filename = data['filename']
    fileurl = data['fileurl']

    sql = f"""INSERT INTO software(userid, filename, fileurl, description) 
    VALUES ({userid}, '{filename}', '{fileurl}', '{description}')"""

    await custom_sql(sql, execute=True)
    await state.clear()
    await message.answer(f"Запись внесена", reply_markup=reply_row_menu(["Опубликовать ПО", "Доступное ПО", "Главное меню"]))


#Redact software record
@router.callback_query(RedactSoftware.filter(F.action == "software_change_filename"), RoleCheck("worker"))
async def redact_filename_callback(callback: types.CallbackQuery, state: FSMContext, callback_data = RedactProblematicDevice):
    await state.update_data(software_id = callback_data.id, action = callback_data.action)
    await state.set_state(RedactSoftwareState.change)
    await callback.message.answer("Введите название ПО:", reply_markup=reply_row_menu(["Отмена"]))
    await callback.answer()

@router.callback_query(RedactSoftware.filter(F.action == "software_change_fileurl"), RoleCheck("worker"))
async def redact_fileurl_callback(callback: types.CallbackQuery, state: FSMContext, callback_data = RedactProblematicDevice):
    await state.update_data(software_id = callback_data.id, action = callback_data.action)
    await state.set_state(RedactSoftwareState.change)
    await callback.message.answer("Введите ссылку на ПО:", reply_markup=reply_row_menu(["Отмена"]))
    await callback.answer()

@router.callback_query(RedactSoftware.filter(F.action == "software_change_description"), RoleCheck("worker"))
async def redact_file_description_callback(callback: types.CallbackQuery, state: FSMContext, callback_data = RedactProblematicDevice):
    await state.update_data(software_id = callback_data.id, action = callback_data.action)
    await state.set_state(RedactSoftwareState.change)
    await callback.message.answer("Введите описание ПО:", reply_markup=reply_row_menu(["Отмена"]))
    await callback.answer()

@router.message(RedactSoftwareState.change, RoleCheck("worker"))
async def redact_software_process(message: types.Message, state: FSMContext):
    data = await state.get_data()
    action = data['action'].split('_')[-1] #change action
    software_id = data['software_id']
    if action == 'name':
        sql = f"UPDATE software SET filename = '{message.text}' WHERE id = {software_id}"
    elif action == 'url':
        sql = f"UPDATE software SET fileurl = '{message.text}' WHERE id = {software_id}"
    elif action == 'description':
        sql = f"UPDATE software SET description = '{message.text}' WHERE id = {software_id}"
    else:
        sql = f"SELECT 1 FROM software" #donothing
    await custom_sql(sql, execute=True)
    await message.answer("Изменения внесены.", reply_markup=get_menu())
    await state.clear()

#Delete software record
@router.callback_query(RedactSoftware.filter(F.action == "software_delete"), RoleCheck("worker"))
async def delete_problem_callback(callback: types.CallbackQuery, callback_data = RedactSoftware):
    sql = f"DELETE FROM software WHERE id = '{callback_data.id}'"
    await custom_sql(sql, execute=True)
    await callback.message.answer("Выбранное ПО было удалено.", reply_markup=get_menu())
    await callback.answer()

#Software carousel menu
@router.message(F.text.lower() == "доступное по", RoleCheck("worker"))
async def software_uploaded_menu(message: types.Message, state: FSMContext):
    software = await get_software()
    if software != None:
        software_id = software[0]['id']
        await state.set_state(Software.init)
        keyboard = get_software_keyboard(software_id)
        await message.answer(await get_software_info(software_id), reply_markup=paginator(keyboard, "software", 0), parse_mode="HTML")
    else:
        await message.answer("На данный момент программное обеспечение отсутствует.", reply_markup=reply_row_menu(["Опубликовать ПО", "Главное меню"]))

@dp.callback_query(Software.init, PaginationValues.filter(F.action.in_(["next", "prev"])), RoleCheck("spectator"))
async def software_uploaded_pageswap(callback: types.CallbackQuery, callback_data: PaginationValues):
    software = await get_software()
    if software == None:
        await message.answer("На данный момент программное обеспечение отсутствует.", reply_markup=reply_row_menu(["Опубликовать ПО", "Главное меню"]))
    else:
        current_page = int(callback_data.page)
        page = None

        if callback_data.action == "prev":
            page = current_page-1 if current_page>0 else len(software)-1 #previous page
        else:
            page = current_page+1 if current_page<(len(software)-1) else 0 #next page
        
        with suppress(TelegramBadRequest):
            software_id = software[page]['id']
            keyboard = get_software_keyboard(software_id)
            await callback.message.edit_text(
                await get_software_info(software_id),
                reply_markup=paginator(keyboard, "software", page),
                parse_mode="HTML"
            )
    await callback.answer()
