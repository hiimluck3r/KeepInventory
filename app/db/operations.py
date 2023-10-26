from app.db import database

async def delete_user(userid):
    sql = f"DELETE FROM users WHERE userid = {userid}"
    await database.execute(sql, execute=True)
        
async def add_user(userid, role):
    sql = f"INSERT INTO users (userid, role) VALUES({userid}, '{role}') ON CONFLICT (userid) DO UPDATE SET role = '{role}'"
    await database.execute(sql, execute=True)

async def custom_sql(sql):
    result = await database.execute(sql, execute=True)
    return result

async def get_users_by_role(role):
    sql = f"SELECT userid FROM users WHERE role = '{role}'"
    result = await database.execute(sql, fetch=True)
    return result