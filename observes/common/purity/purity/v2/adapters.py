from dataclasses import (
    dataclass,
)
from purity.v2.maybe import (
    Maybe,
)
from purity.v2.result import (
    Result,
)
from returns.maybe import (
    Maybe as LegacyMaybe,
)
from returns.result import (
    Failure,
    Result as LegacyResult,
    Success,
)
from typing import (
    Any,
    overload,
    TypeVar,
    Union,
)

_S = TypeVar("_S")
_F = TypeVar("_F")
_T = TypeVar("_T")


@overload
def to_returns(item: Maybe[_T]) -> LegacyMaybe[_T]:
    pass


@overload
def to_returns(item: Result[_S, _F]) -> LegacyResult[_S, _F]:
    pass


def to_returns(
    item: Union[Result[_S, _F], Maybe[_T]]
) -> Union[LegacyResult[_S, _F], LegacyMaybe[_T]]:
    if isinstance(item, Result):
        return (
            item.map(lambda x: Success(x))
            .lash(lambda x: Result.success(Failure(x)))
            .unwrap()
        )
    return LegacyMaybe.from_optional(item.value_or(None))


@dataclass(frozen=True)
class NoValue:
    pass


@overload
def from_returns(item: LegacyMaybe[_T]) -> Maybe[_T]:
    # overloaded signature 1
    pass


@overload
def from_returns(item: LegacyResult[_S, _F]) -> Result[_S, _F]:  # type: ignore
    # False positive due to env conf: Overloaded function signature 2 will never be matched
    pass


def from_returns(
    item: Union[LegacyResult[_S, _F], LegacyMaybe[_T]]
) -> Union[Result[_S, _F], Maybe[_T]]:
    if isinstance(item, LegacyResult):
        success = item.value_or(NoValue())
        fail = item.swap().value_or(NoValue())
        if not isinstance(success, NoValue):
            return Result.success(success)
        elif not isinstance(fail, NoValue):
            return Result.failure(fail)
        raise Exception("Unexpected Result with no value")
    val = item.value_or(None)
    return Maybe.from_optional(val)
