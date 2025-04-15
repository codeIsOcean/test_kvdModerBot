# логика обработки в личке
from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

settings_router = Router()


@settings_router.message(CommandStart(deep_link="settings"))
async def start_settings(message: Message):
    await message.answer(f"🛠 Здесь будут настройки бота для вашей группы: [{message.chat.title}]"
                         f"(https://t.me/{message.chat.username}).", parse_mode="Markdown")
