from aiogram import types
from app.utils.callback_factories import *
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_dashboard_menu():
    builder = InlineKeyboardBuilder()
    buttons = [
        types.InlineKeyboardButton(text="Изменить greet_user", callback_data="changegreet_user"),
        types.InlineKeyboardButton(text="Изменить greet_stranger", callback_data="changegreet_stranger"),
        types.InlineKeyboardButton(text="Сделать бэкап", callback_data="backup_download"),
        #types.InlineKeyboardButton(text="Загрузить бэкап", callback_data="backup_upload"), #todo
        types.InlineKeyboardButton(text="Просмотреть логи", callback_data="logs")
    ]
    
    for i in range(0, len(buttons)-1, 2):
        builder.row(buttons[i], buttons[i+1])

    if len(buttons)%2==1:
        builder.row(buttons[-1])

    return builder.as_markup()

def inline_column_menu(buttons):
    builder = InlineKeyboardBuilder()
    
    for i in range(0, len(buttons)-1, 2):
        builder.row(buttons[i], buttons[i+1])

    if len(buttons)%2==1:
        builder.row(buttons[-1])

    return builder.as_markup()

def inline_row_menu(buttons):
    builder = InlineKeyboardBuilder()
    
    for button in buttons:
        builder.row(button)
    builder.adjust(len(buttons), 0)
    return builder.as_markup()

def get_redact_menu(articleNumber):
    builder = InlineKeyboardBuilder()
    buttons = [
        {'name': 'Артикул', 'action': 'change_articlenumber', 'articleNumber': articleNumber},
        {'name': 'Категория', 'action': 'change_category', 'articleNumber': articleNumber},
        {'name': 'Подкатегория', 'action': 'change_subcategory', 'articleNumber': articleNumber},
        {'name': 'Название', 'action': 'change_name', 'articleNumber': articleNumber},
        {'name': 'Количество', 'action': 'change_quantity', 'articleNumber': articleNumber},
        {'name': 'Год производства', 'action': 'change_productionyear', 'articleNumber': articleNumber},
        {'name': 'Год начала учёта', 'action': 'change_accountingyear', 'articleNumber': articleNumber},
        {'name': 'Местонахождение', 'action': 'change_location', 'articleNumber': articleNumber},
        {'name': 'Владение', 'action': 'change_ownership', 'articleNumber': articleNumber},
        {'name': 'Фотография', 'action': 'change_photo', 'articleNumber': articleNumber},
        {'name': 'Удалить устройство', 'action': 'delete', 'articleNumber': articleNumber}
    ]
    for button in buttons:
        builder.button(
            text = button['name'], callback_data=RedactDevice(action=button['action'], articleNumber=button['articleNumber']).pack()
        )
    builder.adjust(2)
    return builder.as_markup()