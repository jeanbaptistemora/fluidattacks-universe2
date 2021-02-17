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
