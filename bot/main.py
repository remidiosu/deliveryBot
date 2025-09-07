import os
import asyncio
import logging

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from middlewares.auth import AuthMiddleware
from routes.auth_routes import router as AuthRouter
from routes.controller_routes import router as ControllerRouter


load_dotenv()
token = os.getenv('BOT_TOKEN', None)


async def main():
    bot = Bot(token=token)  # type: ignore
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(AuthRouter)
    dp.include_router(ControllerRouter)
    dp.update.middleware(AuthMiddleware())
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
