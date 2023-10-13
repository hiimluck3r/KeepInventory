import asyncio
from app.db.connection import *
from app import ROOT
import sys

pool = ''
worker = ''
spectator = ''
admin = ''

async def get_users():
    global pool, admin, worker, spectator
    pool = await connector()
    async with pool.acquire() as connection:
        async with connection.transaction():
            admin = await connection.fetch(f"SELECT userid FROM users WHERE role = 'root'")
            worker = await connection.fetch(f"SELECT userid FROM users WHERE role = 'worker'")
            spectator = await connection.fetch(f"SELECT userid FROM users WHERE role = 'spectator'")
            admin.append(ROOT) #basically any admin == root, but only root can manage admins
            worker += admin #admins == workers but not vice verse
            spectator += (worker) #same goes to spectators, since we've got admins in workers, it works just as fine as we want

            return pool, admin, worker, spectator

asyncio.run(get_users())
print(f"Admins: {admin}", file=sys.stderr)
print(f"Workers: {worker}", file=sys.stderr)
print(f"Spectators: {spectator}", file=sys.stderr)