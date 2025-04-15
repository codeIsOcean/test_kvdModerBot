import asyncio
import logging
import os
import socket

from aiogram import Bot, Dispatcher
from aiogram import F
from aiogram.types import Message
from aiogram.types import Update
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
from dotenv import load_dotenv
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from handlers.newMemberMuteHandler import router as member_router
from handlers.start import start_router

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_HOST = "https://dishes-sections-cd-washer.trycloudflare.com"  # заменишь на свой cloudflared URL
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
dp.include_router(start_router)
dp.include_router(member_router)


@dp.message()
async def catch_all_messages(message: Message):
    print(f"[LOG] Получено сообщение: {message.text}")
    await message.answer("✅ Webhook работает, сообщение получено.")


@dp.message(F.text)
async def handle_message(message: Message):
    print(f"[👀] Получено сообщение от {message.from_user.full_name}: {message.text}")
    await message.answer("✅ Бот на связи! Webhook работает!")


async def on_startup(app: web.Application):
    try:
        await bot.set_webhook(WEBHOOK_URL)
        logging.info(f"✅ Webhook установлен: {WEBHOOK_URL}")
    except Exception as e:
        if "Too Many Requests" in str(e):
            logging.warning("⏱ Слишком частые установки Webhook. Ждём 2 секунды и пробуем ещё раз...")
            await asyncio.sleep(2)
            await bot.set_webhook(WEBHOOK_URL)
            logging.info(f"✅ Webhook повторно установлен: {WEBHOOK_URL}")
        else:
            raise


async def on_shutdown(app: web.Application):
    await bot.delete_webhook()
    logging.info("❌ Webhook удалён")


async def main(port: int = 8080):
    app = web.Application()
    SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=WEBHOOK_PATH)
    setup_application(app, dp, bot=bot)

    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)

    runner = web.AppRunner(app)
    await runner.setup()

    try:
        site = web.TCPSite(runner, "0.0.0.0", port)
        await site.start()
        print(f"🚀 Webhook сервер работает на http://localhost:{port}")

        # Ожидаем бесконечно — чтобы бот не завершался
        await asyncio.Event().wait()

    except OSError as e:
        if e.errno == 10048:
            logging.warning(f"❗ Порт {port} занят. Пробуем порт 8080...")
            return await main(port=8080)
        else:
            raise


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except Exception as e:
        logging.error(f"💥 Произошла ошибка: {e}")
