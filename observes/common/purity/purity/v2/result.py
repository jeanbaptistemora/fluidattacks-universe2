from __future__ import (
    annotations,
)

from dataclasses import (
    dataclass,
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

_S = TypeVar("_S")
_F = TypeVar("_F")
_T = TypeVar("_T")


@dataclass(frozen=True)
class UnwrapError(Exception, Generic[_S, _F]):
    container: "Result[_S, _F]"


@dataclass(frozen=True)
class _Success(Generic[_T]):
    value: _T


@dataclass(frozen=True)
class _Failure(Generic[_T]):
    value: _T


@dataclass(frozen=True)
class Result(Generic[_S, _F]):
    _value: Union[_Success[_S], _Failure[_F]]

    @staticmethod
    def success(val: _S, _type: Optional[Type[_F]] = None) -> Result[_S, _F]:
        return Result(_Success(val))

    @staticmethod
    def failure(val: _F, _type: Optional[Type[_S]] = None) -> Result[_S, _F]:
        return Result(_Failure(val))

    def map(self, function: Callable[[_S], _T]) -> Result[_T, _F]:
        if isinstance(self._value, _Success):
            return Result(_Success(function(self._value.value)))
        return Result(self._value)

    def alt(self, function: Callable[[_F], _T]) -> Result[_S, _T]:
        if isinstance(self._value, _Failure):
            return Result(_Failure(function(self._value.value)))
        return Result(self._value)

    def bind(self, function: Callable[[_S], Result[_T, _F]]) -> Result[_T, _F]:
        if isinstance(self._value, _Success):
            return function(self._value.value)
        return Result(self._value)

    def lash(self, function: Callable[[_F], Result[_S, _T]]) -> Result[_S, _T]:
        if isinstance(self._value, _Failure):
            return function(self._value.value)
        return Result(self._value)

    def swap(self) -> Result[_F, _S]:
        if isinstance(self._value, _Failure):
            return Result(_Success(self._value.value))
        return Result(_Failure(self._value.value))

    def apply(self, wrapped: Result[Callable[[_S], _T], _F]) -> Result[_T, _F]:
        return wrapped.bind(lambda f: self.map(f))

    def value_or(self, default: _T) -> Union[_S, _T]:
        if isinstance(self._value, _Success):
            return self._value.value
        return default

    def or_else_call(self, function: Callable[[], _T]) -> Union[_S, _T]:
        # lazy version of `value_or`
        if isinstance(self._value, _Success):
            return self._value.value
        return function()

    def to_union(self) -> Union[_S, _F]:
        return self._value.value

    def unwrap(self) -> Union[_S, NoReturn]:
        if isinstance(self._value, _Success):
            return self._value.value
        raise UnwrapError(self)

    def unwrap_fail(self) -> Union[_F, NoReturn]:
        if isinstance(self._value, _Failure):
            return self._value.value
        raise UnwrapError(self)


ResultE = Result[_T, Exception]
