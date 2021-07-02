from __future__ import (
    annotations,
)

from dataclasses import (
    dataclass,
)
from datetime import (
    datetime,
)
from returns.primitives.hkt import (
    SupportsKind1,
)
from returns.primitives.types import (
    Immutable,
)
from tap_gitlab.intervals.patch import (
    Patch,
)
from typing import (
    Any,
    Callable,
    cast,
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
Comparison = Callable[[_Point, _Point], bool]


def default_greater(
    _type: Type[_Point],
) -> Comparison[_Point]:
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
    greater: Comparison[_Point],
) -> Comparison[IntervalPoint[_Point]]:
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
    lower: IntervalPoint[_Point],
    upper: IntervalPoint[_Point],
    greater_than: Comparison[IntervalPoint[_Point]],
) -> Any:
    if not greater_than(upper, lower):
        raise InvalidInterval()
    return {
        "lower": lower,
        "upper": upper,
        "greater": greater_than,
    }


@dataclass
class ClosedInterval(
    Immutable,
    SupportsKind1["ClosedInterval", _Point],
):
    greater: Comparison[IntervalPoint[_Point]]
    lower: _Point
    upper: _Point

    def __init__(
        self,
        greater_than: Comparison[IntervalPoint[_Point]],
        lower: _Point,
        upper: _Point,
    ) -> None:
        raw = _common_builder(lower, upper, greater_than)
        for key, value in raw.items():
            object.__setattr__(self, key, value)


@dataclass
class OpenInterval(
    Immutable,
    SupportsKind1["OpenInterval", _Point],
):
    greater: Comparison[IntervalPoint[_Point]]
    lower: Union[_Point, MIN]
    upper: Union[_Point, MAX]

    def __init__(
        self,
        greater_than: Comparison[IntervalPoint[_Point]],
        lower: Union[_Point, MIN],
        upper: Union[_Point, MAX],
    ) -> None:
        raw = _common_builder(lower, upper, greater_than)
        for key, value in raw.items():
            object.__setattr__(self, key, value)


@dataclass
class OpenLeftInterval(
    Immutable,
    SupportsKind1["OpenLeftInterval", _Point],
):
    greater: Comparison[IntervalPoint[_Point]]
    lower: Union[_Point, MIN]
    upper: _Point

    def __init__(
        self,
        greater_than: Comparison[IntervalPoint[_Point]],
        lower: Union[_Point, MIN],
        upper: _Point,
    ) -> None:
        raw = _common_builder(lower, upper, greater_than)
        for key, value in raw.items():
            object.__setattr__(self, key, value)


@dataclass
class OpenRightInterval(
    Immutable,
    SupportsKind1["OpenRightInterval", _Point],
):
    greater: Comparison[IntervalPoint[_Point]]
    lower: _Point
    upper: Union[_Point, MAX]

    def __init__(
        self,
        greater_than: Comparison[IntervalPoint[_Point]],
        lower: _Point,
        upper: Union[_Point, MAX],
    ) -> None:
        raw = _common_builder(lower, upper, greater_than)
        for key, value in raw.items():
            object.__setattr__(self, key, value)


Interval = Union[
    ClosedInterval[_Point],
    OpenInterval[_Point],
    OpenLeftInterval[_Point],
    OpenRightInterval[_Point],
]


@dataclass
class IntervalFactory(
    Immutable,
    SupportsKind1["IntervalFactory", _Point],
):
    _type: Type[_Point]
    greater: Patch[Comparison[IntervalPoint[_Point]]]

    def __init__(
        self,
        _type: Type[_Point],
        greater_than: Optional[Comparison[_Point]] = None,
    ) -> None:
        _greater_than: Comparison[IntervalPoint[_Point]] = build_greater(
            greater_than if greater_than else default_greater(_type)
        )
        object.__setattr__(self, "_type", _type)
        object.__setattr__(self, "greater", Patch(_greater_than))

    def new_closed(
        self, lower: _Point, upper: _Point
    ) -> ClosedInterval[_Point]:
        return ClosedInterval(self.greater.unwrap, lower, upper)

    def new_open(
        self, lower: Union[_Point, MIN], upper: Union[_Point, MAX]
    ) -> OpenInterval[_Point]:
        return OpenInterval(self.greater.unwrap, lower, upper)

    def new_ropen(
        self, lower: _Point, upper: Union[_Point, MAX]
    ) -> OpenRightInterval[_Point]:
        return OpenRightInterval(self.greater.unwrap, lower, upper)

    def new_lopen(
        self, lower: Union[_Point, MIN], upper: _Point
    ) -> OpenLeftInterval[_Point]:
        return OpenLeftInterval(self.greater.unwrap, lower, upper)
