from __future__ import (
    annotations,
)

from dataclasses import (
    dataclass,
)
from purity.v2._patch import (
    Patch,
)
import sys
from typing import (
    Callable,
    Generic,
    NoReturn,
    TypeVar,
)

_A = TypeVar("_A")
_B = TypeVar("_B")


@dataclass(frozen=True)
class Cmd(Generic[_A]):
    # Equivalent to haskell IO type
    _value: Patch[Callable[[], _A]]

    @staticmethod
    def from_cmd(value: Callable[[], _A]) -> Cmd[_A]:
        return Cmd(Patch(value))

    def map(self, function: Callable[[_A], _B]) -> Cmd[_B]:
        return Cmd(Patch(lambda: function(self._value.unwrap())))

    def bind(self, function: Callable[[_A], Cmd[_B]]) -> Cmd[_B]:
        return function(self._value.unwrap())

    def apply(self, wrapped: Cmd[Callable[[_A], _B]]) -> Cmd[_B]:
        return wrapped.map(lambda f: f(self._value.unwrap()))

    def compute(self) -> NoReturn:
        self._value.unwrap()
        sys.exit(0)


def unsafe_unwrap(action: Cmd[_A]) -> _A:
    # This is an unsafe constructor (type-check cannot ensure its proper use)
    # Do not use until is strictly necessary
    #
    # When all actions (Cmd[_A]) result in the same output instance (_A)
    # this unwrap can be used
    return action._value.unwrap()
