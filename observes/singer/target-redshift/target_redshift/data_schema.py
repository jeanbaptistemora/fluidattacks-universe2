# pylint: skip-file
from __future__ import (
    annotations,
)

import jsonschema
from jsonschema.validators import (
    Draft4Validator,
)
import logging
from postgres_client.column import (
    ColumnType,
)
from postgres_client.schema import (
    SchemaID,
)
from postgres_client.table import (
    Column,
    MetaTable,
    TableID,
)
from returns.primitives.types import (
    Immutable,
)
from singer_io import (
    JSON,
)
from singer_io.singer import (
    SingerSchema,
)
from target_redshift.data_types import (
    from_json,
)
from typing import (
    NamedTuple,
)

LOG = logging.getLogger(__name__)


def _extract_meta_table(
    db_schema: str, singer_schema: SingerSchema
) -> MetaTable:
    columns = frozenset(
        Column(
            field,
            ColumnType(from_json(ftype)),
        )
        for field, ftype in singer_schema.schema["properties"].items()
    )
    table_id = TableID(SchemaID(db_schema), singer_schema.stream)
    return MetaTable.new(
        table_id, frozenset(singer_schema.key_properties), columns
    )


class _RedshiftSchema(NamedTuple):
    table: MetaTable
    validator: Draft4Validator


def _validate_schema(validator: Draft4Validator, schema: JSON) -> None:
    """Prints the validation of a JSON by using the provided validator."""
    try:
        validator.check_schema(schema)
    except jsonschema.exceptions.SchemaError as err:
        LOG.critical("ERROR: schema did not conform to draft 4.")
        raise err


def _from_singer(
    db_schema: str, singer_schema: SingerSchema
) -> _RedshiftSchema:
    validator = jsonschema.Draft4Validator(singer_schema.schema)
    _validate_schema(validator, singer_schema.schema)
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
