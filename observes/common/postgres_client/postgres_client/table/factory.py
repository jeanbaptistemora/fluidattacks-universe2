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


def create_like(
    db_client: Client,
    blueprint: TableID,
    new_table: TableID
) -> TableID:
    statement = """
        CREATE TABLE {new_schema}.{new_table} (
            LIKE {blueprint_schema}.{blueprint_table}
        );
    """
    identifiers: Dict[str, Optional[str]] = {
        'new_schema': new_table.schema,
        'new_table': new_table.table_name,
        'blueprint_schema': blueprint.schema,
        'blueprint_table': blueprint.table_name
    }
    args = DynamicSQLargs(
        identifiers=identifiers
    )
    action = db_client.cursor.execute(statement, args)
    action.act()
    return new_table
