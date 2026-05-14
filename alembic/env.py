from logging.config import fileConfig
import os
import sys

from dotenv import load_dotenv
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

# ── Load .env from backend/.env (single source of truth for credentials) ──
# This uses an absolute path relative to THIS file so it works regardless
# of the working directory you run `alembic` from.
_project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_backend_env = os.path.join(_project_root, "backend", ".env")
load_dotenv(_backend_env)

# ── Add backend/ to sys.path so "from src.*" imports resolve ──
_backend_path = os.path.join(_project_root, "backend")
sys.path.insert(0, _backend_path)

# ── Alembic Config object ──
config = context.config

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ── Import ALL models so Base.metadata sees every table ──
from src.database.core import Base          # noqa: E402
from src.entities.user import User          # noqa: E402,F401
from src.entities.incident import Incident  # noqa: E402,F401

target_metadata = Base.metadata

# ── Inject DATABASE_URL from .env into Alembic config at runtime ──
_db_url = os.getenv("DATABASE_URL", "")
if not _db_url:
    raise RuntimeError(
        "DATABASE_URL is not set. "
        f"Looked in: {_backend_env}"
    )
config.set_main_option("sqlalchemy.url", _db_url)


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


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
