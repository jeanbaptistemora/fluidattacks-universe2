# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from fa_purity.frozen import (
    FrozenList,
)
from fa_purity.json.primitive.core import (
    is_primitive,
    Primitive,
)
from fa_purity.result import (
    Result,
    ResultE,
)
from fa_purity.result.transform import (
    all_ok,
)
from typing import (
    Callable,
    TypeVar,
)

_T = TypeVar("_T")
_R = TypeVar("_R")


def to_prim_val(raw: _T) -> ResultE[Primitive]:
    if is_primitive(raw):
        return Result.success(raw)
    return Result.failure(
        TypeError(f"Got {type(raw)}; expected a PrimitiveVal")
    )


def to_list_of(
    items: FrozenList[_T], assertion: Callable[[_T], ResultE[_R]]
) -> ResultE[FrozenList[_R]]:
    return all_ok(tuple(assertion(i) for i in items))


def to_prim_list(items: FrozenList[_T]) -> ResultE[FrozenList[Primitive]]:
    return all_ok(tuple(to_prim_val(i) for i in items))
