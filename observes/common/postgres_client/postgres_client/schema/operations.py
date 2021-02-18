from postgres_client import table as table_module
from postgres_client import utils
from postgres_client.client import Client
from postgres_client.table import (
    factory as table_factory,
    operations as table_ops
)
from postgres_client.table import TableID
from postgres_client.schema import Schema


LOG = utils.get_log(__name__)


def migrate_all_tables(
    db_client: Client,
    from_schema: Schema,
    to_schema: Schema
) -> None:
    tables = from_schema.get_tables()
    LOG.info('Migrating %s to %s', from_schema, to_schema)
    LOG.debug('tables %s', str(tables))

    def move_table(table: str) -> None:
        source_table = TableID(schema=from_schema.name, table_name=table)
        target_table = TableID(schema=to_schema.name, table_name=table)
        LOG.debug('Moving from %s to %s ', source_table, target_table)
        if table_module.exist(db_client, target_table):
            LOG.debug('%s already exist', target_table)
            table_ops.delete(db_client, target_table)
        table_factory.create_like(
            db_client, source_table, target_table
        )
        table_ops.move(db_client, source_table, target_table)

    list(map(move_table, tables))
