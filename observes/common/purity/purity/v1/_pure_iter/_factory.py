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
    IterableFactory,
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
from returns.maybe import (
    Maybe,
)
from typing import (
    Callable,
    Optional,
    TypeVar,
)

_I = TypeVar("_I")
_R = TypeVar("_R")


@dataclass(frozen=True)
class PureIterFactory:
    @staticmethod
    def chain(
        unchained: PureIter[Mappable[_I]],
    ) -> PureIter[_I]:
        function = partial(IterableFactory.chain, unchained)
        return PureIter(_PureIter(Patch(function)))

    @staticmethod
    def filter(items: PureIter[Optional[_I]]) -> PureIter[_I]:
        draft = _PureIter(
            Patch(lambda: iter(IterableFactory.filter_none(items)))
        )
        return PureIter(draft)

    @staticmethod
    def from_flist(items: FrozenList[_I]) -> PureIter[_I]:
        draft = _PureIter(Patch(lambda: items))
        return PureIter(draft)

    @classmethod
    def infinite_map(
        cls, function: Callable[[int], _R], start: int, step: int
    ) -> PureIter[_R]:
        draft = _PureIter(Patch(lambda: count(start, step)))
        return cls.map(function, PureIter(draft))

    @staticmethod
    def map(function: Callable[[_I], _R], items: Mappable[_I]) -> PureIter[_R]:
        draft = _PureIter(
            Patch(lambda: iter(IterableFactory.map(function, items)))
        )
        return PureIter(draft)

    @staticmethod
    def map_range(function: Callable[[int], _R], items: range) -> PureIter[_R]:
        draft = _PureIter(
            Patch(lambda: iter(IterableFactory.map_range(function, items)))
        )
        return PureIter(draft)

    @staticmethod
    def until_none(items: PureIter[Optional[_I]]) -> PureIter[_I]:
        draft = _PureIter(
            Patch(lambda: iter(IterableFactory.until_none(items)))
        )
        return PureIter(draft)

    @classmethod
    def until_empty(cls, items: PureIter[Maybe[_I]]) -> PureIter[_I]:
        def _to_opt(item: Maybe[_I]) -> Optional[_I]:
            return item.value_or(None)

        opt: PureIter[Optional[_I]] = cls.map(_to_opt, items)
        return cls.until_none(opt)


class PureIterIOFactory:
    @staticmethod
    def chain(
        unchained: PureIter[IO[Mappable[_I]]],
    ) -> PureIter[IO[_I]]:
        function = partial(IterableFactoryIO.chain_io, unchained)
        return PureIter(_PureIter(Patch(function)))

    @staticmethod
    def until_none(items: PureIter[IO[Optional[_I]]]) -> PureIter[IO[_I]]:
        draft = _PureIter(
            Patch(lambda: iter(IterableFactoryIO.filter_io(items)))
        )
        return PureIter(draft)

    @classmethod
    def until_empty(cls, items: PureIter[IO[Maybe[_I]]]) -> PureIter[IO[_I]]:
        def _to_opt(item: IO[Maybe[_I]]) -> IO[Optional[_I]]:
            return item.map(lambda i: i.value_or(None))

        opt: PureIter[IO[Optional[_I]]] = PureIterFactory.map(_to_opt, items)
        return cls.until_none(opt)
