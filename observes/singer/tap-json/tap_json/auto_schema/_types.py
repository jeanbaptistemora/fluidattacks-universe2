from datetime import (
    datetime,
)
from dateutil.parser import (
    parse as date_parser,
    ParserError,
)
from decimal import (
    Decimal,
)
from enum import (
    Enum,
)
from fa_purity import (
    FrozenList,
    Result,
    ResultE,
)
from fa_purity.json.primitive import (
    Primitive,
)
from typing import (
    TypeVar,
)

_T = TypeVar("_T")


class SupportedTypes(Enum):
    DATETIME = "datetime"
    BOOL = "bool"
    INT = "int"
    FLOAT = "float"
    STR = "str"
    EMPTY = "EmptyStr"


def to_date(date_time: _T) -> ResultE[datetime]:
    """Manipulate a date to provide a RFC339 compatible date."""
    if isinstance(date_time, str):
        try:
            return Result.success(date_parser(date_time))
        except ParserError as err:
            return Result.failure(Exception(err))
    error = TypeError(
        f"Expected a `str` to try datetime tranform; got {type(date_time)}"
    )
    return Result.failure(Exception(error))


def item_type(item: Primitive) -> SupportedTypes:
    """Return the python type of a Structura."""
    if to_date(item).map(lambda _: True).value_or(False):
        return SupportedTypes.DATETIME
    if isinstance(item, bool):
        return SupportedTypes.BOOL
    if isinstance(item, int):
        if item in range(-2147483648, 2147483648):
            return SupportedTypes.INT
        return SupportedTypes.STR
    if isinstance(item, float):
        return SupportedTypes.FLOAT
    if isinstance(item, str):
        return SupportedTypes.STR if item != "" else SupportedTypes.EMPTY
    if isinstance(item, Decimal):
        return SupportedTypes.FLOAT
    return SupportedTypes.EMPTY


def merge_types(types: FrozenList[SupportedTypes]) -> SupportedTypes:
    priority = [
        SupportedTypes.EMPTY,
        SupportedTypes.BOOL,
        SupportedTypes.INT,
        SupportedTypes.FLOAT,
        SupportedTypes.DATETIME,
        SupportedTypes.STR,
    ]
    return priority[max(map(priority.index, types))]
