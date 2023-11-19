from aiogram.filters import Filter
from aiogram import types
from typing import Union
from app.db.operations import get_users_by_role
import sys
from app import ROOT

class RoleCheck(Filter):
    def __init__(self, role: str) -> None:
        self.role = role
        pass

    async def __call__(self, query_or_message: Union[types.Message, types.CallbackQuery]) -> bool:  
        if self.role == "admin": #role = 2 - admin
            return query_or_message.from_user.id in (await get_users_by_role("admin"))
            
        elif self.role == "worker": #role = 1 - worker
            return query_or_message.from_user.id in (await get_users_by_role("worker"))

        elif  self.role == "spectator": #role = 0 - spectator
            return query_or_message.from_user.id in (await get_users_by_role("spectator"))
        
        else:
            return False

async def role_check_function(query_or_message_id, role) -> bool:  
        if role == "admin": #role = 2 - admin
            return query_or_message_id in (await get_users_by_role("admin"))
            
        elif role == "worker": #role = 1 - worker
            return query_or_message_id in (await get_users_by_role("worker"))

        elif  role == "spectator": #role = 0 - spectator
            return query_or_message_id in (await get_users_by_role("spectator"))
        
        else:
            return False