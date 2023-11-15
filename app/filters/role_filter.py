from aiogram.filters import Filter
from aiogram import types
from typing import Union
from app.db.operations import get_users_by_role
import sys
from app import ROOT

class RoleCheck(Filter):
    def __init__(self, my_text: str) -> None:
        self.my_text = my_text
        pass

    async def __call__(self, query_or_message: Union[types.Message, types.CallbackQuery]) -> bool:  
        if self.my_text == "admin": #role = 2 - admin
            return query_or_message.from_user.id in (await get_users_by_role("admin"))
            
        elif self.my_text == "worker": #role = 1 - worker
            return query_or_message.from_user.id in (await get_users_by_role("worker"))

        elif  self.my_text == "spectator": #role = 0 - spectator
            return query_or_message.from_user.id in (await get_users_by_role("spectator"))
        
        else:
            return False