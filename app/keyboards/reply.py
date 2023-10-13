from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def stranger_menu():
    buttons = ["Контакты", "GitHub"]
    builder = ReplyKeyboardBuilder()
    for button in buttons:
        builder.add(types.KeyboardButton(text = button))
    builder.adjust(2)

    return builder.as_markup(resize_keyboard=True)

def main_menu():
    buttons = ["Поиск по штрих-коду", "Поиск по номеру",
    "Поиск по аудитории", "Заметки", "Программное обеспечение",
    "Проблемные устройства"]
    builder = ReplyKeyboardBuilder()
    for button in buttons:
        builder.add(types.KeyboardButton(text = button))
    builder.adjust(2)

    return builder.as_markup(resize_keyboard=True)