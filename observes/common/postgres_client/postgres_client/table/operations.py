from postgres_client.client import (
    Client,
)
from postgres_client.table import (
    _queries as queries,
    TableID,
)
from returns.io import (
    IO,
)


def rename(db_client: Client, table: TableID, new_name: str) -> TableID:
    db_client.cursor.execute_query(queries.rename(table, new_name))
    return TableID(schema=table.schema, table_name=new_name)


def delete(
    db_client: Client,
    table: TableID,
) -> IO[None]:
    db_client.cursor.execute_query(queries.delete(table))
    return IO(None)


def move(
    db_client: Client,
    source: TableID,
    target: TableID,
) -> TableID:
    db_client.cursor.execute_queries(queries.redshift_move(source, target))
    return target
