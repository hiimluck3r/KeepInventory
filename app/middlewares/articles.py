from app.db.operations import *
import sys

async def article_guard(articleNumber):
    sql = f"SELECT EXISTS(SELECT 1 FROM devices WHERE articleNumber = '{articleNumber}')"
    result = await custom_sql(sql, fetchval=True)
    print(f"Result: {result}", file=sys.stderr)
    if result==True:
        return True
    else:
        return False

async def problematic_device_guard(articleNumber):
    sql = f"SELECT EXISTS(SELECT 1 FROM problematicDevices WHERE articleNumber = '{articleNumber}')"
    result = await custom_sql(sql, fetchval=True)
    print(f"Result: {result}", file=sys.stderr)
    if result==True:
        return True
    else:
        return False

async def get_device_info(articleNumber):
    sql = f"SELECT * FROM devices WHERE articleNumber = '{articleNumber}'"
    result = await custom_sql(sql, fetchrow=True)
    print(f"resulting row at the device info is: {result}", file=sys.stderr)
    device_info = f"Информация об устройстве: {articleNumber}\n"
    
    device_info+=f"\nID устройства: {result[0]}"
    device_info+=f"\nАртикул: {result[1]}"
    device_info+=f"\nКатегория: {result[2]}"
    device_info+=f"\nПодкатегория: {result[3]}"
    device_info+=f"\nНазвание: {result[4]}"
    device_info+=f"\nКоличество (шт.): {result[5]}"
    device_info+=f"\nГод производства: {result[6]}"
    device_info+=f"\nГод постановки на учёт: {result[7]}"
    device_info+=f"\nМестонахождение: {result[8]}"
    #photoURL should be here but not yet
    if (await problematic_device_guard(articleNumber)):
        device_info+=f'\n\n<b>Является "проблемным" устройством.</b>'

    return device_info

async def multiple_articles(articleNumberIncomplete):
    sql = f"SELECT articleNumber FROM devices WHERE articleNumber ILIKE '%{articleNumberIncomplete}'"
    articles = await custom_sql(sql, fetch=True)
    
    if articles:
        answer_text = f"Артикулы с подстрокой {message.text}:\n"
        for i in range(len(articles)):
            index = articles[i]['id']
            item = articles[i]['articleNumber']
            answer_text+=f"{index+1}. {item}\n"
        answer_text+=f"\nВведите номер интересующего вас артикула:"
        return True, answer_text
    else:
        return False, f"Артикулов с подстрокой {message.text} не найдено."