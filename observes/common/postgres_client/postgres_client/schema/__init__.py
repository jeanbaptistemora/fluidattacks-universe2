# Standard libraries
from __future__ import annotations

from typing import (
    Iterator,
    NamedTuple,
)

# Third party libraries
from returns.io import IO

# Local libraries
from postgres_client import utils
from postgres_client.cursor import Cursor, act
from postgres_client.client import Client
from postgres_client.schema import _queries as queries
from postgres_client.table import DbTable
from postgres_client.table.common import TableID

LOG = utils.get_log(__name__)


class Schema(NamedTuple):
    client: Client
    name: str

    def get_tables(self) -> Iterator[str]:
        actions = queries.get_tables(self.client.cursor, self.name)
        return (item[0] for item in act(actions)[1])

    def exist_on_db(self) -> bool:
        actions = queries.exist_on_db(self.client.cursor, self.name)
        return act(actions)[1][0]

    def delete_on_db(self) -> None:
        action = queries.delete_on_db(self.client.cursor, self.name)
        action.act()

    def move(self, cursor: Cursor, to_schema: Schema) -> IO[None]:
        from_schema = self
        tables = from_schema.get_tables()
        LOG.info("Migrating %s to %s", from_schema, to_schema)
        LOG.debug("tables %s", str(tables))

        def move_table(table: str) -> None:
            source = TableID(schema=from_schema.name, table_name=table)
            target = TableID(schema=to_schema.name, table_name=table)
            source_table = DbTable.retrieve(cursor, source)
            LOG.debug("Moving from %s to %s ", source, target)
            source_table.map(lambda t: t.move(target))

        for table in tables:
            move_table(table)
        return IO(None)

    @classmethod
    def new(cls, client: Client, name: str) -> Schema:
        return cls(client=client, name=name)
