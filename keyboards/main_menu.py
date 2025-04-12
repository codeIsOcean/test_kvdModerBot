from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton


def get_main_menu():
    kb = InlineKeyboardBuilder()
    kb.row(
        InlineKeyboardButton(
            text="➕ Добавить меня в группу",
            url="https://t.me/test_KvdModerBot?startgroup=true"
        )
    )
    kb.row(
        InlineKeyboardButton(text="👥 Группа", url="https://t.me/your_group_link"),
        InlineKeyboardButton(text="📢 Канал", url="https://t.me/your_channel_linkkkk")
    )
    kb.row(
        InlineKeyboardButton(text="🔧 Поддержка", callback_data="support"),
        InlineKeyboardButton(text="📄 Информация", callback_data="info")
    )
    return kb.as_markup()