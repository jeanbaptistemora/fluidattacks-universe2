from fa_purity.frozen import (
    FrozenList,
)
from fa_purity.result import (
    Result,
    ResultE,
)
from typing import (
    Optional,
    Type,
    TypeVar,
)

_T = TypeVar("_T")
_A = TypeVar("_A")


def assert_type(raw: _A, _type: Type[_T]) -> ResultE[_T]:
    if isinstance(raw, _type):
        return Result.success(raw)
    return Result.failure(TypeError(f"Not a {_type} obj"))


def assert_opt_type(
    raw: Optional[_A], _type: Type[_T]
) -> ResultE[Optional[_T]]:
    if raw is None:
        return Result.success(raw)
    return assert_type(raw, _type)


def assert_not_none(obj: Optional[_T]) -> ResultE[_T]:
    if obj is not None:
        return Result.success(obj)
    return Result.failure(TypeError("Expected not None obj"))


def assert_key(raw: FrozenList[_T], key: int) -> ResultE[_T]:
    try:
        return Result.success(raw[key])
    except KeyError as err:
        return Result.failure(err)
    except IndexError as i_err:
        return Result.failure(i_err)
