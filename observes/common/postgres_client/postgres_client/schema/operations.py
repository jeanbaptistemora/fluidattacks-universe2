from postgres_client import table as table_module
from postgres_client.client import Client
from postgres_client.table import TableID
from postgres_client.schema import Schema


def migrate_all_tables(
    db_client: Client,
    from_schema: Schema,
    to_schema: Schema
) -> None:
    tables = from_schema.get_tables()

    def move_table(table: str) -> None:
        source_table = TableID(schema=from_schema.name, table_name=table)
        target_table = TableID(schema=to_schema.name, table_name=table)
        if table_module.exist(db_client, target_table):
            table_module.operations.delete(db_client, target_table)
        table_module.factory.create_like(
            db_client, source_table, target_table
        )

    list(map(move_table, tables))
