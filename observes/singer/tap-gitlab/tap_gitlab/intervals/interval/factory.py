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
from tap_gitlab.intervals.interval._objs import (
    ClosedInterval,
    Comparison,
    IntervalPoint,
    MAX,
    MIN,
    OpenInterval,
    OpenLeftInterval,
    OpenRightInterval,
)
from tap_gitlab.intervals.patch import (
    Patch,
)
from typing import (
    cast,
    Type,
    TypeVar,
    Union,
)

PointType = TypeVar("PointType")


def _default_greater(
    _type: Type[PointType],
) -> Comparison[PointType]:
    if issubclass(_type, int):

        def greater_int(_x: PointType, _y: PointType) -> bool:
            return cast(int, _x) > cast(int, _y)

        return greater_int
    if issubclass(_type, datetime):

        def greater_dt(_x: PointType, _y: PointType) -> bool:
            return cast(datetime, _x) > cast(datetime, _y)

        return greater_dt
    raise NotImplementedError(f"No default greater for type {_type}")


def _build_greater(
    greater: Comparison[PointType],
) -> Comparison[IntervalPoint[PointType]]:
    def _greater(
        _x: IntervalPoint[PointType], _y: IntervalPoint[PointType]
    ) -> bool:
        if _x == _y:
            return False
        if isinstance(_x, MIN) or isinstance(_y, MAX):
            return False
        if isinstance(_x, MAX) or isinstance(_y, MIN):
            return True
        return greater(_x, _y)

    return _greater


@dataclass(frozen=True)
class IntervalFactory(
    SupportsKind1["IntervalFactory", PointType],
):
    greater: Patch[Comparison[IntervalPoint[PointType]]]

    def __init__(
        self,
        greater_than: Comparison[PointType],
    ) -> None:
        object.__setattr__(
            self, "greater", Patch(_build_greater(greater_than))
        )

    @classmethod
    def from_default(
        cls, data_type: Type[PointType]
    ) -> IntervalFactory[PointType]:
        return IntervalFactory(_default_greater(data_type))

    def new_closed(
        self, lower: PointType, upper: PointType
    ) -> ClosedInterval[PointType]:
        return ClosedInterval(self.greater.unwrap, lower, upper)

    def new_open(
        self, lower: Union[PointType, MIN], upper: Union[PointType, MAX]
    ) -> OpenInterval[PointType]:
        return OpenInterval(self.greater.unwrap, lower, upper)

    def new_ropen(
        self, lower: PointType, upper: Union[PointType, MAX]
    ) -> OpenRightInterval[PointType]:
        return OpenRightInterval(self.greater.unwrap, lower, upper)

    def new_lopen(
        self, lower: Union[PointType, MIN], upper: PointType
    ) -> OpenLeftInterval[PointType]:
        return OpenLeftInterval(self.greater.unwrap, lower, upper)
