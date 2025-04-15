# sql-функции (опционально)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from db.models import Group


# функция запросов добавления деталей админа(который добавляет бота в группу) в бд
async def add_group_admin(group_id: int, admin_id: int, session: AsyncSession):
    existing = await session.get(Group, group_id)
    if not existing:
        session.add(Group(group_id=group_id, admin_id=admin_id))
        await sesssion.commit()


async def get_group_admin(group_id: int, session: AsyncSession):
    result = await session.get(Group, group_id)
    return result.admin_id if result else None
