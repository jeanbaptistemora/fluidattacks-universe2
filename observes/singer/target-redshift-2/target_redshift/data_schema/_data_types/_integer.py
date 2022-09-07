# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

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
    StaticTypes,
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
    _size: ResultE[_IntSizes] = opt_transform(
        encoded,
        "size",
        lambda u: u.to_primitive(str)
        .alt(lambda e: Exception(f"Error at size. {e}"))
        .bind(_to_size),
    ).value_or(Result.success(_IntSizes.NORMAL))
    return _size.map(_size_map)
