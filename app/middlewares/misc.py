from app.db.operations import *
from app.keyboards import get_username
from os import walk

async def get_software():
    sql = "SELECT id FROM software"
    return await custom_sql(sql, fetch=True)

async def get_software_info(id):
    software_info = ''
    sql = f"""SELECT * FROM software WHERE id = {id}
    """
    data = await custom_sql(sql, fetchrow=True)
    filename = data['filename']
    fileurl = data['fileurl'] #20 or 50mb limit made me do so (I don't want to setup local api... yet)
    description = data['description']
    user = await get_username(data['userid'])

    software_info+=f"<b>{filename}</b>\n\n"
    software_info+=f"Описание: {description}\n"
    software_info+=f"Ссылка: {fileurl}\n\n"
    software_info+=f"Выложил: {user}"

    return software_info

async def get_notes():
    sql = "SELECT id FROM notes"
    return await custom_sql(sql, fetch=True)

async def get_notes_info(id):
    notes_info = ''
    sql = f"SELECT * FROM notes WHERE id = {id}"
    data = await custom_sql(sql, fetchrow=True)
    header = data['header']
    description = data['header']
    user = await get_username(data['userid'])

    notes_info+=f"<b>{header}</b>\n\n"
    notes_info+=f"{description}\n\n"
    notes_info+=f"Выложил: {user}"

    return notes_info

def get_filenames(path):
    logs = []
    for (dirpath, dirnames, filenames) in walk(path):
        logs.extend(filenames)
        break
    
    return logs