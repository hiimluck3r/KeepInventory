import os
import sys

from aiogram import types
from bot.dispatcher import bot

def goto_menu():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton(text="Главное меню")
    keyboard.add(button)

    return keyboard

def get_main_menu():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Все записи", "Определенная запись"]
    keyboard.add(*buttons)
    buttons = ["Поиск по кабинету", "Новая запись"]
    keyboard.add(*buttons) 

    return keyboard

def get_specific_entry():
    
    return

def get_all_entries():

    return

def by_cabinet_entry():

    return

def new_entry():

    return