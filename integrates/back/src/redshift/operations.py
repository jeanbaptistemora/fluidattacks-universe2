from aioextensions import (
    in_thread,
)
from context import (
    FI_AWS_REDSHIFT_DBNAME,
    FI_AWS_REDSHIFT_HOST,
    FI_AWS_REDSHIFT_PASSWORD,
    FI_AWS_REDSHIFT_PORT,
    FI_AWS_REDSHIFT_USER,
    FI_ENVIRONMENT,
)
from contextlib import (
    contextmanager,
)
import logging
import logging.config
import psycopg2
from psycopg2 import (
    extras,
)
from psycopg2.extensions import (
    cursor as cursor_cls,
    ISOLATION_LEVEL_AUTOCOMMIT,
)
from settings import (
    LOGGING,
    NOEXTRA,
)
from typing import (
    Any,
    Dict,
    Iterator,
    List,
    Optional,
)

logging.config.dictConfig(LOGGING)

LOGGER = logging.getLogger(__name__)
SCHEMA_NAME: str = "integrates"


@contextmanager
def db_cursor() -> Iterator[cursor_cls]:
    connection = psycopg2.connect(
        dbname=FI_AWS_REDSHIFT_DBNAME,
        host=FI_AWS_REDSHIFT_HOST,
        password=FI_AWS_REDSHIFT_PASSWORD,
        port=FI_AWS_REDSHIFT_PORT,
        user=FI_AWS_REDSHIFT_USER,
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


async def initialize_schema() -> None:
    with db_cursor() as cursor:
        LOGGER.info(f"Ensuring {SCHEMA_NAME} schema exists...", **NOEXTRA)
        await in_thread(
            cursor.execute,
            f"""
                CREATE SCHEMA IF NOT EXISTS {SCHEMA_NAME}
            """,
        )


async def execute(
    sql_query: str,
    sql_vars: Optional[Dict[str, Any]] = None,
) -> None:
    if FI_ENVIRONMENT == "production":
        with db_cursor() as cursor:
            await in_thread(cursor.execute, sql_query, sql_vars)


async def execute_many(
    sql_query: str,
    sql_vars: Optional[List[Dict[str, Any]]] = None,
) -> None:
    if FI_ENVIRONMENT == "production":
        with db_cursor() as cursor:
            await in_thread(cursor.executemany, sql_query, sql_vars)


async def execute_batch(
    sql_query: str,
    sql_vars: Optional[List[Dict[str, Any]]] = None,
) -> None:
    if FI_ENVIRONMENT == "production":
        with db_cursor() as cursor:
            extras.execute_batch(cursor, sql_query, sql_vars)
