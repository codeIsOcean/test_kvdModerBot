# подключение к БД
from sqlalchemy.ext.asyncio import create_async_engine, async_session
from sqlalchemy.orm import DeclarativeBase
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = (
    f"postgresql+asyncpg://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = async_session(engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass