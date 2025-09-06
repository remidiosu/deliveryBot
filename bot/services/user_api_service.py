import aiohttp
from .settings import BASE_URL, _headers


async def verify_user(telegram_id: int) -> dict:
    url = f"{BASE_URL}/verify/?telegram_id={telegram_id}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=_headers()) as resp:
            return {"status": resp.status, "data": await resp.json()}


async def create_user(telegram_id: int, role: str, full_name: str, phone_number: str | None = None) -> dict:
    assert role in {"courier", "controller"}
    url = f"{BASE_URL}/register/{role}/"
    payload = {
        "full_name": full_name,
        "telegram_id": telegram_id,
        "phone_number": phone_number,
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload, headers=_headers()) as resp:
            return {"status": resp.status, "data": await resp.json()}


async def fetch_user(telegram_id: int): 
    url = f"{BASE_URL}/fetch/user/"
    payload = {
        "telegram_id": telegram_id
    }

    async with aiohttp.ClientSession() as session: 
        async with session.get(url, json=payload, headers=_headers()) as resp: 
            return {"status": resp.status, "data": await resp.json()}


async def update_user(telegram_id: int, role: str, full_name: str, phone_number: str | None = None) -> dict:
    url = f"{BASE_URL}/update/{role}"
    payload = {
        "full_name": full_name,
        "telegram_id": telegram_id,
        "phone_number": phone_number,
    }

    async with aiohttp.ClientSession() as session:
        async with session.patch(url, json=payload, headers=_headers()) as resp:
            return {"status": resp.status, "data": await resp.json()}


async def fetch_couriers(telegram_id: int) -> dict:
    url = f"{BASE_URL}/couriers/"
    payload = {
        "telegram_id": telegram_id
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, json=payload, headers=_headers()) as resp:
            return {"status": resp.status, "data": await resp.json()}


async def add_courier_to_controller(telegram_id, phone_number: str | None = None) -> dict:
    url = f"{BASE_URL}/couriers/add/"
    payload = {
        "telegram_id": telegram_id,
        "phone_number": phone_number,
    }

    async with aiohttp.ClientSession() as session:
        async with session.patch(url, json=payload, headers=_headers()) as resp:
            return {"status": resp.status, "data": await resp.json()}
