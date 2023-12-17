import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import Config

bot = Bot(token=Config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)

loop = asyncio.get_event_loop()
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

