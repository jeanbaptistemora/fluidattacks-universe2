# pylint: skip-file

from __future__ import (
    annotations,
)

import logging
from postgres_client.client import (
    Client,
)
from postgres_client.cursor import (
    Cursor,
)
from postgres_client.schema import (
    _queries as queries,
)
from postgres_client.table import (
    TableFactory,
    TableID,
)
from returns.io import (
    IO,
    IOFailure,
    IOResult,
    IOSuccess,
)
from returns.pipeline import (
    is_successful,
)
from returns.primitives.types import (
    Immutable,
)
from returns.unsafe import (
    unsafe_perform_io,
)
from typing import (
    Iterator,
    Literal,
    NamedTuple,
    NoReturn,
)

LOG = logging.getLogger(__name__)
IOResultBool = IOResult[Literal[True], Literal[False]]


def _raise(excep: Exception) -> NoReturn:
    raise excep


def _exist(cursor: Cursor, schema: str) -> IOResultBool:
    query = queries.exist(schema)
    cursor.execute_query(query)
    result = cursor.fetch_one().map(lambda elem: elem[0])
    if result == IO(True):
        return IOSuccess(True)
    return IOFailure(False)


class SchemaNotExist(Exception):
    pass


class _Schema(NamedTuple):
    cursor: Cursor
    name: str
    redshift: bool


class Schema(Immutable):
    """Use SchemaFactory for building a Schema element"""

    cursor: Cursor
    name: str
    redshift: bool

    def __new__(cls, obj: _Schema) -> Schema:
        self = object.__new__(cls)
        for prop, val in obj._asdict().items():
            object.__setattr__(self, prop, val)
        return self

    def __str__(self) -> str:
        return "Schema(name={}, redshift={})".format(self.name, self.redshift)

    def get_tables(self) -> Iterator[str]:
        query = queries.get_tables(self.name)
        self.cursor.execute_query(query)
        return (item[0] for item in unsafe_perform_io(self.cursor.fetch_all()))

    def delete_on_db(self) -> IO[None]:
        query = queries.delete(self.name)
        self.cursor.execute_query(query)
        return IO(None)

    def migrate(self, to_schema: Schema) -> IO[None]:
        from_schema = self
        tables = from_schema.get_tables()
        LOG.info("Migrating %s to %s", from_schema, to_schema)
        LOG.debug("tables %s", str(tables))
        factory = TableFactory(self.cursor, self.redshift)

        def move_table(table: str) -> None:
            source = TableID(schema=from_schema.name, table_name=table)
            target = TableID(schema=to_schema.name, table_name=table)
            source_table = factory.retrieve(source)
            LOG.debug("Moving from %s to %s ", source, target)
            source_table.map(lambda t: factory.move(t.table.table_id, target))

        for table in tables:
            move_table(table)
        return IO(None)


class SchemaFactory(NamedTuple):
    client: Client

    def try_retrieve(
        self, name: str, redshift: bool = True
    ) -> IOResult[Schema, SchemaNotExist]:
        exists = _exist(self.client.cursor, name)
        if is_successful(exists):
            return IOSuccess(
                Schema(
                    _Schema(
                        cursor=self.client.cursor, name=name, redshift=redshift
                    )
                )
            )
        return IOFailure(SchemaNotExist(name))

    def retrieve(self, name: str, redshift: bool = True) -> IO[Schema]:
        result = self.try_retrieve(name, redshift)
        return result.alt(_raise).unwrap()

    def new_schema(self, name: str, redshift: bool = True) -> IO[Schema]:
        query = queries.create(name)
        self.client.cursor.execute_query(query)
        return self.retrieve(name, redshift)

    @classmethod
    def new(cls, client: Client) -> SchemaFactory:
        return cls(client)
