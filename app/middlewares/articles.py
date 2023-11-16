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
    
    #photoURL should be here but not yet
    if (await problematic_device_guard(articleNumber)):
        device_info+=f'\n\n<b>Является "проблемным" устройством.</b>'

    return device_info

async def multiple_articles(articleNumberIncomplete):
    sql = f"SELECT articleNumber FROM devices WHERE articleNumber ILIKE '%{articleNumberIncomplete}'"
    articles = await custom_sql(sql, fetch=True)
    if articles:
        articles_clear = []
        answer_text = f"Артикулы с подстрокой {articleNumberIncomplete}:\n"
        for i in range(len(articles)):
            item = articles[i]['articlenumber']
            articles_clear.append(item)
            answer_text+=f"{i+1}. {item}\n"
        answer_text+=f"\nВведите номер интересующего вас артикула:"
        return True, answer_text, articles_clear
    else:
        return False, f"Артикулов с подстрокой {articleNumberIncomplete} не найдено.", []