from collections.abc import (
    Iterator,
)
from contextlib import (
    contextmanager,
)
from dynamodb.context import (
    FI_AWS_REDSHIFT_DBNAME,
    FI_AWS_REDSHIFT_HOST,
    FI_AWS_REDSHIFT_PASSWORD,
    FI_AWS_REDSHIFT_USER,
    FI_ENVIRONMENT,
)
import logging
import psycopg2
from psycopg2 import (
    extras,
    sql,
)
from psycopg2.extensions import (
    cursor as cursor_cls,
    ISOLATION_LEVEL_AUTOCOMMIT,
)
from typing import (
    Any,
)

LOGGER = logging.getLogger(__name__)
SCHEMA_NAME: str = "integrates"
AWS_REDSHIFT_PORT = 5439


@contextmanager
def db_cursor() -> Iterator[cursor_cls]:
    connection = psycopg2.connect(
        dbname=FI_AWS_REDSHIFT_DBNAME,
        host=FI_AWS_REDSHIFT_HOST,
        password=FI_AWS_REDSHIFT_PASSWORD,
        port=AWS_REDSHIFT_PORT,
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


def initialize_schema() -> None:
    with db_cursor() as cursor:
        LOGGER.info("Ensuring %s schema exists...", SCHEMA_NAME)
        cursor.execute(
            sql.SQL(
                """
                CREATE SCHEMA IF NOT EXISTS {schema_name}
            """
            ).format(
                schema_name=sql.Identifier(SCHEMA_NAME),
            ),
        )


def execute(
    sql_query: sql.Composed,
    sql_vars: dict[str, Any] | None = None,
) -> None:
    if FI_ENVIRONMENT == "prod":
        with db_cursor() as cursor:
            cursor.execute(sql_query, sql_vars)


def execute_many(
    sql_query: sql.Composed,
    sql_vars: list[dict[str, Any]] | None = None,
) -> None:
    if FI_ENVIRONMENT == "prod":
        with db_cursor() as cursor:
            cursor.executemany(sql_query, sql_vars)


def execute_batch(
    sql_query: sql.Composed,
    sql_vars: list[dict[str, Any]] | None = None,
) -> None:
    if FI_ENVIRONMENT == "prod":
        with db_cursor() as cursor:
            extras.execute_batch(cursor, sql_query, sql_vars, page_size=1000)
