from __future__ import (
    annotations,
)

from dataclasses import (
    dataclass,
)
import more_itertools
from purity.v2.cmd import (
    Cmd,
    unsafe_unwrap,
)
from purity.v2.frozen import (
    FrozenList,
)
from typing import (
    Callable,
    Generic,
    Iterable,
    Iterator,
    TypeVar,
)

_T = TypeVar("_T")
_R = TypeVar("_R")


@dataclass(frozen=True)
class _PureIter(
    Generic[_T],
):
    # In this case Cmd models mutation not side effects
    _new_iter: Cmd[Iterable[_T]]


def _chunked(items: Iterable[_T], size: int) -> Iterator[FrozenList[_T]]:
    return iter(map(lambda l: tuple(l), more_itertools.chunked(items, size)))


class PureIter(_PureIter[_T]):
    def __init__(self, obj: _PureIter[_T]):
        super().__init__(obj._new_iter)

    def map(self, function: Callable[[_T], _R]) -> PureIter[_R]:
        draft: _PureIter[_R] = _PureIter(
            self._new_iter.map(lambda i: iter(map(function, i)))
        )
        return PureIter(draft)

    def chunked(self, size: int) -> PureIter[FrozenList[_T]]:
        draft = _PureIter(self._new_iter.map(lambda i: _chunked(i, size)))
        return PureIter(draft)

    def to_list(self) -> FrozenList[_T]:
        # all cmds will result in same output
        cmd = self._new_iter.map(lambda x: tuple(x))
        return unsafe_unwrap(cmd)

    def __iter__(self) -> Iterator[_T]:
        # all cmds will result in an equivalent new iterator
        return iter(unsafe_unwrap(self._new_iter))
