from dataclasses import (
    dataclass,
)
from purity.v1 import (
    Patch,
)
from ratelimit import (
    limits as rate_limit,
    sleep_and_retry,
)
from returns.primitives.hkt import (
    SupportsKind2,
)
from typing import (
    Callable,
    NamedTuple,
    TypeVar,
)

_InputTVar = TypeVar("_InputTVar")
_ReturnTVar = TypeVar("_ReturnTVar")


class Limits(NamedTuple):
    max_calls: int
    max_period: float
    min_period: float


@dataclass(frozen=True)
class _LimitedFunction(
    SupportsKind2[
        "_LimitedFunction[_InputTVar, _ReturnTVar]", _InputTVar, _ReturnTVar
    ],
):
    _function: Patch[Callable[[_InputTVar], _ReturnTVar]]


@dataclass(frozen=True)
class LimitedFunction(
    _LimitedFunction[_InputTVar, _ReturnTVar],
):
    def __init__(self, obj: _LimitedFunction[_InputTVar, _ReturnTVar]) -> None:
        super().__init__(obj._function)

    def __call__(self, args: _InputTVar) -> _ReturnTVar:
        # reveal_type(self._function)
        return self._function.unwrap(args)


@dataclass(frozen=True)
class RateLimiter:
    @staticmethod
    def limit(
        function: Callable[[_InputTVar], _ReturnTVar], limits: Limits
    ) -> LimitedFunction[_InputTVar, _ReturnTVar]:
        @sleep_and_retry
        @rate_limit(calls=1, period=limits.min_period)  # anti burst limit
        @rate_limit(
            calls=limits.max_calls, period=limits.max_period
        )  # api limit
        def _wrapper(args: _InputTVar) -> _ReturnTVar:
            return function(args)

        return LimitedFunction(_LimitedFunction(Patch(_wrapper)))
