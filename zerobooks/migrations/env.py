import asyncio
import sys
from logging.config import fileConfig
from os.path import abspath, dirname
from typing import cast

from alembic import context
from sqlalchemy import engine_from_config, pool

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)  # type: ignore

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata

# Add sys path
sys.path.append(abspath(dirname(dirname(dirname(__file__)))))

# Create tables
from atomdb.sql import SQLModelManager  # noqa: E402

from zerobooks.app import ZeroApplication  # noqa: E402

# First load all db models
from zerobooks.models import api  # noqa: F401, E402

manager = cast(SQLModelManager, SQLModelManager.instance())
manager.create_tables()

# Set metadata
target_metadata = manager.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def get_db_url():
    """Use MYSQL_URL env var instead of putting the DB credentials in a file
    also modifies it to use the pymysql backend.

    """
    from zerobooks.app import DB_FILE

    return f"sqlite:///{DB_FILE}"


def run_migrations_offline():
    """Run migrations in 'offline' mode.

        This configures the context with just a URL
        and not an Engine, though an Engine is acceptable
        here as well.  By skipping the Engine creation
        we don't even need a DBAPI to be available.
    k
        Calls to context.execute() here emit the given string to the
        script output.

    """
    url = get_db_url()
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    cfg = config.get_section(config.config_ini_section)
    # Use URL from env
    url = get_db_url()
    cfg["sqlalchemy.url"] = url
    connectable = engine_from_config(
        cfg,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    loop = asyncio.get_event_loop()
    db_file = url.split("://")[-1]
    loop.run_until_complete(ZeroApplication.open_database(db_file))
    assert manager.database is not None

    try:
        with connectable.connect() as connection:
            context.configure(connection=connection, target_metadata=target_metadata)

            with context.begin_transaction():
                context.run_migrations()
    finally:
        loop.run_until_complete(ZeroApplication.close_database())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
