from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery
import json


class RequireRoles(BaseFilter):
    def __init__(self, *roles: str):
        self.roles = set(roles)

    async def __call__(self, event: Message | CallbackQuery, **data):
        role = data.get("role")
        is_registered = data.get("is_registered")
        # print(f"DBG role={role}, reg={is_registered}")  # temporary
        return bool(is_registered) and role in self.roles
