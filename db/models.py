from sqlalchemy import Integer, String, BigInteger  # таблицы
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Column, BigInteger
from db.session import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)
    full_name: Mapped[str] = mapped_column(String(255))


# таблица для хранения информаций группы и админы который добавляет бота в группу
class Group(Base):
    __tablename__ = "groups"

    group_id = Column(BigInteger, primary_key=True, index=True)
    admin_id = Column(BigInteger, nullable=False)
