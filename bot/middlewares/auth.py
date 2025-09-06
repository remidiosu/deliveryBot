from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.filters import BaseFilter
from aiogram.types import TelegramObject, Message, CallbackQuery
import json

from services.user_api_service import verify_user
from config.redis import r, CACHE_TTL, NEG_TTL


async def get_role_cached(tg_id: int) -> dict | None:
    key = f"user:role:{tg_id}"
    cached = await r.get(key)
    if cached:
        try:
            return json.loads(cached)
        except json.JSONDecodeError:
            await r.delete(key)

    resp = await verify_user(tg_id)
    data = resp.get("data")

    if data.get('role'):
        await r.set(key, json.dumps(data), ex=CACHE_TTL)

    return data


class AuthMiddleware(BaseMiddleware):
    async def __call__(self, handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       event: TelegramObject, data: Dict[str, Any]) -> Any:
        if isinstance(event, (Message, CallbackQuery)):
            from_user = event.from_user
        else:
            from_user = getattr(event, "from_user", None)

        info = await get_role_cached(from_user.id)
        data["role"] = info.get("role")
        data["is_registered"] = info.get("registered")

        return await handler(event, data)
