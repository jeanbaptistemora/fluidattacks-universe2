from returns.primitives.container import (
    BaseContainer,
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
from tap_gitlab.intervals.progress import (
    FragmentedProgressInterval,
)
from typing import (
    Callable,
    final,
    TypeVar,
)

_Point = TypeVar("_Point")


@final
class IntervalEncoder(
    BaseContainer,
    SupportsKind1["IntervalEncoder", _Point],
):
    def __init__(
        self,
        encode_point: Callable[[_Point], JSON],
    ) -> None:
        super().__init__(
            {
                "encode_point": encode_point,
            }
        )

    def encode_point(self, point: _Point) -> JSON:
        return self._inner_value["encode_point"](point)

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
