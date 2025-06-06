import asyncio
from aiogram import Router, Bot, Dispatcher, F
from aiogram.filters import Command, CommandObject
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
import logging

from configs import TOKEN
from handlers.newMemberMuteHandler import router as member_router
from handlers.start import start_router
from handlers.callbacks import callback_router
from handlers.group_events import group_router
from handlers.settings import settings_router

# Измененный импорт

bot = Bot(TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
dp.include_router(start_router)
dp.include_router(member_router)
dp.include_router(group_router)
dp.include_router(callback_router)
dp.include_router(settings_router)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
