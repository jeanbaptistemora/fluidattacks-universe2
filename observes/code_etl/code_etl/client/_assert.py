# pylint: skip-file

from purity.v1 import (
    FrozenList,
)
from returns.result import (
    Failure,
    Result,
    Success,
)
from typing import (
    Any,
    Optional,
    Type,
    TypeVar,
)

_T = TypeVar("_T")


def assert_type(raw: Any, _type: Type[_T]) -> Result[_T, TypeError]:
    if isinstance(raw, _type):
        return Success(raw)
    return Failure(TypeError(f"Not a {_type} obj"))


def assert_not_none(obj: Optional[_T]) -> Result[_T, TypeError]:
    if obj is not None:
        return Success(obj)
    return Failure(TypeError(f"Expected not None obj"))


def assert_key(raw: FrozenList[Any], key: int) -> Result[Any, KeyError]:
    try:
        return Success(raw[key])
    except KeyError as err:
        return Failure(err)
