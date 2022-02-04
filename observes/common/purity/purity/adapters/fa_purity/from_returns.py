from dataclasses import (
    dataclass,
)
from fa_purity.cmd import (
    Cmd,
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
    Result as LegacyResult,
)
from returns.unsafe import (
    unsafe_perform_io,
)
from typing import (
    Callable,
    overload,
    TypeVar,
    Union,
)

_S = TypeVar("_S")
_F = TypeVar("_F")
_T = TypeVar("_T")


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


def to_cmd(action: Callable[[], IO[_T]]) -> Cmd[_T]:
    return Cmd.from_cmd(lambda: unsafe_perform_io(action()))
