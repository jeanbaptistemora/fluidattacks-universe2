from purity.v2.frozen import (
    FrozenList,
)
from purity.v2.pure_iter.core import (
    PureIter,
)
from typing import (
    TypeVar,
)

_T = TypeVar("_T")


def to_tuple(piter: PureIter[_T], limit: int) -> FrozenList[_T]:
    n_items = 0
    items = []
    for i in piter:
        n_items += 1
        items.append(i)
        if n_items >= limit:
            break
    return tuple(items)


def assert_immutability(piter: PureIter[_T], only_count: bool = False) -> None:
    # for finite PureIter
    if only_count:
        assert sum(1 for _ in piter) == sum(1 for _ in piter)
    else:
        assert tuple(piter) == tuple(piter)


def assert_immutability_inf(piter: PureIter[_T]) -> None:
    # for infinite PureIter
    assert to_tuple(piter, 10) == to_tuple(piter, 10)
