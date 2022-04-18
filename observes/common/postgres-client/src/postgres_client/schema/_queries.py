# pylint: skip-file

from postgres_client.ids import (
    SchemaID,
)
from postgres_client.query import (
    Query,
    SqlArgs,
)


def get_tables(schema: SchemaID) -> Query:
    query: str = (
        "SELECT tables.table_name FROM information_schema.tables "
        "WHERE table_schema = %(schema_name)s"
    )
    args = SqlArgs(values={"schema_name": str(schema)})
    return Query(query, args)


def exist(schema: SchemaID) -> Query:
    query: str = (
        "SELECT EXISTS("
        "SELECT 1 FROM pg_namespace "
        "WHERE nspname = %(schema_name)s);"
    )
    args = SqlArgs(values={"schema_name": str(schema)})
    return Query(query, args)


def delete(schema: SchemaID, cascade: bool) -> Query:
    opt = "CASCADE" if cascade else ""
    query: str = "DROP SCHEMA {schema_name} " + opt
    args = SqlArgs(identifiers={"schema_name": str(schema)})
    return Query(query, args)


def create(schema: SchemaID) -> Query:
    query: str = "CREATE SCHEMA {schema_name}"
    args = SqlArgs(identifiers={"schema_name": str(schema)})
    return Query(query, args)


def rename(from_schema: SchemaID, to_schema: SchemaID) -> Query:
    query = "ALTER SCHEMA {from_schema} RENAME TO {to_schema}"
    args = SqlArgs(
        identifiers={
            "from_schema": str(from_schema),
            "to_schema": str(to_schema),
        }
    )
    return Query(query, args)
