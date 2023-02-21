from typing import (
    TypeVar,
)

_L = TypeVar("_L")
_R = TypeVar("_R")


def inr(val: _R, _left: type[_L] | None = None) -> _L | _R:
    return val


def inl(val: _L, _right: type[_L] | None = None) -> _L | _R:
    return val
