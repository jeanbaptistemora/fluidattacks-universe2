# Iterable builders
# should always return a new instance because Iterables are mutable
from itertools import (
    chain,
)
from purity.v1.pure_iter._obj import (
    PureIter,
)
from returns.io import (
    IO,
)
from returns.unsafe import (
    unsafe_perform_io,
)
from typing import (
    Iterable,
    Optional,
    TypeVar,
)

_I = TypeVar("_I")


class IterableFactory:
    @staticmethod
    def chain(
        unchained: PureIter[PureIter[_I]],
    ) -> Iterable[_I]:
        return chain.from_iterable(unchained)

    @staticmethod
    def filter_none(items: PureIter[Optional[_I]]) -> Iterable[_I]:
        return (i for i in items if i is not None)

    @staticmethod
    def until_none(items: PureIter[Optional[_I]]) -> Iterable[_I]:
        for item in items:
            if item is None:
                break
            yield item


class IterableFactoryIO:
    @staticmethod
    def chain_io(
        unchained: PureIter[IO[PureIter[_I]]],
    ) -> Iterable[IO[_I]]:
        iters = (unsafe_perform_io(i) for i in iter(unchained))
        return map(IO, chain.from_iterable(iters))

    @staticmethod
    def filter_io(items: PureIter[IO[Optional[_I]]]) -> Iterable[IO[_I]]:
        for item in items:
            _item = unsafe_perform_io(item)
            if _item is None:
                break
            yield IO(_item)
