# Standard libraries
from __future__ import annotations
from enum import Enum
from typing import (
    NamedTuple,
    Optional,
)


# Supported JSON Schema types
class DbTypes(Enum):
    BOOLEAN = "BOOLEAN"
    NUMERIC = "NUMERIC(38)"
    FLOAT = "FLOAT8"
    VARCHAR = "VARCHAR"
    TIMESTAMP = "TIMESTAMP"


class Column(NamedTuple):
    name: str
    field_type: DbTypes
    default_val: Optional[str] = None

    @classmethod
    def new(
        cls, name: str, field_type: DbTypes, default_val: Optional[str]
    ) -> Column:
        return cls(name=name, field_type=field_type, default_val=default_val)


# old interface
class IsolatedColumn(NamedTuple):
    name: str
    field_type: str
    default_val: Optional[str] = None


def adapt(i_column: IsolatedColumn) -> Column:
    return Column.new(
        i_column.name,
        DbTypes(i_column.field_type.upper()),
        i_column.default_val,
    )
