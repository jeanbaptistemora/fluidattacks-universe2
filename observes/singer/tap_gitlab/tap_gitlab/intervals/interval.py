from __future__ import (
    annotations,
)

from datetime import (
    datetime,
)
from returns.primitives.container import (
    BaseContainer,
)
from returns.primitives.hkt import (
    SupportsKind1,
)
from returns.primitives.types import (
    Immutable,
)
from typing import (
    Any,
    Callable,
    cast,
    final,
    Optional,
    Type,
    TypeVar,
    Union,
)


class MIN(Immutable):
    def __new__(cls) -> MIN:
        return object.__new__(cls)

    def __str__(self) -> str:
        return "MIN"


class MAX(Immutable):
    def __new__(cls) -> MAX:
        return object.__new__(cls)

    def __str__(self) -> str:
        return "MAX"


class InvalidInterval(Exception):
    pass


_Point = TypeVar("_Point")
IntervalPoint = Union[_Point, MIN, MAX]


def default_greater(
    _type: Type[_Point],
) -> Callable[[_Point, _Point], bool]:
    if issubclass(_type, int):

        def greater_int(_x: _Point, _y: _Point) -> bool:
            return cast(int, _x) > cast(int, _y)

        return greater_int
    if issubclass(_type, datetime):

        def greater_dt(_x: _Point, _y: _Point) -> bool:
            return cast(datetime, _x) > cast(datetime, _y)

        return greater_dt
    raise NotImplementedError(f"No default greater for type {_type}")


def build_greater(
    greater: Callable[[_Point, _Point], bool]
) -> Callable[[IntervalPoint[_Point], IntervalPoint[_Point]], bool]:
    def _greater(_x: IntervalPoint[_Point], _y: IntervalPoint[_Point]) -> bool:
        if _x == _y:
            return False
        if isinstance(_x, MIN) or isinstance(_y, MAX):
            return False
        if isinstance(_x, MAX) or isinstance(_y, MIN):
            return True
        return greater(_x, _y)

    return _greater


def _common_builder(
    _type: Type[_Point],
    lower: Union[_Point, MIN],
    upper: Union[_Point, MAX],
    greater_than: Optional[Callable[[_Point, _Point], bool]],
) -> Any:
    _greater_than: Callable[
        [IntervalPoint[_Point], IntervalPoint[_Point]], bool
    ] = build_greater(greater_than if greater_than else default_greater(_type))
    if not isinstance(lower, MIN) and not isinstance(upper, MAX):
        if _greater_than(lower, upper):
            raise InvalidInterval()
    return {
        "lower": lower,
        "upper": upper,
        "greater": _greater_than,
    }


@final
class ClosedInterval(
    BaseContainer,
    SupportsKind1["ClosedInterval", _Point],
):
    def __init__(
        self,
        lower: _Point,
        upper: _Point,
        greater_than: Optional[Callable[[_Point, _Point], bool]] = None,
    ) -> None:
        super().__init__(
            _common_builder(type(lower), lower, upper, greater_than)
        )

    @property
    def lower(self) -> _Point:
        return self._inner_value["lower"]

    @property
    def upper(self) -> _Point:
        return self._inner_value["upper"]


@final
class OpenInterval(
    BaseContainer,
    SupportsKind1["OpenInterval", _Point],
):
    def __init__(
        self,
        _type: Type[_Point],
        lower: Union[_Point, MIN],
        upper: Union[_Point, MAX],
        greater_than: Optional[Callable[[_Point, _Point], bool]] = None,
    ) -> None:
        super().__init__(_common_builder(_type, lower, upper, greater_than))

    @property
    def lower(self) -> Union[_Point, MIN]:
        return self._inner_value["lower"]

    @property
    def upper(self) -> Union[_Point, MAX]:
        return self._inner_value["upper"]


@final
class OpenLeftInterval(
    BaseContainer,
    SupportsKind1["OpenLeftInterval", _Point],
):
    def __init__(
        self,
        lower: Union[_Point, MIN],
        upper: _Point,
        greater_than: Optional[Callable[[_Point, _Point], bool]] = None,
    ) -> None:
        super().__init__(
            _common_builder(type(upper), lower, upper, greater_than)
        )

    @property
    def lower(self) -> Union[_Point, MIN]:
        return self._inner_value["lower"]

    @property
    def upper(self) -> _Point:
        return self._inner_value["upper"]


@final
class OpenRightInterval(
    BaseContainer,
    SupportsKind1["OpenRightInterval", _Point],
):
    def __init__(
        self,
        lower: _Point,
        upper: Union[_Point, MAX],
        greater_than: Optional[Callable[[_Point, _Point], bool]] = None,
    ) -> None:
        super().__init__(
            _common_builder(type(lower), lower, upper, greater_than)
        )

    @property
    def lower(self) -> _Point:
        return self._inner_value["lower"]

    @property
    def upper(self) -> Union[_Point, MAX]:
        return self._inner_value["upper"]


Interval = Union[
    ClosedInterval[_Point],
    OpenInterval[_Point],
    OpenLeftInterval[_Point],
    OpenRightInterval[_Point],
]
