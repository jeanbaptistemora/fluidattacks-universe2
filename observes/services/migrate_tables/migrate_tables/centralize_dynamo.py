# pylint: skip-file
# Standard libraries
from typing import (
    IO,
    List,
)

# Third party libraries
from returns.pipeline import is_successful
from returns.unsafe import unsafe_perform_io

# Local libraries
from postgres_client import client as client_module
from postgres_client.client import Client
from postgres_client.schema import Schema, SchemaFactory
from postgres_client.schema import operations as schema_ops

# Self libraries
from migrate_tables import utils


LOG = utils.get_log(__name__)


def main(auth_file: IO[str], tables: List[str], target_schema: str) -> None:
    db_client = client_module.new_client_from_conf(auth_file)
    schema_factory = SchemaFactory.new(db_client)
    target = schema_factory.retrieve(f"{target_schema}")
    for table in tables:
        table = table.lower()
        LOG.debug("Processing dymo table: %s", table)
        source = schema_factory.try_retrieve(f"dynamodb_{table}")
        if is_successful(source):
            LOG.debug("Migrating: %s", table)
            schema_ops.migrate_all_tables(
                db_client,
                unsafe_perform_io(source.unwrap()),
                unsafe_perform_io(target),
            )
            source.map(lambda schema: schema.delete_on_db())
        else:
            LOG.info("Schema: %s does not exist", source)
