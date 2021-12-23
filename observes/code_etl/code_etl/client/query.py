from code_etl.client.encoder import (
    CommitTableRow,
    RawRow,
)
from dataclasses import (
    fields,
)
from postgres_client.ids import (
    TableID,
)
from postgres_client.query import (
    Query,
    SqlArgs,
)


def all_data(table: TableID) -> Query:
    _attrs = ",".join([f.name for f in fields(RawRow)])
    args = SqlArgs(
        identifiers={
            "schema": table.schema.name,
            "table": table.table_name,
        }
    )
    return Query(f"SELECT {_attrs} FROM {{schema}}.{{table}}", args)


def all_data_count(table: TableID) -> Query:
    return Query(
        """
        SELECT COUNT(*) FROM {schema}.{table}
        """,
        SqlArgs(
            identifiers={
                "schema": table.schema.name,
                "table": table.table_name,
            }
        ),
    )


def insert_row(table: TableID) -> Query:
    _fields = ",".join(tuple(f.name for f in fields(CommitTableRow)))
    values = ",".join(tuple(f"%({f.name})s" for f in fields(CommitTableRow)))
    return Query(
        f"INSERT INTO {{schema}}.{{table}} ({_fields}) VALUES {values}",
        SqlArgs(
            identifiers={
                "schema": table.schema.name,
                "table": table.table_name,
            }
        ),
    )
