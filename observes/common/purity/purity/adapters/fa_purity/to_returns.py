from fa_purity.cmd import (
    Cmd,
    unsafe_unwrap,
)
from fa_purity.maybe import (
    Maybe,
)
from fa_purity.result import (
    Result,
)
from returns.io import (
    IO,
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
    overload,
    TypeVar,
    Union,
)

_T = TypeVar("_T")
_S = TypeVar("_S")
_F = TypeVar("_F")


@overload
def to_returns(item: Maybe[_T]) -> LegacyMaybe[_T]:
    # overloaded signature 1
    pass


@overload
def to_returns(item: Result[_S, _F]) -> LegacyResult[_S, _F]:
    # overloaded signature 2
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


def unsafe_to_io(action: Cmd[_T]) -> IO[_T]:
    return IO(unsafe_unwrap(action))
