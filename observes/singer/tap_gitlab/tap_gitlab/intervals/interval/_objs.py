from dataclasses import (
    dataclass,
)
from returns.primitives.hkt import (
    SupportsKind1,
)
from tap_gitlab.intervals.patch import (
    Patch,
)
from typing import (
    Any,
    Callable,
    TypeVar,
    Union,
)


@dataclass(frozen=True)
class MIN:
    def __str__(self) -> str:
        return "MIN"


@dataclass(frozen=True)
class MAX:
    def __str__(self) -> str:
        return "MAX"


class InvalidInterval(Exception):
    pass


_Point = TypeVar("_Point")
PointType = TypeVar("PointType")
IntervalPoint = Union[PointType, MIN, MAX]
Comparison = Callable[[PointType, PointType], bool]


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
        "greater": Patch(greater_than),
    }


def _contains_point(
    greater: Comparison[IntervalPoint[_Point]],
    lower: IntervalPoint[_Point],
    upper: IntervalPoint[_Point],
    point: IntervalPoint[_Point],
) -> bool:
    return (greater(point, lower) or point == lower) and (
        greater(upper, point) or point == upper
    )


@dataclass(frozen=True)
class ClosedInterval(
    SupportsKind1["ClosedInterval", _Point],
):
    greater: Patch[Comparison[IntervalPoint[_Point]]]
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

    def __contains__(self, point: IntervalPoint[_Point]) -> bool:
        return _contains_point(
            self.greater.unwrap, self.lower, self.upper, point
        )


@dataclass(frozen=True)
class OpenInterval(
    SupportsKind1["OpenInterval", _Point],
):
    greater: Patch[Comparison[IntervalPoint[_Point]]]
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

    def __contains__(self, point: IntervalPoint[_Point]) -> bool:
        return _contains_point(
            self.greater.unwrap, self.lower, self.upper, point
        )


@dataclass(frozen=True)
class OpenLeftInterval(
    SupportsKind1["OpenLeftInterval", _Point],
):
    greater: Patch[Comparison[IntervalPoint[_Point]]]
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

    def __contains__(self, point: IntervalPoint[_Point]) -> bool:
        return _contains_point(
            self.greater.unwrap, self.lower, self.upper, point
        )


@dataclass(frozen=True)
class OpenRightInterval(
    SupportsKind1["OpenRightInterval", _Point],
):
    greater: Patch[Comparison[IntervalPoint[_Point]]]
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

    def __contains__(self, point: IntervalPoint[_Point]) -> bool:
        return _contains_point(
            self.greater.unwrap, self.lower, self.upper, point
        )


Interval = Union[
    ClosedInterval[PointType],
    OpenInterval[PointType],
    OpenLeftInterval[PointType],
    OpenRightInterval[PointType],
]
