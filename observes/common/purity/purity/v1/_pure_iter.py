from __future__ import (
    annotations,
)

from collections import (
    deque,
)
from dataclasses import (
    dataclass,
)
from itertools import (
    chain,
    count,
)
from purity.v1._frozen import (
    FrozenList,
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
from returns.unsafe import (
    unsafe_perform_io,
)
from typing import (
    Callable,
    Iterable,
    Iterator,
    Optional,
    TypeVar,
    Union,
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


Mappable = Union[FrozenList[_I], PureIter[_I]]


@dataclass(frozen=True)
class PureIterFactory:
    @staticmethod
    def from_flist(items: FrozenList[_I]) -> PureIter[_I]:
        draft = _PureIter(Patch(lambda: items))
        return PureIter(draft)

    @staticmethod
    def map(function: Callable[[_I], _R], items: Mappable[_I]) -> PureIter[_R]:
        def gen() -> Iterable[_R]:
            return (function(i) for i in items)

        draft = _PureIter(Patch(lambda: iter(gen())))
        return PureIter(draft)

    @classmethod
    def infinite_map(
        cls, function: Callable[[int], _R], start: int, step: int
    ) -> PureIter[_R]:
        draft = _PureIter(Patch(lambda: count(start, step)))
        return cls.map(function, PureIter(draft))

    @staticmethod
    def map_range(function: Callable[[int], _R], items: range) -> PureIter[_R]:
        def gen() -> Iterable[_R]:
            return (function(i) for i in items)

        draft = _PureIter(Patch(lambda: iter(gen())))
        return PureIter(draft)

    @staticmethod
    def filter(
        function: Callable[[_I], Optional[_R]], items: Mappable[_I]
    ) -> PureIter[_R]:
        def filtered() -> Iterable[_R]:
            raw = (function(i) for i in items)
            return (i for i in raw if i is not None)

        draft = _PureIter(Patch(lambda: iter(filtered())))
        return PureIter(draft)

    @staticmethod
    def filter_range(
        function: Callable[[int], Optional[_R]], items: range
    ) -> PureIter[_R]:
        def filtered() -> Iterable[_R]:
            raw = (function(i) for i in items)
            return (i for i in raw if i is not None)

        draft = _PureIter(Patch(lambda: iter(filtered())))
        return PureIter(draft)

    @staticmethod
    def until_empty(
        function: Callable[[_I], Optional[_R]], items: Mappable[_I]
    ) -> PureIter[_R]:
        def filtered() -> Iterable[_R]:
            raw = (function(i) for i in items)
            for item in raw:
                if item is None:
                    break
                yield item

        draft = _PureIter(Patch(lambda: iter(filtered())))
        return PureIter(draft)

    @staticmethod
    def until_empty_range(
        function: Callable[[int], Optional[_R]], items: range
    ) -> PureIter[_R]:
        def filtered() -> Iterable[_R]:
            raw = (function(i) for i in items)
            for item in raw:
                if item is None:
                    break
                yield item

        draft = _PureIter(Patch(lambda: iter(filtered())))
        return PureIter(draft)

    @staticmethod
    def chain_lists(
        unchained: PureIter[IO[FrozenList[_I]]],
    ) -> PureIter[IO[_I]]:
        def iters() -> Iterable[FrozenList[_I]]:
            for piter in unchained:
                yield unsafe_perform_io(piter)

        def chained() -> Iterable[IO[_I]]:
            return map(lambda x: IO(x), chain.from_iterable(iters()))

        return PureIter(_PureIter(Patch(lambda: chained())))
