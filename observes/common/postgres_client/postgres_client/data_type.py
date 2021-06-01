# pylint: skip-file

from enum import (
    Enum,
)
from returns.maybe import (
    Maybe,
)
from typing import (
    Dict,
)


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


def to_rs_datatype(raw: str) -> RedshiftDataType:
    raw_dt = raw.upper()
    dt = Maybe.from_optional(alias_map.get(raw_dt))
    return dt.or_else_call(lambda: RedshiftDataType(raw_dt))
