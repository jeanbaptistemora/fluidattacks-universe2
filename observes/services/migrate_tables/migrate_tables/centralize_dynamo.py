# Standard libraries
from typing import (
    IO,
    List,
)
# Third party libraries
# Local libraries
from postgres_client import client as client_module
from postgres_client.client import Client
from postgres_client.schema import Schema
from postgres_client.schema import operations as schema_ops
from postgres_client.schema import factory as schema_factory


def get_associated_schema(db_client: Client, dymo_table: str) -> Schema:
    return schema_factory.db_schema(db_client, f'dynamodb_{dymo_table}')


def main(
    auth_file: IO[str],
    tables: List[str],
    target_schema: str
) -> None:
    db_client = client_module.new_client_from_conf(auth_file)
    target = schema_factory.db_schema(db_client, f'{target_schema}')
    for table in tables:
        source = get_associated_schema(db_client, table)
        if source.exist_on_db():
            schema_ops.migrate_all_tables(db_client, source, target)
