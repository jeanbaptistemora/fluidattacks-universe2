# pylint: skip-file

from migrate_tables import (
    utils,
)
from postgres_client import (
    client as client_module,
)
from postgres_client.client import (
    Client,
)
from postgres_client.ids import (
    SchemaID,
)
from postgres_client.schema import (
    Schema,
    SchemaFactory,
)
from returns.io import (
    IO,
)
from returns.pipeline import (
    is_successful,
)
from returns.unsafe import (
    unsafe_perform_io,
)
from typing import (
    IO as IOData,
    List,
)

LOG = utils.get_log(__name__)


def main(
    auth_file: IOData[str], tables: List[str], target_schema: str
) -> IO[None]:
    db_client = client_module.new_client_from_conf(auth_file)
    schema_factory = SchemaFactory(db_client)
    target = unsafe_perform_io(
        schema_factory.retrieve(SchemaID(target_schema))
    )
    for table in tables:
        table = table.lower()
        LOG.debug("Processing dymo table: %s", table)
        source_result = schema_factory.try_retrieve(
            SchemaID(f"dynamodb_{table}")
        )
        if is_successful(source_result):
            source = unsafe_perform_io(source_result.unwrap())
            source.migrate(target)
            schema_factory.delete(source, True)
        else:
            LOG.info("Schema: %s does not exist", source_result)
    return IO(None)
