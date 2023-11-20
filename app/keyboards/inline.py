from aiogram import types
import sys
from app.utils.callback_factories import *
from aiogram.utils.keyboard import InlineKeyboardBuilder

def paginator(buttons: list = [], mode: str = "problematic", page: int = 0) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    match mode:
        case "problematic":
            for button in buttons:
                builder.button(
                    text = button['text'], callback_data=RedactProblematicDevice(action=button['action'], articleNumber=button['articleNumber']).pack()
                )
        case "software":
            for button in buttons:
                builder.button(
                    text = button['text'], callback_data=RedactSoftware(action=button['action'], id=button['id']).pack()
                )
        case "notes":
            for button in buttons:
                builder.button(
                    text = button['text'], callback_data=RedactNotes(action=button['action'], id=button['id']).pack()
                )
        case _:
            pass
    
    builder.row(
        types.InlineKeyboardButton(text = "⬅️", callback_data=PaginationValues(action="prev", page=page).pack()),
        types.InlineKeyboardButton(text = "➡️", callback_data=PaginationValues(action="next", page=page).pack())
    )

    builder.adjust(2)
    return builder.as_markup()

def get_software_keyboard(id) -> list:
    buttons = [
        {'text': 'Изменить название', 'action': 'software_change_name', 'id': id},
        {'text': 'Изменить описание', 'action': 'software_change_description', 'id': id},
        {'text': 'Изменить ссылку', 'action': 'software_change_url', 'id': id},
        {'text': 'Удалить', 'action': 'software_delete', 'id': id},
    ]

    return buttons

def get_notes_keyboard(id) -> list:
    buttons = [
        {'text': 'Изменить текст', 'action': 'notes_change_description', 'id': id},
        {'text': 'Удалить', 'action': 'notes_delete', 'id': id},
    ]

    return buttons

def get_problematic_device_keyboard(articleNumber) -> list:
    buttons = [
        {'text': 'Описание проблемы', 'action': 'problematic_change_problem', 'articleNumber': articleNumber}, #p == problematic
        {'text': 'Описание решения', 'action': 'problematic_change_solution', 'articleNumber': articleNumber},
        {'text': 'Удалить', 'action': 'problematic_delete', 'articleNumber': articleNumber},
        {'text': 'Отметить исправленным', 'action': 'problematic_complete', 'articleNumber': articleNumber}
    ]

    return buttons

def get_dashboard_menu() -> InlineKeyboardBuilder:
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

def inline_column_menu(buttons) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    
    for i in range(0, len(buttons)-1, 2):
        builder.row(buttons[i], buttons[i+1])

    if len(buttons)%2==1:
        builder.row(buttons[-1])

    return builder.as_markup()

def inline_row_menu(buttons) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    
    for button in buttons:
        builder.row(button)
    builder.adjust(len(buttons), 0)
    return builder.as_markup()

def get_redact_menu(articleNumber) -> InlineKeyboardBuilder:
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