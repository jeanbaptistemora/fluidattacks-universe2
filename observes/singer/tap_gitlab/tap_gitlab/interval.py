from enum import (
    Enum,
)
from returns.primitives.container import (
    BaseContainer,
)
from returns.primitives.hkt import (
    SupportsKind1,
    SupportsKind2,
)
from typing import (
    final,
    Literal,
    Tuple,
    TypeVar,
)


class IntervalType(Enum):
    CLOSED = "CLOSED"
    OPEN = "OPEN"
    OPEN_LEFT = "OPEN_LEFT"
    OPEN_RIGHT = "OPEN_RIGHT"


_IType = TypeVar(
    "_IType",
    Literal[IntervalType.CLOSED],
    Literal[IntervalType.OPEN],
    Literal[IntervalType.OPEN_LEFT],
    Literal[IntervalType.OPEN_RIGHT],
)
_Point = TypeVar("_Point")


@final
class Interval(
    BaseContainer,
    SupportsKind2["Interval", _IType, _Point],
):
    def __init__(
        self,
        _itype: _IType,
        lower: _Point,
        upper: _Point,
    ) -> None:
        super().__init__(
            {
                "lower": lower,
                "upper": upper,
            }
        )

    @property
    def lower(self) -> _Point:
        return self._inner_value["lower"]

    @property
    def upper(self) -> _Point:
        return self._inner_value["upper"]


ClosedInterval = Interval[Literal[IntervalType.CLOSED], _Point]
OpenInterval = Interval[Literal[IntervalType.OPEN], _Point]
OpenLeftInterval = Interval[Literal[IntervalType.OPEN_LEFT], _Point]
OpenRightInterval = Interval[Literal[IntervalType.OPEN_RIGHT], _Point]


def closed_interval(lower: _Point, upper: _Point) -> ClosedInterval[_Point]:
    return Interval(IntervalType.CLOSED, lower, upper)


def open_interval(lower: _Point, upper: _Point) -> OpenInterval[_Point]:
    return Interval(IntervalType.OPEN, lower, upper)


def open_lf_interval(lower: _Point, upper: _Point) -> OpenLeftInterval[_Point]:
    return Interval(IntervalType.OPEN_LEFT, lower, upper)


def open_rt_interval(
    lower: _Point, upper: _Point
) -> OpenRightInterval[_Point]:
    return Interval(IntervalType.OPEN_RIGHT, lower, upper)


@final
class FragmentedInterval(
    BaseContainer,
    SupportsKind1["FragmentedInterval", _Point],
):
    def __init__(
        self,
        endpoints: Tuple[_Point, ...],
        emptiness: Tuple[bool, ...],
    ) -> None:
        super().__init__(
            {
                "endpoints": endpoints,
                "emptiness": emptiness,
            }
        )

    @property
    def endpoints(self) -> Tuple[_Point, ...]:
        return self._inner_value["endpoints"]

    @property
    def emptiness(self) -> Tuple[bool, ...]:
        return self._inner_value["emptiness"]
