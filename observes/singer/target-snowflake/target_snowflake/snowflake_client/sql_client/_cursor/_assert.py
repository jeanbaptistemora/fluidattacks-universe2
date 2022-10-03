# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from fa_purity.frozen import (
    FrozenList,
)
from fa_purity.result import (
    Result,
    ResultE,
)
from fa_purity.result.transform import (
    all_ok,
)
from fa_purity.union import (
    UnionFactory,
)
from target_snowflake.snowflake_client.sql_client._primitive import (
    Primitive,
)
from typing import (
    Optional,
    TypeVar,
)

_T = TypeVar("_T")


class _AssertException(Exception):
    pass


def assert_fetch_one(
    result: Optional[_T],
) -> ResultE[Optional[FrozenList[Primitive]]]:
    _union: UnionFactory[None, FrozenList[Primitive]] = UnionFactory()
    if result is None:
        return Result.success(result)
    if isinstance(result, tuple):
        return Primitive.assert_primitive_list(result).map(_union.inr)
    return Result.failure(
        _AssertException(
            f"Expected `Optional[FrozenList[_T]]` but got {type(result)}"
        )
    )


def assert_fetch_list(item: _T) -> ResultE[FrozenList[FrozenList[Primitive]]]:
    if isinstance(item, tuple):
        return all_ok(tuple(Primitive.assert_primitive_list(i) for i in item))
    return Result.failure(
        _AssertException(f"Expected `FrozenList[_T]` but got {type(item)}")
    )
