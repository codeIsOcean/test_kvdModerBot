# приветствие при добавлениях в группу
from aiogram import Router, Bot, F
from aiogram.types import Message, ChatMemberUpdated, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.enums import ChatMemberStatus
from aiogram.filters import ChatMemberUpdatedFilter
from sqlalchemy.ext.asyncio import AsyncSession

from db.queries import add_group_admin

group_router = Router()
group_router.chat_member(
    ChatMemberUpdatedFilter(member_status_changed=(None, ChatMemberStatus.MEMBER))
)


async def bot_added(event: ChatMemberUpdated, bot: Bot, session: AsyncSession):
    group_id = event.chat.id
    admin_id = event.from_user.id

    await add_group_admin(group_id, admin_id, session)

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⚙️ Настроить", callback_data=f"settings_{group_id}")]
    ])

    await bot.send_message(
        chat_id=group_id,
        text="👋 Бот добавлен!\n\nЧтобы использовать мои функции — нажмите кнопку ниже:",
        reply_markup=kb
    )