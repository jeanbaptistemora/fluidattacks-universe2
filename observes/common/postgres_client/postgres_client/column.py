# pylint: skip-file
from __future__ import (
    annotations,
)

from enum import (
    Enum,
)
import logging
from returns.maybe import (
    Maybe,
)
from returns.primitives.types import (
    Immutable,
)
from typing import (
    Any,
    Dict,
    NamedTuple,
    Optional,
)

LOG = logging.getLogger(__name__)


class RedshiftDataType(Enum):
    SMALLINT = "SMALLINT"
    INTEGER = "INTEGER"
    BIGINT = "BIGINT"
    DECIMAL = "DECIMAL"
    REAL = "REAL"
    DOUBLE_PRECISION = "DOUBLE PRECISION"
    BOOLEAN = "BOOLEAN"
    CHAR = "CHAR"
    VARCHAR = "VARCHAR"
    DATE = "DATE"
    TIMESTAMP = "TIMESTAMP"
    TIMESTAMPTZ = "TIMESTAMPTZ"
    TIME = "TIME"
    TIMETZ = "TIMETZ"


alias_map: Dict[str, RedshiftDataType] = {
    "INT2": RedshiftDataType.SMALLINT,
    "INT": RedshiftDataType.INTEGER,
    "INT4": RedshiftDataType.INTEGER,
    "INT8": RedshiftDataType.BIGINT,
    "NUMERIC": RedshiftDataType.DECIMAL,
    "FLOAT4": RedshiftDataType.REAL,
    "FLOAT8": RedshiftDataType.DOUBLE_PRECISION,
    "FLOAT": RedshiftDataType.DOUBLE_PRECISION,
    "BOOL": RedshiftDataType.BOOLEAN,
    "CHARACTER": RedshiftDataType.CHAR,
    "NCHAR": RedshiftDataType.CHAR,
    "BPCHAR": RedshiftDataType.CHAR,
    "CHARACTER VARYING": RedshiftDataType.VARCHAR,
    "NVARCHAR": RedshiftDataType.VARCHAR,
    "TEXT": RedshiftDataType.VARCHAR,
    "TIMESTAMP WITHOUT TIME ZONE": RedshiftDataType.TIMESTAMP,
    "TIMESTAMP WITH TIME ZONE": RedshiftDataType.TIMESTAMPTZ,
    "TIME WITHOUT TIME ZONE": RedshiftDataType.TIME,
    "TIME WITH TIME ZONE": RedshiftDataType.TIMETZ,
}

default_precision = {
    RedshiftDataType.CHAR: 1,
    RedshiftDataType.VARCHAR: 256,
    RedshiftDataType.DECIMAL: 18,
}
default_scale = {
    RedshiftDataType.DECIMAL: 0,
}
max_precision = {
    RedshiftDataType.CHAR: 4096,
    RedshiftDataType.VARCHAR: 65535,
}


def to_rs_datatype(raw: str) -> RedshiftDataType:
    raw_dt = raw.upper()
    dt = Maybe.from_optional(alias_map.get(raw_dt))
    return dt.or_else_call(lambda: RedshiftDataType(raw_dt))


class PrecisionRequired(Exception):
    pass


class _ColumnType(NamedTuple):
    field_type: RedshiftDataType
    precision: Optional[int]
    scale: Optional[int]
    default_val: Optional[str]
    nullable: bool


class ColumnType(Immutable):
    field_type: RedshiftDataType
    precision: Optional[int]
    scale: Optional[int]
    default_val: Optional[str]
    nullable: bool

    def __new__(
        cls,
        field_type: RedshiftDataType,
        precision: Optional[int] = None,
        scale: Optional[int] = None,
        default_val: Optional[str] = None,
        nullable: bool = True,
    ) -> ColumnType:
        _precision = Maybe.from_optional(precision).or_else_call(
            lambda: default_precision.get(field_type)
        )
        _scale = Maybe.from_optional(scale).or_else_call(
            lambda: default_scale.get(field_type)
        )
        self = object.__new__(cls)
        obj = _ColumnType(
            field_type, _precision, _scale, default_val, nullable
        )
        for prop, val in obj._asdict().items():
            object.__setattr__(self, prop, val)
        return self

    def __hash__(self) -> int:
        return hash(tuple(vars(self).values()))

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, ColumnType):
            return vars(self) == vars(other)
        return False

    def __repr__(self) -> str:
        return (
            "ColumnType(field_type={},precision={},"
            "default_val={},nullable={})"
        ).format(
            self.field_type,
            self.precision,
            self.default_val,
            self.nullable,
        )


class Column(NamedTuple):
    name: str
    c_type: ColumnType
