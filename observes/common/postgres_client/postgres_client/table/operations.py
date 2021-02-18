# Standard libraries
from typing import (
    Dict,
    Optional,
)
# Third party libraries
# Local libraries
from postgres_client.client import Client
from postgres_client.cursor import DynamicSQLargs
from postgres_client.table import TableID


def rename(
    db_client: Client,
    table: TableID,
    new_name: str
) -> TableID:
    statement = """
        ALTER TABLE {schema}.{table} RENAME TO {new_name};
    """
    identifiers: Dict[str, Optional[str]] = {
        'schema': table.schema,
        'table': table.table_name,
        'new_name': new_name,
    }
    args = DynamicSQLargs(
        identifiers=identifiers
    )
    action = db_client.cursor.execute(statement, args)
    action.act()
    return TableID(schema=table.schema, table_name=new_name)


def delete(
    db_client: Client,
    table: TableID,
) -> None:
    statement = """
        DROP TABLE {schema}.{table} CASCADE;
    """
    identifiers: Dict[str, Optional[str]] = {
        'schema': table.schema,
        'table': table.table_name,
    }
    args = DynamicSQLargs(
        identifiers=identifiers
    )
    action = db_client.cursor.execute(statement, args)
    action.act()


def move(
    db_client: Client,
    source: TableID,
    target: TableID,
) -> TableID:
    statement = (
        'ALTER TABLE {target_schema}.{target_table} '
        'APPEND FROM {source_schema}.{source_table};'
    )
    identifiers: Dict[str, Optional[str]] = {
        'source_schema': source.schema,
        'source_table': source.table_name,
        'target_schema': target.schema,
        'target_table': target.table_name,
    }
    args = DynamicSQLargs(
        identifiers=identifiers
    )
    action = db_client.cursor.execute(statement, args)
    action.act()
    delete(db_client, source)
    return target
