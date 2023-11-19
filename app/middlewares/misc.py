from app.db.operations import *
from app.keyboards import get_username

async def get_software():
    sql = f"SELECT id FROM software"
    articles = await custom_sql(sql, fetch=True)

    return articles

async def get_software_info(id):
    device_info = ''
    sql = f"""SELECT * FROM software WHERE id = id
    """
    data = await custom_sql(sql, fetchrow=True)
    filename = data['filename']
    fileurl = data['fileurl'] #20 or 50mb limit made me do so (I don't want to setup local api... yet)
    description = data['description']
    user = await get_username(data['userid'])

    device_info+=f"<b>{filename}</b>\n\n"
    device_info+=f"Описание: {description}\n"
    device_info+=f"Ссылка: {fileurl}\n\n"
    device_info+=f"Выложил: {user}"

    return device_info
