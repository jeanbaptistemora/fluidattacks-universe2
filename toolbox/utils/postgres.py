# Standard library
import contextlib
from operator import itemgetter
import os
from typing import (
    List,
    Tuple,
)

# Third party imports
with contextlib.suppress(ImportError):
    import psycopg2


def _get_connection_string_from_env():
    required_arguments: Tuple[str, ...] = (
        'dbname',
        'host',
        'password',
        'port',
        'user',
    )

    return {
        argument: os.environ[f'aws_redshift__{argument}']
        for argument in required_arguments
    }


def get_columns(cursor, table_schema: str, table_name: str) -> List[str]:
    query: str = """
        SELECT column_name
        FROM information_schema.COLUMNS
        WHERE (
            table_name = %(table_name)s
            and table_schema = %(table_schema)s
        )
        """
    variables: dict = {
        'table_name': table_name,
        'table_schema': table_schema,
    }
    cursor.execute(query, variables)

    return list(set(map(itemgetter(0), cursor)))


@contextlib.contextmanager
def database():
    connection = psycopg2.connect(**_get_connection_string_from_env())

    try:
        cursor = connection.cursor()
        try:
            yield connection, cursor
        finally:
            cursor.close()
    finally:
        connection.close()
