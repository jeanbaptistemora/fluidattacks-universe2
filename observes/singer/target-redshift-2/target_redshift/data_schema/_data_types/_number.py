from .._utils import (
    opt_transform,
)
from enum import (
    Enum,
)
from fa_purity import (
    JsonObj,
    Result,
    ResultE,
)
from redshift_client.data_type.core import (
    DataType,
    DecimalType,
    StaticTypes,
)


class _NumSizes(Enum):
    FLOAT = "float"
    BIG_FLOAT = "big_float"
    EXACT = "exact"


def _to_size(raw: str) -> ResultE[_NumSizes]:
    try:
        return Result.success(_NumSizes(raw.lower()))
    except ValueError as err:
        return Result.failure(err)


def _decimal_handler(encoded: JsonObj) -> ResultE[DataType]:
    precision: ResultE[int] = opt_transform(
        encoded,
        "precision",
        lambda u: u.to_primitive(int).alt(
            lambda e: Exception(f"Error at precision. {e}")
        ),
    ).value_or(Result.success(18))
    scale: ResultE[int] = opt_transform(
        encoded,
        "scale",
        lambda u: u.to_primitive(int).alt(
            lambda e: Exception(f"Error at scale. {e}")
        ),
    ).value_or(Result.success(0))
    return precision.bind(
        lambda p: scale.map(lambda s: DataType(DecimalType(p, s)))
    )


def _size_map(size: _NumSizes, encoded: JsonObj) -> ResultE[DataType]:
    if size is _NumSizes.EXACT:
        return _decimal_handler(encoded)
    if size is _NumSizes.FLOAT:
        return Result.success(StaticTypes.REAL, Exception).map(DataType)
    if size is _NumSizes.BIG_FLOAT:
        return Result.success(StaticTypes.DOUBLE_PRECISION, Exception).map(
            DataType
        )


def num_handler(encoded: JsonObj) -> ResultE[DataType]:
    _size: ResultE[_NumSizes] = opt_transform(
        encoded,
        "size",
        lambda u: u.to_primitive(str)
        .alt(lambda e: Exception(f"Error at size. {e}"))
        .bind(_to_size),
    ).value_or(Result.success(_NumSizes.FLOAT))
    return _size.bind(lambda s: _size_map(s, encoded))
