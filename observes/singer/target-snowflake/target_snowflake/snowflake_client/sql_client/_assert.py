# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from fa_purity import (
    FrozenList,
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


def to_list_of(
    items: FrozenList[_T], assertion: Callable[[_T], ResultE[_R]]
) -> ResultE[FrozenList[_R]]:
    return all_ok(tuple(assertion(i) for i in items))
