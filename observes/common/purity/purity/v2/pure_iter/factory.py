from __future__ import (
    annotations,
)

from itertools import (
    count,
)
from purity.v2.cmd import (
    Cmd,
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
    Iterable,
    List,
    TypeVar,
    Union,
)

_T = TypeVar("_T")
_I = TypeVar("_I")
_R = TypeVar("_R")


def unsafe_from_cmd(iterable: Cmd[Iterable[_T]]) -> PureIter[_T]:
    # This is an unsafe constructor (type-check cannot ensure its proper use)
    # Do not use until is strictly necessary
    # Cmd MUST produce an IMMUTABLE Iterable object i.e. tuple
    # or different/new MUTABLE Iterable objects that are equivalent i.e. map object
    #
    # Non compliant code:
    #   y = map(lambda i: i + 1, range(0, 10))
    #   x = unsafe_from_cmd(
    #       Cmd.from_cmd(lambda: y)
    #   )
    #   # y is a map obj instance; cmd lambda is pinned with a single ref
    #   # since map is MUTABLE the ref should change at every call
    #
    # Compliant code:
    #   x = unsafe_from_cmd(
    #       Cmd.from_cmd(
    #           lambda: map(lambda i: i + 1, range(0, 10))
    #       )
    #   )
    #   # cmd lambda produces a new ref in each call
    #   # but all of them are equivalent (created with the same builder with equal args)
    return PureIter(_PureIter(iterable))


def from_flist(items: FrozenList[_T]) -> PureIter[_T]:
    return unsafe_from_cmd(Cmd.from_cmd(lambda: items))


def from_list(items: Union[List[_T], FrozenList[_T]]) -> PureIter[_T]:
    _items = tuple(items) if isinstance(items, list) else items
    return from_flist(_items)


def from_range(range_obj: range) -> PureIter[int]:
    return unsafe_from_cmd(Cmd.from_cmd(lambda: range_obj))


def infinite_range(start: int, step: int) -> PureIter[int]:
    return unsafe_from_cmd(Cmd.from_cmd(lambda: count(start, step)))


def pure_map(
    function: Callable[[_I], _R], items: Union[List[_I], FrozenList[_I]]
) -> PureIter[_R]:
    return from_list(items).map(function)
