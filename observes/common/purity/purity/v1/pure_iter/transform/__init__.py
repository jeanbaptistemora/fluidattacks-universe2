from purity.v2.pure_iter.core import (
    PureIter,
)
from purity.v2.pure_iter.transform import (
    chain,
    filter_opt,
    until_none,
)
from returns.maybe import (
    Maybe,
)
from typing import (
    Optional,
    TypeVar,
)

_I = TypeVar("_I")


def filter_maybe(items: PureIter[Maybe[_I]]) -> PureIter[_I]:
    return filter_opt(items.map(lambda x: x.value_or(None)))


def until_empty(items: PureIter[Maybe[_I]]) -> PureIter[_I]:
    def _to_opt(item: Maybe[_I]) -> Optional[_I]:
        return item.value_or(None)

    opt: PureIter[Optional[_I]] = items.map(_to_opt)
    return until_none(opt)


__all__ = [
    "chain",
    "filter_opt",
    "until_none",
]
