from aioextensions import (
    in_thread,
)
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
from psycopg2 import (
    connect,
)
from psycopg2.extensions import (
    cursor as cursor_cls,
    ISOLATION_LEVEL_AUTOCOMMIT,
)
from typing import (
    Any,
    Iterator,
)

COMMIT_HASH_SENTINEL: str = "-" * 40
DATE_SENTINEL: datetime = datetime.utcfromtimestamp(0)
DATE_NOW: datetime = datetime.utcnow()
LOG = logging.getLogger(__name__)


def log_sync(level: str, msg: str, *args: Any) -> None:
    getattr(LOG, level)(msg, *args)


async def log(level: str, msg: str, *args: Any) -> None:
    await in_thread(log_sync, level, msg, *args)


@contextmanager
def db_cursor() -> Iterator[cursor_cls]:
    connection = connect(
        dbname=environ["REDSHIFT_DATABASE"],
        host=environ["REDSHIFT_HOST"],
        password=environ["REDSHIFT_PASSWORD"],
        port=environ["REDSHIFT_PORT"],
        user=environ["REDSHIFT_USER"],
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
