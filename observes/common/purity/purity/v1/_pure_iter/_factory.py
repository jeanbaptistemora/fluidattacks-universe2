from __future__ import (
    annotations,
)

from dataclasses import (
    dataclass,
)
from itertools import (
    count,
)
from purity.v1._frozen import (
    FrozenList,
)
from purity.v1._patch import (
    Patch,
)
from purity.v1._pure_iter._iter_factory import (
    IterableFactoryIO,
)
from purity.v1._pure_iter._obj import (
    _PureIter,
    Mappable,
    PureIter,
)
from returns.curry import (
    partial,
)
from returns.io import (
    IO,
)
from typing import (
    Callable,
    Iterable,
    Optional,
    TypeVar,
)

_I = TypeVar("_I")
_R = TypeVar("_R")


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
        unchained: PureIter[IO[Mappable[_I]]],
    ) -> PureIter[IO[_I]]:
        function = partial(IterableFactoryIO.chain_io, unchained)
        return PureIter(_PureIter(Patch(function)))
