# Standard library
from contextlib import (
    contextmanager,
)
from datetime import (
    datetime,
)
import logging
from os import (
    environ,
)
import sys
from typing import (
    Any,
    Iterator,
)
# Third party libraries
from aioextensions import (
    in_thread,
)
from psycopg2 import (
    connect,
)
from psycopg2.extensions import (
    cursor as cursor_cls,
    ISOLATION_LEVEL_AUTOCOMMIT,
)


COMMIT_HASH_SENTINEL: str = '-' * 40
DATE_SENTINEL: datetime = datetime.utcfromtimestamp(0)
DATE_NOW: datetime = datetime.utcnow()

# Logging
LOG = logging.getLogger(__name__)
LOG.setLevel(logging.DEBUG)
LOG.addHandler(logging.StreamHandler())
LOG.handlers[0].setFormatter(logging.Formatter('[%(levelname)s] %(message)s'))


def get_log(name: str, min_lvl: int = logging.INFO) -> logging.Logger:
    logger_format: str = '[%(levelname)s] %(message)s'
    logger_formatter: logging.Formatter = logging.Formatter(logger_format)

    logger_handler: logging.Handler = logging.StreamHandler(sys.stderr)
    logger_handler.setFormatter(logger_formatter)

    logger: logging.Logger = logging.getLogger(name)
    logger.setLevel(min_lvl)
    logger.addHandler(logger_handler)
    return logger


def log_sync(level: str, msg: str, *args: Any) -> None:
    getattr(LOG, level)(msg, *args)


async def log(level: str, msg: str, *args: Any) -> None:
    await in_thread(log_sync, level, msg, *args)


@contextmanager
def db_cursor() -> Iterator[cursor_cls]:
    connection = connect(
        dbname=environ['REDSHIFT_DATABASE'],
        host=environ['REDSHIFT_HOST'],
        password=environ['REDSHIFT_PASSWORD'],
        port=environ['REDSHIFT_PORT'],
        user=environ['REDSHIFT_USER'],
    )
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    try:
        cursor: cursor_cls = connection.cursor()
        try:
            yield cursor
        finally:
            cursor.close()
    finally:
        connection.close()
