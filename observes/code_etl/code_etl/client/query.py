from code_etl.client.decoder import (
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
