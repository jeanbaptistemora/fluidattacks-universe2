from __future__ import (
    annotations,
)

from more_itertools import (
    windowed,
)
from returns.primitives.container import (
    BaseContainer,
)
from returns.primitives.hkt import (
    SupportsKind1,
)
from singer_io.common import (
    JSON,
)
from tap_gitlab.intervals.interval import (
    IntervalPoint,
    MAX,
    MIN,
    OpenLeftInterval,
)
from tap_gitlab.intervals.progress import (
    ProgressInterval,
)
from typing import (
    final,
    Optional,
    Tuple,
    TypeVar,
)

_Point = TypeVar("_Point")


class InvalidEndpoints(Exception):
    pass


@final
class FragmentedInterval(
    BaseContainer,
    SupportsKind1["FragmentedInterval", _Point],
):
    def __init__(
        self,
        endpoints: Tuple[IntervalPoint[_Point], ...],
        emptiness: Tuple[bool, ...],
    ) -> None:
        super().__init__(
            {
                "endpoints": endpoints,
                "emptiness": emptiness,
            }
        )

    @property
    def endpoints(self) -> Tuple[IntervalPoint[_Point], ...]:
        return self._inner_value["endpoints"]

    @property
    def emptiness(self) -> Tuple[bool, ...]:
        return self._inner_value["emptiness"]

    @property
    def intervals(self) -> Tuple[OpenLeftInterval[_Point], ...]:
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
                return OpenLeftInterval(p_1, p_2)
            raise InvalidEndpoints()

        return tuple(
            _new_interval(p_1, p_2) for p_1, p_2 in windowed(self.endpoints, 2)
        )

    @property
    def progress_intervals(
        self,
    ) -> Tuple[ProgressInterval[_Point], ...]:
        intervals = zip(self.intervals, self.emptiness)
        return tuple(
            ProgressInterval(item, not empty) for item, empty in intervals
        )

    def to_json(self) -> JSON:
        return {
            "type": "FragmentedInterval",
            "obj": {
                "endpoints": self.endpoints,
                "emptiness": self.emptiness,
            },
        }
