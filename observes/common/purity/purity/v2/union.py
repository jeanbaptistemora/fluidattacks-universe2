from typing import (
    Optional,
    Type,
    TypeVar,
    Union,
)

_L = TypeVar("_L")
_R = TypeVar("_R")


def inr(val: _R, _left: Optional[Type[_L]] = None) -> Union[_L, _R]:
    return val


def inl(val: _L, _right: Optional[Type[_L]] = None) -> Union[_L, _R]:
    return val
