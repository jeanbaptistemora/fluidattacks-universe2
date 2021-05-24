# pylint: skip-file
# Standard libraries
from typing import (
    List,
)

# Third party libraries
from returns.maybe import Maybe

# Local libraries
from postgres_client.cursor import (
    DynamicSQLargs,
    Query,
)


def get_tables(schema: str) -> Query:
    query: str = (
        "SELECT tables.table_name FROM information_schema.tables "
        "WHERE table_schema = %(schema_name)s"
    )
    args = DynamicSQLargs(values={"schema_name": schema})
    return Query.new(query, Maybe.from_value(args))


def exist(schema: str) -> Query:
    query: str = (
        "SELECT EXISTS("
        "SELECT 1 FROM pg_namespace "
        "WHERE nspname = %(schema_name)s);"
    )
    args = DynamicSQLargs(values={"schema_name": schema})
    return Query.new(query, Maybe.from_value(args))


def delete(schema: str) -> Query:
    query: str = "DROP SCHEMA {schema_name}"
    args = DynamicSQLargs(identifiers={"schema_name": schema})
    return Query.new(query, Maybe.from_value(args))
