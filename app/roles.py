import asyncio
from app.db.operations import get_users_by_role
from app import ROOT, loop
import sys

async def update_users():
    tasks = []
    roles = ["admin", "worker", "spectator"]
    users = {}

    for role in roles:
        task = asyncio.create_task(get_users_by_role(role))
        tasks.append(task)

    users['admin'], users['worker'], users['spectator'] = await asyncio.gather(*tasks)    
    users['admin'].append(ROOT)
    users['worker'] += users['admin']
    users['spectator'] += users['worker']

    print(f"Admins: {users['admin']}", file=sys.stderr)
    print(f"Workers: {users['worker']}", file=sys.stderr)
    print(f"Spectators: {users['spectator']}", file=sys.stderr)

    return users

users = loop.run_until_complete(update_users())
admin = users["admin"]
worker = users["worker"]
spectator = users["spectator"]
