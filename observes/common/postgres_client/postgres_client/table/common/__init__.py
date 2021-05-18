# Standard libraries
from __future__ import annotations
from typing import (
    NamedTuple,
)


class TableID(NamedTuple):
    schema: str
    table_name: str

    @classmethod
    def new(cls, schema: str, table_name: str) -> TableID:
        return cls(schema=schema, table_name=table_name)
