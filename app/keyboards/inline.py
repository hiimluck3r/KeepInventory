from aiogram import types
import sys
from app.utils.callback_factories import *
from aiogram.utils.keyboard import InlineKeyboardBuilder

def paginator(buttons: list = [], page: int = 0) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    for button in buttons:
        builder.button(
            text = button['text'], callback_data=RedactProblematicDevice(action=button['action'], articleNumber=button['articleNumber']).pack()
        )
    
    builder.row(
        types.InlineKeyboardButton(text = "⬅️", callback_data=PaginationValues(action="prev", page=page).pack()),
        types.InlineKeyboardButton(text = "➡️", callback_data=PaginationValues(action="next", page=page).pack())
    )

    builder.adjust(2)
    return builder.as_markup()

def get_problematic_device_keyboard(articleNumber):
    buttons = [
        {'text': 'Описание проблемы', 'action': 'change_problem', 'articleNumber': articleNumber},
        {'text': 'Описание решения', 'action': 'change_solution', 'articleNumber': articleNumber},
        {'text': 'Удалить', 'action': 'delete', 'articleNumber': articleNumber},
        {'text': 'Отметить исправленным', 'action': 'complete', 'articleNumber': articleNumber}
    ]

    return buttons

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
        {'text': 'Артикул', 'action': 'change_articlenumber', 'articleNumber': articleNumber},
        {'text': 'Категория', 'action': 'change_category', 'articleNumber': articleNumber},
        {'text': 'Подкатегория', 'action': 'change_subcategory', 'articleNumber': articleNumber},
        {'text': 'Название', 'action': 'change_name', 'articleNumber': articleNumber},
        {'text': 'Количество', 'action': 'change_quantity', 'articleNumber': articleNumber},
        {'text': 'Год производства', 'action': 'change_productionyear', 'articleNumber': articleNumber},
        {'text': 'Год начала учёта', 'action': 'change_accountingyear', 'articleNumber': articleNumber},
        {'text': 'Местонахождение', 'action': 'change_location', 'articleNumber': articleNumber},
        {'text': 'Владение', 'action': 'change_ownership', 'articleNumber': articleNumber},
        {'text': 'Фотография', 'action': 'change_photo', 'articleNumber': articleNumber},
        {'text': 'Удалить устройство', 'action': 'delete', 'articleNumber': articleNumber},
        {'text': 'Проблемное устройство', 'action': 'make_problematic', 'articleNumber': articleNumber}
    ]
    for button in buttons:
        builder.button(
            text = button['text'], callback_data=RedactDevice(action=button['action'], articleNumber=button['articleNumber']).pack()
        )
    builder.adjust(2)
    
    return builder.as_markup()