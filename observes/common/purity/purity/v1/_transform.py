# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from __future__ import (
    annotations,
)

from dataclasses import (
    dataclass,
)
from purity.v2._patch import (
    Patch,
)
from returns.primitives.hkt import (
    SupportsKind2,
)
from typing import (
    Callable,
    TypeVar,
)

_A = TypeVar("_A")
_B = TypeVar("_B")


@dataclass(frozen=True)
class Transform(
    SupportsKind2["Transform[_A, _B]", _A, _B],
):
    _transform: Patch[Callable[[_A], _B]]

    def __init__(self, transform: Callable[[_A], _B]) -> None:
        object.__setattr__(self, "_transform", Patch(transform))

    def __call__(self, item: _A) -> _B:
        return self._transform.unwrap(item)
