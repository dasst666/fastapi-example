import os
from logging.config import fileConfig

from dotenv import load_dotenv
from sqlmodel import SQLModel

from alembic import context

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

# Импорт моделей
from src.schemas import *

# Alembic config
config = context.config
fileConfig(config.config_file_name)
target_metadata = SQLModel.metadata


def run_migrations_offline():
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    from sqlalchemy import create_engine

    engine = create_engine(DATABASE_URL)
    with engine.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata, compare_type=True
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
