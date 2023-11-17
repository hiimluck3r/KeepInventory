import sys
import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool
from app import DBUSER, DB, HOST, PORT, PASSWORD

class DatabaseClass:
    def __init__(self):
        self.pool = None

    async def create_pool(self):
        self.pool = await asyncpg.create_pool(database=DB, user=DBUSER, password=PASSWORD, host=HOST, port=PORT)

    async def execute(self, command: str, *args, fetch: bool = False, fetchval: bool = False, fetchrow: bool = False, execute: bool = False, download: bool = False):
        if self.pool is None:
            await self.create_pool()
        result = None
        async with self.pool.acquire() as connection:
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
                elif download:
                    print(command, file = sys.stderr)
                    result = await connection.copy_from_table(
                        command, output = f'app/backups/{command}.csv' #command = name of the table
                    )
                    print(f"Made a backup of {command}: {result}", file = sys.stderr)
        return result

database = DatabaseClass()

