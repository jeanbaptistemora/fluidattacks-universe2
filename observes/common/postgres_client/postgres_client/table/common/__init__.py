# Standard libraries
from __future__ import annotations
from typing import (
    FrozenSet,
    NamedTuple,
)

# Local libraries
from postgres_client.table.common.column import Column


class InvalidPrimaryKey(Exception):
    pass


class TableID(NamedTuple):
    schema: str
    table_name: str

    @classmethod
    def new(cls, schema: str, table_name: str) -> TableID:
        return cls(schema=schema, table_name=table_name)


class MetaTable(NamedTuple):
    table_id: TableID
    primary_keys: FrozenSet[str]
    columns: FrozenSet[Column]
    path: str

    @classmethod
    def new(
        cls,
        table_id: TableID,
        primary_keys: FrozenSet[str],
        columns: FrozenSet[Column],
    ) -> MetaTable:
        columns_names = [col.name for col in columns]
        invalid_keys = list(
            filter(lambda key: key not in columns_names, primary_keys)
        )
        if invalid_keys:
            raise InvalidPrimaryKey(str(invalid_keys))
        return cls(
            table_id=table_id,
            primary_keys=primary_keys,
            columns=columns,
            path=f'"{table_id.schema}"."{table_id.table_name}"',
        )
