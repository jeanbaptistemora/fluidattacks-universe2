from __future__ import (
    annotations,
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
from purity.v1.pure_iter._obj import (
    _PureIter,
    PureIter,
)
from typing import (
    TypeVar,
)

_T = TypeVar("_T")


def from_flist(items: FrozenList[_T]) -> PureIter[_T]:
    draft = _PureIter(Patch(lambda: items))
    return PureIter(draft)


def from_range(range_obj: range) -> PureIter[int]:
    draft = _PureIter(Patch(lambda: iter(range_obj)))
    return PureIter(draft)


def infinite_range(start: int, step: int) -> PureIter[int]:
    draft = _PureIter(Patch(lambda: count(start, step)))
    return PureIter(draft)
