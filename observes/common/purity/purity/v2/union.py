from typing import (
    Type,
    TypeVar,
    Union,
)

_L = TypeVar("_L")
_R = TypeVar("_R")


def inr(_left: Type[_L], val: _R) -> Union[_L, _R]:
    return val


def inl(_right: Type[_R], val: _L) -> Union[_L, _R]:
    return val
