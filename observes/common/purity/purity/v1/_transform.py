from __future__ import (
    annotations,
)

from dataclasses import (
    dataclass,
)
from purity.v1._patch import (
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
