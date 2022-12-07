from fa_purity.frozen import (
    FrozenList,
)
from fa_purity.result import (
    Result,
    ResultE,
    ResultFactory,
)
from typing import (
    Optional,
    Type,
    TypeVar,
)

_T = TypeVar("_T")
_A = TypeVar("_A")


def assert_type(raw: _A, _type: Type[_T]) -> ResultE[_T]:
    factory: ResultFactory[_T, Exception] = ResultFactory()
    if isinstance(raw, _type):
        return factory.success(raw)
    return factory.failure(TypeError(f"Not a {_type} obj"))


def assert_opt_type(
    raw: Optional[_A], _type: Type[_T]
) -> ResultE[Optional[_T]]:
    factory: ResultFactory[Optional[_T], Exception] = ResultFactory()
    if raw is None:
        return factory.success(raw)
    return assert_type(raw, _type).bind(factory.success)


def assert_not_none(obj: Optional[_T]) -> ResultE[_T]:
    factory: ResultFactory[_T, Exception] = ResultFactory()
    if obj is not None:
        return factory.success(obj)
    return factory.failure(TypeError("Expected not None obj"))


def assert_key(raw: FrozenList[_T], key: int) -> ResultE[_T]:
    factory: ResultFactory[_T, Exception] = ResultFactory()
    try:
        return factory.success(raw[key])
    except KeyError as err:
        return factory.failure(err)
    except IndexError as i_err:
        return factory.failure(i_err)
