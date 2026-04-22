from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import os
from dotenv import load_dotenv

load_dotenv()

# Import models so they register with Base.metadata before autogenerate
from app.models.user import User  # noqa: F401
from app.models.task import Task  # noqa: F401
from app.db.database import Base

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Point Alembic at your models' metadata for autogenerate
target_metadata = Base.metadata

# Read DATABASE_URL from environment (falls back to SQLite)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./tasks.db")
config.set_main_option("sqlalchemy.url", DATABASE_URL)


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
