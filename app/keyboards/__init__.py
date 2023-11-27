from aiogram import types
from app.loader import bot

async def get_username(user_id):
    try:
        chat = await bot.get_chat(user_id)
        username = chat.username
        return f"@{username}"
    except Exception as e:
        print("Error while getting username:", e)
        return "@404n0tF0uNd"