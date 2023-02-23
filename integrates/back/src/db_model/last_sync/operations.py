from collections.abc import (
    Iterator,
)
from context import (
    FI_AWS_REDSHIFT_DBNAME,
    FI_AWS_REDSHIFT_HOST,
    FI_AWS_REDSHIFT_PASSWORD,
    FI_AWS_REDSHIFT_PORT,
    FI_AWS_REDSHIFT_USER,
)
from contextlib import (
    contextmanager,
)
import psycopg2
from psycopg2.extensions import (
    cursor as cursor_cls,
    ISOLATION_LEVEL_AUTOCOMMIT,
)


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
