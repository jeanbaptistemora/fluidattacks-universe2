from __future__ import (
    annotations,
)

from dataclasses import (
    dataclass,
)
from purity.v2 import (
    _iter_factory,
)
from purity.v2.cmd import (
    Cmd,
)
from purity.v2.frozen import (
    FrozenList,
)
from typing import (
    Callable,
    Generic,
    Iterable,
    TypeVar,
)

_T = TypeVar("_T")
_R = TypeVar("_R")


@dataclass(frozen=True)
class _Stream(
    Generic[_T],
):
    _new_iter: Cmd[Iterable[_T]]


class Stream(_Stream[_T]):
    def __init__(self, obj: _Stream[_T]):
        super().__init__(obj._new_iter)

    def map(self, function: Callable[[_T], _R]) -> Stream[_R]:
        draft: _Stream[_R] = _Stream(
            self._new_iter.map(lambda i: iter(map(function, i)))
        )
        return Stream(draft)

    def chunked(self, size: int) -> Stream[FrozenList[_T]]:
        draft = _Stream(
            self._new_iter.map(lambda i: _iter_factory.chunked(i, size))
        )
        return Stream(draft)

    def to_list(self) -> Cmd[FrozenList[_T]]:
        return self._new_iter.map(tuple)

    def unsafe_to_iter(self) -> Cmd[Iterable[_T]]:
        # if possible iterables should not be used directly
        return self._new_iter
