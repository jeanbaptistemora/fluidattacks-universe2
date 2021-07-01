from __future__ import (
    annotations,
)

from dataclasses import (
    dataclass,
)
from more_itertools import (
    windowed,
)
from tap_gitlab.intervals.alias import (
    NTuple,
)
from tap_gitlab.intervals.interval import (
    IntervalFactory,
    IntervalPoint,
    InvalidInterval,
    MAX,
    MIN,
    OpenLeftInterval,
)
from typing import (
    final,
    Generic,
    Optional,
    TypeVar,
)

_Point = TypeVar("_Point")


class InvalidEndpoints(Exception):
    pass


def _to_endpoints(
    intervals: NTuple[OpenLeftInterval[_Point]],
) -> NTuple[IntervalPoint[_Point]]:
    endpoints: NTuple[IntervalPoint[_Point]] = tuple()
    if not intervals:
        raise InvalidInterval("Empty intervals")
    for interval in intervals:
        if not endpoints:
            endpoints = endpoints + (interval.lower, interval.upper)
        else:
            if endpoints[-1] == interval.lower:
                endpoints = endpoints + (interval.upper,)
            else:
                raise InvalidInterval(
                    f"discontinuous: {endpoints[-1]} + {interval}"
                )
    return endpoints


def _to_intervals(
    factory: IntervalFactory[_Point], endpoints: NTuple[IntervalPoint[_Point]]
) -> NTuple[OpenLeftInterval[_Point]]:
    def _new_interval(
        p_1: Optional[IntervalPoint[_Point]],
        p_2: Optional[IntervalPoint[_Point]],
    ) -> OpenLeftInterval[_Point]:
        if (
            p_1
            and p_2
            and not isinstance(p_1, MAX)
            and not isinstance(p_2, (MIN, MAX))
        ):
            return factory.new_lopen(p_1, p_2)
        raise InvalidEndpoints()

    return tuple(
        _new_interval(p_1, p_2) for p_1, p_2 in windowed(endpoints, 2)
    )


@dataclass(frozen=True)
class _FragmentedInterval(Generic[_Point]):
    endpoints: NTuple[IntervalPoint[_Point]]
    intervals: NTuple[OpenLeftInterval[_Point]]


@final
@dataclass(frozen=True)
class FragmentedInterval(Generic[_Point]):
    endpoints: NTuple[IntervalPoint[_Point]]
    intervals: NTuple[OpenLeftInterval[_Point]]

    def __init__(self, obj: _FragmentedInterval[_Point]) -> None:
        for key, value in obj.__dict__.items():
            object.__setattr__(self, key, value)


@final
@dataclass(frozen=True)
class FIntervalFactory(Generic[_Point]):
    factory: IntervalFactory[_Point]

    def from_endpoints(
        self, endpoints: NTuple[IntervalPoint[_Point]]
    ) -> FragmentedInterval[_Point]:
        draft = _FragmentedInterval(
            endpoints, _to_intervals(self.factory, endpoints)
        )
        return FragmentedInterval(draft)

    # pylint: disable=no-self-use
    def from_intervals(
        self, intervals: NTuple[OpenLeftInterval[_Point]]
    ) -> FragmentedInterval[_Point]:
        endpoints = _to_endpoints(intervals)
        draft = _FragmentedInterval(endpoints, intervals)
        return FragmentedInterval(draft)

    def append_to(
        self, f_interval: FragmentedInterval[_Point], point: _Point
    ) -> FragmentedInterval[_Point]:
        return self.from_endpoints(f_interval.endpoints + (point,))
