from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_dashboard_menu():
    builder = InlineKeyboardBuilder()
    buttons = [
        types.InlineKeyboardButton(text="Изменить greet_user.txt", callback_data="changegreet_user"), #желательно заменить названия файлов на норм слова
        types.InlineKeyboardButton(text="Изменить greet_stranger.txt", callback_data="changegreet_stranger"),
        types.InlineKeyboardButton(text="Сделать бэкап", callback_data="backup_download"), #.csv? pg_dumpall?
        types.InlineKeyboardButton(text="Загрузить бэкап", callback_data="backup_upload")
    ]
    
    builder.row(buttons[0], buttons[1])
    builder.row(buttons[2], buttons[3])

    return builder.as_markup()