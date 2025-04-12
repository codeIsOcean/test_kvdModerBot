from aiogram import Router, F, Bot
from aiogram.types import ChatMemberUpdated, Message, ChatPermissions
from aiogram.filters import ChatMemberUpdatedFilter, Command
from aiogram.enums import ChatMemberStatus, ChatType
from datetime import datetime, timedelta
import asyncio
import logging

router = Router()


# ✅ Вариант 1: Мут через RESTRICTED статус (когда одобрение идёт через join_request)
@router.chat_member(
    F.chat.type.in_({"group", "supergroup"}),
    ChatMemberUpdatedFilter(
        member_status_changed=(None, ChatMemberStatus.RESTRICTED)
    )
)
async def mute_unapproved_member(event: ChatMemberUpdated):
    """Мут участников, не прошедших одобрение"""
    try:
        if getattr(event.new_chat_member, 'is_approved', True):
            return

        user = event.new_chat_member.user
        chat = event.chat

        await event.bot.restrict_chat_member(
            chat_id=chat.id,
            user_id=user.id,
            permissions=ChatPermissions(
                can_send_messages=False,
                can_send_media_messages=False,
                can_send_polls=False,
                can_send_other_messages=False,
                can_add_web_page_previews=False,
                can_change_info=False,
                can_invite_users=False,
                can_pin_messages=False
            ),
            until_date=datetime.now() + timedelta(days=366)
        )

        await asyncio.sleep(1)
        await event.bot.send_message(
            chat_id=chat.id,
            text=f"🚫 Спамер @{user.username} был автоматически замьючен."
        )

    except Exception as e:
        logging.error(f"MUTE ERROR (variant 1): {str(e)}")


# ✅ Вариант 2: Отслеживаем вручную обновление chat_member после одобрения
@router.chat_member(
    F.chat.type.in_({"group", "supergroup"})
)
async def manually_mute_on_approval(event: ChatMemberUpdated):
    """Мут вручную одобренных участников, если Telegram прислал событие"""
    try:
        old_status = event.old_chat_member.status
        new_status = event.new_chat_member.status

        logging.info(f"[V2] Обработка chat_member: {event.from_user.id} | old={old_status} -> new={new_status}")

        if old_status in ("left", "kicked") and new_status == "member":
            user = event.new_chat_member.user
            chat = event.chat

            await event.bot.restrict_chat_member(
                chat_id=chat.id,
                user_id=user.id,
                permissions=ChatPermissions(
                    can_send_messages=False,
                    can_send_media_messages=False,
                    can_send_polls=False,
                    can_send_other_messages=False,
                    can_add_web_page_previews=False,
                    can_change_info=False,
                    can_invite_users=False,
                    can_pin_messages=False
                ),
                until_date=datetime.now() + timedelta(days=366)
            )

            await asyncio.sleep(1)
            logging.info(f"🔇 Пользователь @{user.username} был замьючен после ручного одобрения (chat_member).")
        else:
            logging.info(f"[V2] Не обработан: статус не соответствует. old={old_status}, new={new_status}")

    except Exception as e:
        logging.error(f"MUTE ERROR (variant 2 - manual chat_member): {str(e)}")


# ✅ Повторная проверка при изменении прав
@router.chat_member(
    F.chat.type.in_({"group", "supergroup"}),
    ChatMemberUpdatedFilter(
        member_status_changed=(ChatMemberStatus.RESTRICTED, ChatMemberStatus.MEMBER)
    )
)
async def recheck_approved_member(event: ChatMemberUpdated):
    """Повторно мутим, если одобренный пользователь всё ещё не подтверждён"""
    await mute_unapproved_member(event)

