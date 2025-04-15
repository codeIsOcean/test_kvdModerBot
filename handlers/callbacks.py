# обработка inline кнопок, кнопки которые появятся в чате
from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from db.queries import get_group_admin
from sqlalchemy.ext.asyncio import AsyncSession

callback_router = Router()


@callback_router.callback_query(F.data.startswith("settings_"))
async def group_settings_callback(call: CallbackQuery, session: AsyncSession):
    group_id = int(call.data.split("_")[1])
    user_id = call.from_user.id

    admin_id = await get_group_admin(group_id, session)

    if user_id != admin_id:
        await call.answer("⛔ Только админ, добавивший бота, может настраивать его.", show_alert=True)
        return

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔐 Открыть в приватном чате",
                              url=f"https://t.me/{call.bot.username}?start=settings")]
    ])

    await call.message.edit_text(
        text="⚙️ Настройки были отправлены в приватный чат.",
        reply_markup=kb
    )
