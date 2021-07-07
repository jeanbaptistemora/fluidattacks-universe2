# pylint: skip-file

import boto3
import io
import logging
from postgres_client.client import (
    ClientFactory,
)
from postgres_client.cursor import (
    Cursor,
)
from postgres_client.schema import (
    SchemaFactory,
    SchemaID,
)
from postgres_client.table import (
    TableFactory,
)
from returns.curry import (
    partial,
)
from singer_io.factory import (
    singer_handler,
)
import sys
import target_redshift
from target_redshift.batcher import (
    Batcher,
)
from target_redshift.singer_handlers import (
    record_handler,
    schema_handler,
    SchemasMap,
    state_handler,
    StateId,
)
from typing import (
    Callable,
    IO,
    Optional,
)

LOG = logging.getLogger(__name__)


def persist_messages(
    batcher: Batcher,
    cursor: Cursor,
    schema_name: str,
    state_id: Optional[StateId] = None,
    update_table: bool = False,
) -> None:
    schemas: SchemasMap = {}
    factory = TableFactory(cursor)
    s3 = boto3.client("s3")
    handler: Callable[[str, SchemasMap], SchemasMap] = singer_handler(
        partial(schema_handler, batcher, factory, update_table, schema_name),
        partial(record_handler, batcher),
        partial(state_handler, s3, state_id),
    )
    for message in io.TextIOWrapper(sys.stdin.buffer, encoding="utf-8"):
        schemas = handler(message, schemas)
    batcher.flush()
    batcher.vacuum()


def load_data(
    auth_file: IO[str],
    schema_name: str,
    drop_schema_flag: bool,
    old: bool,
    state_id: Optional[StateId],
) -> None:
    """Usual entry point."""

    greeting = (
        "                                   ",
        " Singer target for Amazon Redshift ",
        "                                   ",
        "            ___                    ",
        "           | >>|> fluid            ",
        "           |___|  attacks          ",
        "                                   ",
        "       We hack your software       ",
        "                                   ",
        "     https://fluidattacks.com/     ",
        "                                   ",
    )

    LOG.info("\n".join(greeting))

    target_schema = SchemaID(schema_name)
    backup_schema = SchemaID(f"{target_schema}_backup")
    loading_schema = SchemaID(f"{target_schema}_loading")

    factory = ClientFactory()
    client = factory.from_conf(auth_file)
    schema_factory = SchemaFactory(client)
    dbcur = client.cursor.db_cursor
    try:
        if drop_schema_flag:
            # It means user wants to guarantee 100% data integrity
            # It also implies the use of a loading strategy
            #   to guarantee continuated service availability

            batcher = Batcher(dbcur, str(loading_schema))

            # The loading strategy is:
            #   RECREATE loading_schema
            schema_factory.recreate(loading_schema, cascade=True)
            #   LOAD loading_schema
            if old:
                # old version support
                target_redshift.persist_messages(batcher, str(loading_schema))
            else:
                persist_messages(
                    batcher, client.cursor, str(loading_schema), state_id
                )
            #   DROP backup_schema IF EXISTS
            schema_factory.try_retrieve(backup_schema).map(
                partial(schema_factory.delete, cascade=True)
            )
            # RENAME schemas
            schema_factory.try_retrieve(target_schema).map(
                partial(schema_factory.rename, new_name=backup_schema)
            )
            schema_factory.retrieve(loading_schema).map(
                partial(schema_factory.rename, new_name=target_schema)
            )
        else:
            # It means user only wants to push data and
            #   just cares about having it there.
            # The trade-off is:
            #     - data integrity
            #     - possible un-updated schema
            #     - and dangling/orphan/duplicated records
            batcher = Batcher(dbcur, str(target_schema))
            persist_messages(
                batcher, client.cursor, str(target_schema), state_id, True
            )
    finally:
        client.close()
