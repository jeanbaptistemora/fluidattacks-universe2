# Standard libraries
from typing import (
    FrozenSet,
    NamedTuple,
    Tuple,
)

# Third party libraries
# Local libraries
from postgres_client.table import DbTypes


class RedshiftField(NamedTuple):
    name: str
    dbtype: DbTypes


class RedshiftSchema(NamedTuple):
    fields: FrozenSet[RedshiftField]
    schema_name: str
    table_name: str


class RedshiftRecord(NamedTuple):
    r_schema: RedshiftSchema
    record: FrozenSet[Tuple[str, str]]


class AmbiguousType(Exception):
    pass


class InvalidState(Exception):
    pass


class InvalidType(Exception):
    pass
