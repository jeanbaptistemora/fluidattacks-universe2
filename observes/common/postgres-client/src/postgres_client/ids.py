from __future__ import (
    annotations,
)

from returns.primitives.types import (
    Immutable,
)


class SchemaID(Immutable):
    name: str

    def __new__(cls, raw: str) -> SchemaID:
        self = object.__new__(cls)
        object.__setattr__(self, "name", raw.lower())
        return self

    def __str__(self) -> str:
        return self.name


# pylint: disable=too-few-public-methods
class TableID(Immutable):
    schema: SchemaID
    table_name: str

    def __new__(cls, schema: SchemaID, table_name: str) -> TableID:
        self = object.__new__(cls)
        object.__setattr__(self, "schema", schema)
        object.__setattr__(self, "table_name", table_name.lower())
        return self
