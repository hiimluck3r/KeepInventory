import asyncpg

from app import USER, PASSWORD, DB, HOST, PORT

async def connector():
    pool = await asyncpg.create_pool(
            user=USER,
            password=PASSWORD,
            database=DB,
            host=HOST,
            port=PORT,
        )
    return pool