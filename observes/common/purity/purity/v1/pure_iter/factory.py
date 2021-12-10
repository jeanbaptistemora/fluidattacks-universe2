from __future__ import (
    annotations,
)

from itertools import (
    count,
)
from purity.v2._patch import (
    Patch,
)
from purity.v2.frozen import (
    FrozenList,
)
from purity.v2.pure_iter.core import (
    _PureIter,
    PureIter,
)
from typing import (
    Callable,
    List,
    TypeVar,
    Union,
)

_T = TypeVar("_T")
_I = TypeVar("_I")
_R = TypeVar("_R")


def from_flist(items: FrozenList[_T]) -> PureIter[_T]:
    draft = _PureIter(Patch(lambda: items))
    return PureIter(draft)


def from_list(items: Union[List[_T], FrozenList[_T]]) -> PureIter[_T]:
    draft = _PureIter(Patch(lambda: tuple(items)))
    return PureIter(draft)


def from_range(range_obj: range) -> PureIter[int]:
    draft = _PureIter(Patch(lambda: iter(range_obj)))
    return PureIter(draft)


def infinite_range(start: int, step: int) -> PureIter[int]:
    draft = _PureIter(Patch(lambda: count(start, step)))
    return PureIter(draft)


def pure_map(
    function: Callable[[_I], _R], items: Union[List[_I], FrozenList[_I]]
) -> PureIter[_R]:
    return from_list(items).map(function)
