from __future__ import (
    annotations,
)

from collections import (
    deque,
)
from dataclasses import (
    dataclass,
)
from purity.v1._patch import (
    Patch,
)
from returns.io import (
    IO,
)
from returns.primitives.hkt import (
    SupportsKind1,
)
from typing import (
    Callable,
    Iterable,
    Iterator,
    TypeVar,
)

_I = TypeVar("_I")
_R = TypeVar("_R")


@dataclass(frozen=True)
class _PureIter(
    SupportsKind1["_PureIter[_I]", _I],
):
    _iter_obj: Patch[Callable[[], Iterable[_I]]]


class PureIter(_PureIter[_I]):
    def __init__(self, obj: _PureIter[_I]):
        super().__init__(obj._iter_obj)

    def __iter__(self) -> Iterator[_I]:
        return iter(self._iter_obj.unwrap())

    def map_each(self, function: Callable[[_I], _R]) -> PureIter[_R]:
        draft = _PureIter(Patch(lambda: map(function, self)))
        return PureIter(draft)

    @staticmethod
    def consume(p_iter: PureIter[IO[None]]) -> IO[None]:
        deque(p_iter, maxlen=0)
        return IO(None)
