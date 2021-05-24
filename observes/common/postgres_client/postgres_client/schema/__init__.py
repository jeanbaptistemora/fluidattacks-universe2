# Standard libraries
from __future__ import annotations
from typing import (
    Iterator,
    NamedTuple,
)

# Third party libraries
from returns.io import IO
from returns.unsafe import unsafe_perform_io

# Local libraries
from postgres_client import utils
from postgres_client.cursor import Cursor
from postgres_client.client import Client
from postgres_client.schema import _queries as queries
from postgres_client.table import DbTable
from postgres_client.table.common import TableID

LOG = utils.get_log(__name__)


class Schema(NamedTuple):
    cursor: Cursor
    name: str
    redshift: bool

    def get_tables(self) -> Iterator[str]:
        query = queries.get_tables(self.name)
        self.cursor.execute_query(query)
        return (item[0] for item in unsafe_perform_io(self.cursor.fetch_all()))

    def exist_on_db(self) -> bool:
        query = queries.exist(self.name)
        self.cursor.execute_query(query)
        return unsafe_perform_io(self.cursor.fetch_one())[1][0]

    def delete_on_db(self) -> IO[None]:
        query = queries.delete(self.name)
        self.cursor.execute_query(query)
        return IO(None)

    def migrate(self, to_schema: Schema) -> IO[None]:
        from_schema = self
        tables = from_schema.get_tables()
        LOG.info("Migrating %s to %s", from_schema, to_schema)
        LOG.debug("tables %s", str(tables))

        def move_table(table: str) -> None:
            source = TableID(schema=from_schema.name, table_name=table)
            target = TableID(schema=to_schema.name, table_name=table)
            source_table = DbTable.retrieve(self.cursor, source, self.redshift)
            LOG.debug("Moving from %s to %s ", source, target)
            source_table.map(lambda t: t.move(target))

        for table in tables:
            move_table(table)
        return IO(None)

    @classmethod
    def new(cls, client: Client, name: str, redshift: bool = True) -> Schema:
        return cls(cursor=client.cursor, name=name, redshift=redshift)
