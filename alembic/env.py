from db.session import Base
from db.models import User, Group
import asyncio
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from sqlalchemy.ext.asyncio import AsyncEngine
from alembic import context
from sqlalchemy.ext.asyncio import create_async_engine


target_metadata = Base.metadata  # Должно быть ПОСЛЕ импорта моделей!
config = context.config
fileConfig(config.config_file_name) if config.config_file_name else None


async def get_async_engine():
    return create_async_engine(context.config.get_main_option("sqlalchemy.url"), echo=True)


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    context.configure(connection=connection,
                      target_metadata=Base.metadata,
                      compare_type=True,
                      compare_server_default=True
                      )
    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    engine = get_async_engine()
    async with engine.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await engine.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    import asyncio

    asyncio.run(run_migrations_online())
