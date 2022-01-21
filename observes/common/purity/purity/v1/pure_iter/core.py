from __future__ import (
    annotations,
)

from dataclasses import (
    dataclass,
)
import more_itertools
from purity.v2._patch import (
    Patch,
)
from returns.io import (
    IO,
)
from returns.primitives.hkt import (
    SupportsKind1,
)
from returns.unsafe import (
    unsafe_perform_io,
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
    _iter_obj: Patch[Callable[[], IO[Iterable[_I]]]]


class PureIter(_PureIter[_I]):
    def __init__(self, obj: _PureIter[_I]):
        super().__init__(obj._iter_obj)

    def __iter__(self) -> Iterator[_I]:
        # unsafe used for compatibility
        return iter(unsafe_perform_io(self._iter_obj.unwrap()))

    def map(self, function: Callable[[_I], _R]) -> PureIter[_R]:
        draft: _PureIter[_R] = _PureIter(
            Patch(lambda: IO(iter(map(function, self))))
        )
        return PureIter(draft)

    def chunked(self, size: int) -> PureIter[PureIter[_I]]:
        draft: _PureIter[PureIter[_I]] = _PureIter(
            Patch(
                lambda: IO(
                    iter(
                        map(
                            lambda items: PureIter(
                                _PureIter(Patch(lambda: IO(tuple(items))))
                            ),
                            more_itertools.chunked(self, size),
                        )
                    )
                )
            )
        )
        return PureIter(draft)
