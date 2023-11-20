from app.db.operations import *
from app.keyboards import get_username
import sys

async def article_guard(articleNumber):
    sql = f"SELECT EXISTS(SELECT 1 FROM devices WHERE articleNumber = '{articleNumber}')"
    result = await custom_sql(sql, fetchval=True)
    print(f"Result: {result}", file=sys.stderr)
    return result == True

async def problematic_device_guard(articleNumber):
    sql = f"SELECT EXISTS(SELECT 1 FROM problematicDevices WHERE articleNumber = '{articleNumber}')"
    result = await custom_sql(sql, fetchval=True)
    print(f"Result: {result}", file=sys.stderr)
    return result == True

async def get_device_info(articleNumber):
    sql = f"SELECT * FROM devices WHERE articleNumber = '{articleNumber}'"
    result = await custom_sql(sql, fetchrow=True)
    print(f"resulting row at the device info is: {result}", file=sys.stderr)
    device_info = f"Информация об устройстве: {articleNumber}\n"
    
    device_info+=f"\nID устройства: {result['id']}"
    device_info+=f"\nАртикул: {result['articlenumber']}"
    device_info+=f"\nКатегория: {result['category']}"
    device_info+=f"\nПодкатегория: {result['subcategory']}"
    device_info+=f"\nНазвание: {result['name']}"
    device_info+=f"\nКоличество (шт.): {result['quantity']}"
    device_info+=f"\nГод производства: {result['productionyear']}"
    device_info+=f"\nГод постановки на учёт: {result['accountingyear']}"
    device_info+=f"\nМестонахождение: {result['location']}"
    device_info+=f"\nВладение: {result['ownership']}"
    
    if (await problematic_device_guard(articleNumber)):
        device_info+=f'\n\n<b>Является "проблемным" устройством.</b>'

    return device_info, result['photo']

async def multiple_articles(articleNumberIncomplete):
    sql = f"SELECT articleNumber FROM devices WHERE articleNumber ILIKE '%{articleNumberIncomplete}'"
    articles = await custom_sql(sql, fetch=True)
    if not articles:
        return False, f"Артикулов с подстрокой {articleNumberIncomplete} не найдено.", []
    articles_clear = []
    answer_text = f"Артикулы с подстрокой {articleNumberIncomplete}:\n"
    for i in range(len(articles)):
        item = articles[i]['articlenumber']
        articles_clear.append(item)
        answer_text+=f"{i+1}. {item}\n"
    answer_text+=f"\nВведите номер интересующего вас артикула:"
    return True, answer_text, articles_clear

async def get_problematic_devices():
    sql = "SELECT articleNumber FROM problematicDevices"
    return await custom_sql(sql, fetch=True)

async def get_problematic_device_info(articleNumber):
    device_info = ''
    sql = f"""SELECT * FROM problematicDevices WHERE articleNumber = '{articleNumber}'
    """
    data = await custom_sql(sql, fetchrow=True)
    status = data['status']
    problemDescription = data['problemdescription']
    solutionDescription = data['solutiondescription']
    user = await get_username(data['userid'])

    device_info+=f"Артикул: {articleNumber}\n"

    device_info += "Статус: Исправлено\n" if status else "Статус: В работе\n"
    device_info+=f"\nОписание проблемы: {problemDescription}\n"
    device_info+=f"\nРешение проблемы: {solutionDescription}\n"
    device_info+=f"Работает: {user}"

    return device_info
