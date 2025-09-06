import os
import asyncio
import logging

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from routes.auth_routes import router as AuthRouter


load_dotenv()
token = os.getenv('BOT_TOKEN', None)


async def main():
    bot = Bot(token=token)  # type: ignore
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(AuthRouter)
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
