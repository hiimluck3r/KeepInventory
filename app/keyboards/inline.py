from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_dashboard_menu():
    builder = InlineKeyboardBuilder()
    buttons = [
        types.InlineKeyboardButton(text="Изменить greet_user.txt", callback_data="changegreet_user"), #желательно заменить названия файлов на норм слова
        types.InlineKeyboardButton(text="Изменить greet_stranger.txt", callback_data="changegreet_stranger"),
        types.InlineKeyboardButton(text="Сделать бэкап", callback_data="backup_download"), #.csv? pg_dumpall?
        types.InlineKeyboardButton(text="Загрузить бэкап", callback_data="backup_upload"),
        types.InlineKeyboardButton(text="Просмотреть логи", callback_data="logs")
    ]
    
    for i in range(0, len(buttons), 2):
        builder.row(buttons[i], buttons[i+1])

    if len(buttons)%2==1:
        builder.row(buttons[i-1])

    return builder.as_markup()