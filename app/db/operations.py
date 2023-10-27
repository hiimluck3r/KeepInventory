from app.db import database

async def delete_user(userid):
    sql = f"DELETE FROM users WHERE userid = {userid}"
    await database.execute(sql, execute=True)
        
async def add_user(userid, role):
    sql = f"INSERT INTO users (userid, role) VALUES({userid}, '{role}') ON CONFLICT (userid) DO UPDATE SET role = '{role}'"
    await database.execute(sql, execute=True)

async def custom_sql(sql, fetch: bool = False, fetchval: bool = False, fetchrow: bool = False, execute: bool = False):
    values = []
    result = None
    if fetch:
        result = await database.execute(sql, fetch=True)
        for row in result:
            a = []
            values.append(a)
            for field in row:
                a.append(field)
    elif fetchval:
        result = await database.execute(sql, fetchval=True)
        for row in result:
            a = []
            values.append(a)
            for field in row:
                a.append(field)
    elif fetchrow:
        result = await database.execute(sql, fetchrow=True)
        for row in result:
            a = []
            values.append(a)
            for field in row:
                a.append(field)
    elif execute:
        values = await database.execute(sql, execute=True)
    return values

async def get_users_by_role(role):
    sql = f"SELECT userid FROM users WHERE role = '{role}'"
    result = await database.execute(sql, fetch=True)
    values = []
    for row in result:
        for field in row:
            values.append(field)
    return values