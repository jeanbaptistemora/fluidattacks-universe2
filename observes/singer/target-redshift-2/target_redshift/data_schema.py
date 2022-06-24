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


def _string_handler(encoded: JsonObj) -> ResultE[DataType]:
    precision = _opt_transform(
        encoded, "precision", lambda u: u.to_primitive(int).unwrap()
    ).value_or(256)
    meta_type: ResultE[_MetaType] = (
        _opt_transform(
            encoded, "meta_type", lambda u: u.to_primitive(str).unwrap()
        )
        .map(_to_meta_type)
        .value_or(Result.success(_MetaType.STATIC))
    )
    p_type = meta_type.map(
        lambda m: PrecisionTypes.CHAR
        if m is _MetaType.STATIC
        else PrecisionTypes.VARCHAR
    )
    return p_type.map(lambda t: PrecisionType(t, precision)).map(DataType)
