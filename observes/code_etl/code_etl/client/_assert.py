# pylint: skip-file

from purity.v1 import (
    FrozenList,
)
from returns.result import (
    Failure,
    ResultE,
    Success,
)
from typing import (
    Any,
    Optional,
    Type,
    TypeVar,
)

_T = TypeVar("_T")


def assert_type(raw: Any, _type: Type[_T]) -> ResultE[_T]:
    if isinstance(raw, _type):
        return Success(raw)
    return Failure(TypeError(f"Not a {_type} obj"))


def assert_opt_type(raw: Any, _type: Type[_T]) -> ResultE[Optional[_T]]:
    if raw is None:
        return Success(raw)
    return assert_type(raw, _type)


def assert_not_none(obj: Optional[_T]) -> ResultE[_T]:
    if obj is not None:
        return Success(obj)
    return Failure(TypeError(f"Expected not None obj"))


def assert_key(raw: FrozenList[Any], key: int) -> ResultE[Any]:
    try:
        return Success(raw[key])
    except KeyError as err:
        return Failure(err)
    except IndexError as i_err:
        return Failure(i_err)
