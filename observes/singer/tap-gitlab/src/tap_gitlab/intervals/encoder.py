from dataclasses import (
    dataclass,
)
from returns.primitives.hkt import (
    SupportsKind1,
)
from singer_io import (
    JSON,
)
from tap_gitlab.intervals.fragmented import (
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
    FragmentedProgressInterval,
)
from typing import (
    Callable,
    TypeVar,
)

_Point = TypeVar("_Point")


@dataclass(frozen=True)
class IntervalEncoder(
    SupportsKind1["IntervalEncoder", _Point],
):
    _encode_point: Patch[Callable[[_Point], JSON]]

    def __init__(
        self,
        encode_point: Callable[[_Point], JSON],
    ) -> None:
        object.__setattr__(self, "_encode_point", Patch(encode_point))

    def encode_point(self, point: _Point) -> JSON:
        return self._encode_point.unwrap(point)

    def encode_ipoint(self, point: IntervalPoint[_Point]) -> JSON:
        encoded = (
            str(point)
            if isinstance(point, (MAX, MIN))
            else self.encode_point(point)
        )
        return {
            "type": "IntervalPoint",
            "obj": {
                "point": encoded,
            },
        }

    def encode_f_interval(self, interval: FragmentedInterval[_Point]) -> JSON:
        return {
            "type": "FragmentedInterval",
            "obj": {
                "endpoints": tuple(
                    self.encode_ipoint(point) for point in interval.endpoints
                ),
            },
        }

    def encode_f_progress(
        self, interval: FragmentedProgressInterval[_Point]
    ) -> JSON:
        return {
            "type": "FragmentedProgressInterval",
            "obj": {
                "f_interval": self.encode_f_interval(interval.f_interval),
                "completeness": interval.completeness,
            },
        }
