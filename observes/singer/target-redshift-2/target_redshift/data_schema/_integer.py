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


class _IntSizes(Enum):
    SMALL = "small"
    NORMAL = "normal"
    BIG = "big"


def _to_size(raw: str) -> ResultE[_IntSizes]:
    try:
        return Result.success(_IntSizes(raw.lower()))
    except ValueError as err:
        return Result.failure(err)


def _size_map(size: _IntSizes) -> DataType:
    if size is _IntSizes.SMALL:
        return DataType(StaticTypes.SMALLINT)
    if size is _IntSizes.NORMAL:
        return DataType(StaticTypes.INTEGER)
    if size is _IntSizes.BIG:
        return DataType(StaticTypes.BIGINT)


def int_handler(encoded: JsonObj) -> ResultE[DataType]:
    _size: ResultE[_IntSizes] = _opt_transform(
        encoded,
        "size",
        lambda u: u.to_primitive(str)
        .alt(lambda e: Exception(f"Error at size. {e}"))
        .bind(_to_size),
    ).value_or(Result.success(_IntSizes.NORMAL))
    return _size.map(_size_map)
