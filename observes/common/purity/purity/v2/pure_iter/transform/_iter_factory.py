# Iterable builders
# should always return a new instance because Iterables are mutable
from itertools import (
    chain,
)
from purity.v2.cmd import (
    Cmd,
    unsafe_unwrap,
)
from purity.v2.pure_iter.core import (
    PureIter,
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


class IterableFactoryCmd:
    @staticmethod
    def chain_io(
        unchained: PureIter[Cmd[PureIter[_I]]],
    ) -> Iterable[Cmd[_I]]:
        iters = (unsafe_unwrap(i) for i in iter(unchained))
        for a in chain.from_iterable(iters):
            yield Cmd.from_cmd(lambda: a)

    @staticmethod
    def until_none(items: PureIter[Cmd[Optional[_I]]]) -> Iterable[Cmd[_I]]:
        for item in items:
            _item = unsafe_unwrap(item)
            if _item is None:
                break
            not_none_item = _item
            yield Cmd.from_cmd(lambda: not_none_item)
