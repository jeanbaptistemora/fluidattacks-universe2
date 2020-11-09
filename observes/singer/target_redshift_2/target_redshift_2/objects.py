# Standard libraries
from typing import (
    FrozenSet,
    NamedTuple,
    Tuple,
)
# Third party libraries
# Local libraries
from target_redshift_2.db_client import DbTypes


class RedshiftField(NamedTuple):
    type: DbTypes
    name: str


class RedshiftSchema(NamedTuple):
    fields: FrozenSet[RedshiftField]
    schema_name: str
    table_name: str


class RedshiftRecord(NamedTuple):
    r_schema: RedshiftSchema
    record: FrozenSet[Tuple[str, str]]
