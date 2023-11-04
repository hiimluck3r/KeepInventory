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
    sql = f"SELECT 1 FROM devices WHERE articleNumber = '{articleNumber}'"
    result = await custom_sql(sql, fetchrow=True)
    device_info = f"Информация об устройстве: {articleNumber}\n"
    device_attributes = [device_id, articleNumber, category, subcategory, name, quantity, productionYear, accountingYear, location, ownership, photo]
    for index, attribute in enumerate(device_attributes):
        attribute = result[index]
    
    device_info+=f"\nID устройства: {device_attributes[0]}"
    device_info+=f"\nАртикул: {device_attributes[1]}"
    device_info+=f"\nКатегория: {device_attributes[2]}"
    device_info+=f"\nПодкатегория: {device_attributes[3]}"
    device_info+=f"\nНазвание: {device_attributes[4]}"
    device_info+=f"\nКоличество (шт.): {device_attributes[5]}"
    device_info+=f"\nГод производства: {device_attributes[6]}"
    device_info+=f"\nГод постановки на учёт: {device_attributes[7]}"
    device_info+=f"\nМестонахождение: {device_attributes[8]}"
    #photoURL should be here but not yet
    if problematic_device_guard(articleNumber):
        device_info+=f'\n\n*Является "проблемным" устройством.*'

    return device_info

