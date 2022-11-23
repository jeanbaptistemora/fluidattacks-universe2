# pylint: skip-file

from __future__ import (
    annotations,
)

from psycopg2.sql import (
    Identifier,
    SQL,
)
from returns.maybe import (
    Maybe,
)
from returns.pipeline import (
    is_successful,
)
from returns.primitives.types import (
    Immutable,
)
from typing import (
    Dict,
    NamedTuple,
    Optional,
)


class SqlArgs(NamedTuple):
    values: Dict[str, Optional[str]] = {}
    identifiers: Dict[str, Optional[str]] = {}


def sql_id_purifier(statement: str, args: Maybe[SqlArgs] = Maybe.empty) -> str:
    raw_sql = SQL(statement)
    format_input = args.map(
        lambda sql_args: dict(
            (key, Identifier(value))
            for key, value in sql_args.identifiers.items()
        )
    )
    if is_successful(format_input):
        return raw_sql.format(**format_input.unwrap())
    return statement


class _Query(NamedTuple):
    query: str
    args: Maybe[SqlArgs]


class Query(Immutable):
    query: str
    args: Maybe[SqlArgs]

    def __new__(cls, query: str, args: Optional[SqlArgs] = None) -> Query:
        self = object.__new__(cls)
        _args = Maybe.from_optional(args)
        obj = _Query(query=sql_id_purifier(query, _args), args=_args)
        for prop, val in obj._asdict().items():
            object.__setattr__(self, prop, val)
        return self
