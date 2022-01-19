from __future__ import (
    annotations,
)

from dataclasses import (
    dataclass,
)
from purity.v2.result import (
    Result,
)
from typing import (
    Callable,
    Generic,
    NoReturn,
    Optional,
    Type,
    TypeVar,
    Union,
)

_A = TypeVar("_A")
_B = TypeVar("_B")


@dataclass(frozen=True)
class Maybe(Generic[_A]):
    _value: Result[_A, None]

    @staticmethod
    def from_optional(value: Optional[_A]) -> Maybe[_A]:
        if value is None:
            return Maybe(Result.failure(value))
        return Maybe(Result.success(value))

    @staticmethod
    def from_result(result: Result[_A, None]) -> Maybe[_A]:
        return Maybe(result)

    @staticmethod
    def empty(_type: Type[_A]) -> Maybe[_A]:
        return Maybe.from_optional(None)

    def to_result(self) -> Result[_A, None]:
        return self._value

    def map(self, function: Callable[[_A], _B]) -> Maybe[_B]:
        return Maybe(self._value.map(function))

    def bind(self, function: Callable[[_A], Maybe[_B]]) -> Maybe[_B]:
        return Maybe(self._value.bind(lambda a: function(a).to_result()))

    def bind_optional(
        self, function: Callable[[_A], Optional[_B]]
    ) -> Maybe[_B]:
        return self.bind(lambda a: Maybe.from_optional(function(a)))

    def lash(self, function: Callable[[], Maybe[_A]]) -> Maybe[_A]:
        return Maybe(self._value.lash(lambda _: function().to_result()))

    def unwrap(self) -> Union[_A, NoReturn]:
        return self._value.unwrap()

    def failure(self) -> Union[None, NoReturn]:
        return self._value.unwrap_fail()

    def value_or(self, default: _B) -> Union[_A, _B]:
        return self._value.value_or(default)

    def or_else_call(self, function: Callable[[], _B]) -> Union[_A, _B]:
        return self._value.or_else_call(function)
