from __future__ import (
    annotations,
)

from dataclasses import (
    dataclass,
)
from enum import (
    Enum,
)
from typing import (
    Callable,
    Generic,
    Literal,
    overload,
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


class RTypes(Enum):
    SUCCESS = True
    FAILURE = False


@dataclass(frozen=True)
class Result(Generic[_S, _F]):
    _value: Union[_Success[_S], _Failure[_F]]

    @staticmethod
    def success(val: _S) -> Result[_S, _F]:
        return Result(_Success(val))

    @staticmethod
    def failure(val: _F) -> Result[_S, _F]:
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

    @overload
    def unwrap(self, r_type: Literal[RTypes.SUCCESS] = RTypes.SUCCESS) -> _S:
        pass

    @overload
    def unwrap(self, r_type: Literal[RTypes.FAILURE]) -> _F:
        pass

    def unwrap(self, r_type: RTypes = RTypes.SUCCESS) -> Union[_S, _F]:
        if r_type == RTypes.SUCCESS and isinstance(self._value, _Success):
            return self._value.value
        elif isinstance(self._value, _Failure):
            return self._value.value
        raise UnwrapError(self)


ResultE = Result[_T, Exception]
