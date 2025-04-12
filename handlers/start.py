from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, ChatMemberUpdated
from aiogram.filters import CommandStart
from aiogram.enums import ParseMode

from configs import ADMIN_IDS
from keyboards.main_menu import get_main_menu
from texts.messages import WELCOME_TEXT, SUPPORT_TEXT, INFO_TEXT

start_router = Router()

ALOOWED_USERS = ADMIN_IDS


@start_router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        WELCOME_TEXT.format(name=message.from_user.first_name),
        reply_markup=get_main_menu(),
        parse_mode=ParseMode.MARKDOWN
    )


@start_router.callback_query(F.data == "add_group")
async def add_group_callback(call: CallbackQuery):
    if call.from_user.id in ALOOWED_USERS:
        text = "\ud83d\udd17 Вот список групп, где вы админ или участник (эмуляция)."
    else:
        "\u274c Извините, на данный момент я работаю только с определёнными пользователями."
    await call.message.edit_text(text)


@start_router.callback_query(F.data == "support")
async def support_callback(call: CallbackQuery):
    await call.message.edit_text(SUPPORT_TEXT)


@start_router.callback_query(F.data == "info")
async def info_callback(call: CallbackQuery):
    await call.message.edit_text(INFO_TEXT)


@start_router.my_chat_member()
async def handl_added_to_group(event: ChatMemberUpdated):
    #Проверка что бот стал админом
    if event.new_chat_member.status in("administrator", "member"):
        user = event.from_user
        chat = event.chat
        print(f"✅Бот добавлен в группу {chat.title} ({chat.id} от {user.full_name} ({user.id})")




