# pylint: skip-file

from postgres_client.query import (
    Query,
    SqlArgs,
)


def get_tables(schema: str) -> Query:
    query: str = (
        "SELECT tables.table_name FROM information_schema.tables "
        "WHERE table_schema = %(schema_name)s"
    )
    args = SqlArgs(values={"schema_name": schema})
    return Query(query, args)


def exist(schema: str) -> Query:
    query: str = (
        "SELECT EXISTS("
        "SELECT 1 FROM pg_namespace "
        "WHERE nspname = %(schema_name)s);"
    )
    args = SqlArgs(values={"schema_name": schema})
    return Query(query, args)


def delete(schema: str, cascade: bool) -> Query:
    opt = "CASCADE" if cascade else ""
    query: str = "DROP SCHEMA {schema_name} " + opt
    args = SqlArgs(identifiers={"schema_name": schema})
    return Query(query, args)


def create(schema: str) -> Query:
    query: str = "CREATE SCHEMA {schema_name}"
    args = SqlArgs(identifiers={"schema_name": schema})
    return Query(query, args)
