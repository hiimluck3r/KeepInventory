from app.db import database
from app import ROOT

async def delete_user(userid):
    sql = f"DELETE FROM users WHERE userid = {userid}"
    await database.execute(sql, execute=True)
        
async def add_user(userid, role):
    if role == "admin":
        role = 2
    elif role == "worker":
        role = 1
    else:
        role = 0 #spectator is basically the base role
        
    sql = f"INSERT INTO users (userid, role) VALUES({userid}, {role}) ON CONFLICT (userid) DO UPDATE SET role = {role}"
    await database.execute(sql, execute=True)

async def custom_sql(sql, fetch: bool = False, fetchval: bool = False, fetchrow: bool = False, execute: bool = False):
    values = []
    result = None
    if fetch:
        result = await database.execute(sql, fetch=True)
        values = [dict(row) for row in result]
    elif fetchval:
        values = await database.execute(sql, fetchval=True)
    elif fetchrow:
        result = await database.execute(sql, fetchrow=True)
        values = dict(result)
    elif execute:
        values = await database.execute(sql, execute=True)
    
    if values:
        return values
    else:
        return None

async def get_users_by_role(role):
    
    if role == "admin":
        role = 2
    elif role == "worker":
        role = 1
    else:
        role = 0 #spectator is basically the base role
    
    sql = f"SELECT userid FROM users WHERE role >= {role}"
    result = await database.execute(sql, fetch=True)
    values = [ROOT]
    for row in result:
        for field in row:
            values.append(field)
    return values