from __future__ import (
    annotations,
)

from returns.primitives.container import (
    BaseContainer,
)
from returns.primitives.hkt import (
    SupportsKind1,
)
from tap_gitlab.intervals.alias import (
    NTuple,
)
from tap_gitlab.intervals.interval import (
    IntervalFactory,
    IntervalPoint,
    InvalidInterval,
    OpenLeftInterval,
)
from typing import (
    final,
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


@final
class FragmentedInterval(
    BaseContainer,
    SupportsKind1["FragmentedInterval", _Point],
):
    def __init__(
        self,
        intvl_factory: IntervalFactory,
        intervals: NTuple[OpenLeftInterval[_Point]],
    ) -> None:
        endpoints = _to_endpoints(intervals)
        super().__init__(
            {
                "endpoints": endpoints,
                "intervals": intervals,
                "intvl_factory": intvl_factory,
            }
        )

    @property
    def factory(self) -> IntervalFactory:
        return self._inner_value["intvl_factory"]

    @property
    def endpoints(self) -> NTuple[IntervalPoint[_Point]]:
        return self._inner_value["endpoints"]

    @property
    def intervals(self) -> NTuple[OpenLeftInterval[_Point]]:
        return self._inner_value["intervals"]
