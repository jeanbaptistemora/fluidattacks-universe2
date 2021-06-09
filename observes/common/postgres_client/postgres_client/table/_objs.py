# pylint: skip-file

from __future__ import (
    annotations,
)

from postgres_client.column import (
    Column,
)
from postgres_client.ids import (
    TableID,
)
from typing import (
    FrozenSet,
    NamedTuple,
)


class InvalidPrimaryKey(Exception):
    pass


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
