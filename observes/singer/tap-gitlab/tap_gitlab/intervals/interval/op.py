from tap_gitlab.intervals.interval._objs import (
    Interval,
)
from typing import (
    TypeVar,
)

PointType = TypeVar("PointType")


def are_disjoin(
    interval_1: Interval[PointType], interval_2: Interval[PointType]
) -> bool:
    return not (
        interval_1.lower in interval_2
        or interval_1.upper in interval_2
        or interval_2.lower in interval_1
        or interval_2.upper in interval_1
    )
