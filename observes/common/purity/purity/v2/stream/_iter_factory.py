# Iterable transforms
# should always return a new instance because Iterables are mutable
# result should be wrapped in a Cmd

from collections import (
    deque as deque_iter,
)
import more_itertools
from purity.v2.cmd import (
    Cmd,
    unsafe_unwrap,
)
from purity.v2.frozen import (
    FrozenList,
)
from typing import (
    Iterable,
    Optional,
    TypeVar,
)

_T = TypeVar("_T")


def chunked(items: Iterable[_T], size: int) -> Iterable[FrozenList[_T]]:
    return map(lambda l: tuple(l), more_itertools.chunked(items, size))


def deque(items: Iterable[_T]) -> None:
    deque_iter(items, maxlen=0)


def filter_none(items: Iterable[Optional[_T]]) -> Iterable[_T]:
    return (i for i in items if i is not None)


def squash(items: Iterable[Cmd[_T]]) -> Iterable[_T]:
    for item in items:
        yield unsafe_unwrap(item)


def until_none(items: Iterable[Optional[_T]]) -> Iterable[_T]:
    for item in items:
        if item is None:
            break
        yield item
