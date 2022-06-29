from enum import (
    Enum,
)
from fa_purity import (
    JsonObj,
    Maybe,
    Result,
    ResultE,
)
from fa_purity.json.value.transform import (
    Unfolder,
)
import logging
from redshift_client.data_type.core import (
    DataType,
    PrecisionType,
    PrecisionTypes,
    StaticTypes,
)
from typing import (
    Callable,
    TypeVar,
)

LOG = logging.getLogger(__name__)


_T = TypeVar("_T")


def _opt_transform(
    obj: JsonObj, key: str, transform: Callable[[Unfolder], _T]
) -> Maybe[_T]:
    return Maybe.from_optional(obj.get(key)).map(
        lambda p: transform(Unfolder(p))
    )


class _MetaType(Enum):
    STATIC = "static"
    DYNAMIC = "dynamic"


def _to_meta_type(raw: str) -> ResultE[_MetaType]:
    try:
        return Result.success(_MetaType(raw.lower()))
    except ValueError as err:
        return Result.failure(err)


def _format_handler(format: str, encoded: JsonObj) -> ResultE[DataType]:
    timezone: ResultE[bool] = _opt_transform(
        encoded,
        "timezone",
        lambda u: u.to_primitive(bool).alt(
            lambda e: Exception(f"Error at timezone. {e}")
        ),
    ).value_or(Result.success(False))
    if format == "date-time":
        return timezone.map(
            lambda t: StaticTypes.TIMESTAMPTZ if t else StaticTypes.TIMESTAMP
        ).map(DataType)
    elif format == "time":
        return timezone.map(
            lambda t: StaticTypes.TIMETZ if t else StaticTypes.TIME,
        ).map(DataType)
    elif format == "date":
        return Result.success(StaticTypes.DATE, Exception).map(
            lambda x: DataType(x)
        )
    err = NotImplementedError(f"Not supported format '{format}'")
    return Result.failure(err)


def _string_handler(encoded: JsonObj) -> ResultE[DataType]:
    precision: ResultE[int] = _opt_transform(
        encoded,
        "precision",
        lambda u: u.to_primitive(int).alt(
            lambda e: Exception(f"Error at precision. {e}")
        ),
    ).value_or(Result.success(256))
    meta_type: ResultE[_MetaType] = _opt_transform(
        encoded,
        "metatype",
        lambda u: u.to_primitive(str)
        .alt(Exception)
        .bind(_to_meta_type)
        .alt(lambda e: Exception(f"Error at metatype. {e}")),
    ).value_or(Result.success(_MetaType.STATIC))
    p_type = meta_type.map(
        lambda m: PrecisionTypes.CHAR
        if m is _MetaType.STATIC
        else PrecisionTypes.VARCHAR
    )
    return p_type.bind(
        lambda t: precision.map(lambda p: PrecisionType(t, p))
    ).map(DataType)


def string_format_handler(encoded: JsonObj) -> ResultE[DataType]:
    _format = _opt_transform(
        encoded,
        "format",
        lambda u: u.to_primitive(str).alt(
            lambda e: Exception(f"Error at format. {e}")
        ),
    )
    return _format.map(
        lambda r: r.bind(lambda f: _format_handler(f, encoded))
    ).or_else_call(lambda: _string_handler(encoded))
