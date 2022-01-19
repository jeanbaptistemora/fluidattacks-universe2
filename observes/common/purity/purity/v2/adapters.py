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
