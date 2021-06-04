# pylint: skip-file
from __future__ import (
    annotations,
)

import jsonschema
from jsonschema.validators import (
    Draft4Validator,
)
from postgres_client.table import (
    Column,
    MetaTable,
    TableID,
)
from returns.primitives.types import (
    Immutable,
)
from singer_io.singer import (
    SingerSchema,
)
from target_redshift.data_types import (
    from_json,
)
from target_redshift.utils import (
    escape,
)
from typing import (
    NamedTuple,
)


def _extract_meta_table(
    db_schema: str, singer_schema: SingerSchema
) -> MetaTable:
    columns = frozenset(
        Column(escape(field), from_json(ftype))
        for field, ftype in singer_schema.schema["properties"].items()
    )
    table_id = TableID(db_schema, escape(singer_schema.stream.lower()))
    return MetaTable.new(table_id, frozenset(), columns)


class _RedshiftSchema(NamedTuple):
    table: MetaTable
    validator: Draft4Validator


def _from_singer(
    db_schema: str, singer_schema: SingerSchema
) -> _RedshiftSchema:
    validator = jsonschema.Draft4Validator(singer_schema.schema)
    table = _extract_meta_table(db_schema, singer_schema)
    return _RedshiftSchema(table, validator)


class RedshiftSchema(Immutable):
    table: MetaTable
    validator: Draft4Validator

    def __new__(
        cls, db_schema: str, singer_schema: SingerSchema
    ) -> RedshiftSchema:
        self = object.__new__(cls)
        obj = _from_singer(db_schema, singer_schema)
        for prop, val in obj._asdict().items():
            object.__setattr__(self, prop, val)
        return self