# тут были изменения сделаны.
# from aiogram import Router, F, Bot
# from aiogram.types import ChatMemberUpdated, Message, ChatPermissions
# from aiogram.filters import ChatMemberUpdatedFilter, Command
# from aiogram.enums import ChatMemberStatus, ChatType
# from datetime import datetime, timedelta
# import asyncio
# import logging
#
# router = Router()
# тут я прописал изменения чтобы закоммитить на удаленку
#
# @router.chat_member(
#     F.chat.type.in_({"group", "supergroup"}),
#     ChatMemberUpdatedFilter(
#         member_status_changed=(None, ChatMemberStatus.RESTRICTED)
#     )
# )
# async def mute_unapproved_member(event: ChatMemberUpdated):
#     """Мут участников, не прошедших одобрение"""
#     try:
#         if getattr(event.new_chat_member, 'is_approved', True):
#             return
#
#         user = event.new_chat_member.user
#         chat = event.chat
#
#         await event.bot.restrict_chat_member(
#             chat_id=chat.id,
#             user_id=user.id,
#             permissions=ChatPermissions(
#                 can_send_messages=False,
#                 can_send_media_messages=False,
#                 can_send_polls=False,
#                 can_send_other_messages=False,
#                 can_add_web_page_previews=False,
#                 can_change_info=False,
#                 can_invite_users=False,
#                 can_pin_messages=False
#             ),
#             until_date=datetime.now() + timedelta(days=366)
#         )
#
#         await asyncio.sleep(1)
#         await event.bot.delete_message(chat.id, event.message_id)
#
#         await event.bot.send_message(
#             chat_id=chat.id,
#             text=f"🚫 Спамер @{user.username} был автоматически замьючен."
#         )
#
#     except Exception as e:
#         logging.error(f"MUTE ERROR: {str(e)}")
#
#
# @router.chat_member(
#     F.chat.type.in_({"group", "supergroup"}),
#     ChatMemberUpdatedFilter(
#         member_status_changed=(ChatMemberStatus.RESTRICTED, ChatMemberStatus.MEMBER)
#     )
# )
# async def recheck_approved_member(event: ChatMemberUpdated):
#     """Повторно мутим, если одобренный пользователь всё ещё не подтверждён"""
#     await mute_unapproved_member(event)
#
#
# @router.message(Command("fix_rights"))
# async def fix_rights(message: Message):
#     """Проверка настроек группы"""
#     chat = message.chat
#     try:
#         bot_member = await message.bot.get_chat_member(chat.id, (await message.bot.me()).id)
#
#         if not bot_member.can_restrict_members:
#             await message.answer("⚠ Боту не хватает прав 'Блокировать участников'!")
#             return
#
#         chat_info = await message.bot.get_chat(chat.id)
#         if not getattr(chat_info, 'join_by_request', False):
#             await message.answer("⚠ В группе не включено 'Одобрение участников'!")
#
#         await message.answer("✅ Все настройки корректны для работы антиспама!")
#
#     except Exception as e:
#         logging.error(f"Rights check failed: {e}")
#         await message.answer("🔴 Ошибка проверки прав!")
#
#
# @router.message(Command("my_rights"))
# async def check_rights(message: Message, bot: Bot):
#     """Показ прав бота в чате"""
#     try:
#         chat = message.chat
#         bot_member = await bot.get_chat_member(chat.id, (await bot.get_me()).id)
#
#         response = (
#             f"ℹ️ <b>Информация о правах бота</b>\n"
#             f"Чат: {chat.title}\n"
#             f"Тип: {chat.type}\n"
#             f"Статус бота: {bot_member.status}\n"
#             f"Может ограничивать: {getattr(bot_member, 'can_restrict_members', False)}\n"
#             f"Одобрение участников: {getattr(chat, 'join_by_request', False)}"
#         )
#         await message.answer(response)
#     except Exception as e:
#         logging.error(f"Rights check error: {e}")
#         await message.answer("⚠ Ошибка проверки прав. Подробности в логах.")
#
#
# @router.message(Command("check"))
# async def check_bot(message: Message):
#     """Проверка активности бота"""
#     await message.answer("Бот активен и работает!")
#
#
# @router.message(Command("check_mute"))
# async def check_mute(message: Message):
#     """Тест мута на самом себе"""
#     test_user_id = message.from_user.id
#     chat_id = message.chat.id
#
#     success = await apply_mute(chat_id, test_user_id, message.bot)
#     if success:
#         await message.answer("✅ Тестовый мут применён успешно!")
#         await asyncio.sleep(10)
#         await message.bot.restrict_chat_member(
#             chat_id=chat_id,
#             user_id=test_user_id,
#             permissions=ChatPermissions(can_send_messages=True)
#         )
#     else:
#         await message.answer("❌ Не удалось применить мут!")
#
#
# async def apply_mute(chat_id: int, user_id: int, bot: Bot):
#     """Универсальный мут пользователя"""
#     try:
#         bot_member = await bot.get_chat_member(chat_id, (await bot.me()).id)
#         if not (bot_member.is_chat_admin() and bot_member.can_restrict_members):
#             logging.error("Бот не имеет прав для мута!")
#             return False
#
#         await bot.restrict_chat_member(
#             chat_id=chat_id,
#             user_id=user_id,
#             permissions=ChatPermissions(can_send_messages=False),
#             until_date=datetime.now() + timedelta(days=366)
#         )
#         return True
#     except Exception as e:
#         logging.error(f"Mute failed: {str(e)}")
#         return False
