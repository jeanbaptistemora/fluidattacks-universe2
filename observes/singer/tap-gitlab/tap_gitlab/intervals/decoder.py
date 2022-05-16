from dataclasses import (
    dataclass,
)
from returns.primitives.hkt import (
    SupportsKind1,
)
from singer_io import (
    JSON,
)
from tap_gitlab.intervals.alias import (
    NTuple,
)
from tap_gitlab.intervals.fragmented import (
    FIntervalFactory,
    FragmentedInterval,
)
from tap_gitlab.intervals.interval import (
    IntervalPoint,
    MAX,
    MIN,
)
from tap_gitlab.intervals.patch import (
    Patch,
)
from tap_gitlab.intervals.progress import (
    FProgressFactory,
    FragmentedProgressInterval,
)
from typing import (
    Callable,
    List,
    TypeVar,
)

_Point = TypeVar("_Point")


class DecodeError(Exception):
    pass


@dataclass(frozen=True)
class IntervalDecoder(
    SupportsKind1["IntervalDecoder", _Point],
):
    factory: FIntervalFactory[_Point]
    p_factory: FProgressFactory[_Point]
    decode_point: Patch[Callable[[JSON], _Point]]

    def decode_ipoint(self, raw: JSON) -> IntervalPoint[_Point]:
        if raw["type"] == "IntervalPoint":
            raw_point = raw["obj"]["point"]
            point: IntervalPoint[_Point]
            if raw_point == "MIN":
                point = MIN()
            elif raw_point == "MAX":
                point = MAX()
            else:
                point = self.decode_point.unwrap(raw_point)
            return point
        raise DecodeError()

    def decode_f_interval(self, raw: JSON) -> FragmentedInterval[_Point]:
        if raw["type"] == "FragmentedInterval":
            raw_points = raw["obj"]["endpoints"]
            endpoints: NTuple[IntervalPoint[_Point]] = tuple(
                self.decode_ipoint(raw_point) for raw_point in raw_points
            )
            return self.factory.from_endpoints(endpoints)
        raise DecodeError()

    def decode_f_progress(
        self, raw: JSON
    ) -> FragmentedProgressInterval[_Point]:
        if raw["type"] == "FragmentedProgressInterval":
            raw_f_interval = raw["obj"]["f_interval"]
            f_interval = self.decode_f_interval(raw_f_interval)
            raw_completeness = raw["obj"]["completeness"]
            completeness: List[bool] = []
            for item in raw_completeness:
                if item is True or item is False:
                    completeness.append(item)
                else:
                    raise DecodeError("Expected NTuple[bool]")
            return self.p_factory.new_fprogress(
                f_interval, tuple(completeness)
            )
        raise DecodeError()
