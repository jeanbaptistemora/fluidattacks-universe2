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
from returns.io import (
    IO,
)
from typing import (
    Callable,
    Iterable,
    Iterator,
    List,
    TypeVar,
    Union,
)

_T = TypeVar("_T")
_I = TypeVar("_I")
_R = TypeVar("_R")


def iter_obj(iterable: Iterable[_T]) -> IO[Iterator[_T]]:
    return IO(iter(iterable))


def unsafe_from_iterable(iterable: Iterable[_T]) -> PureIter[_T]:
    # This is an unsafe constructor do not use until is strictly necessary
    # iterable MUST be an IMMUTABLE object e.g. a tuple
    draft: _PureIter[_T] = _PureIter(Patch(lambda: IO(iterable)))
    return PureIter(draft)


def unsafe_from_generator(
    generator: Callable[[], IO[Iterable[_T]]]
) -> PureIter[_T]:
    # This is an unsafe constructor do not use until is strictly necessary
    # generator MUST return a new different object in each call
    draft: _PureIter[_T] = _PureIter(Patch(generator))
    return PureIter(draft)


def from_flist(items: FrozenList[_T]) -> PureIter[_T]:
    return unsafe_from_iterable(items)


def from_list(items: Union[List[_T], FrozenList[_T]]) -> PureIter[_T]:
    _items = tuple(items) if isinstance(items, list) else items
    return from_flist(_items)


def from_range(range_obj: range) -> PureIter[int]:
    return unsafe_from_generator(lambda: iter_obj(range_obj))


def infinite_range(start: int, step: int) -> PureIter[int]:
    return unsafe_from_generator(lambda: iter_obj(count(start, step)))


def pure_map(
    function: Callable[[_I], _R], items: Union[List[_I], FrozenList[_I]]
) -> PureIter[_R]:
    return from_list(items).map(function)
