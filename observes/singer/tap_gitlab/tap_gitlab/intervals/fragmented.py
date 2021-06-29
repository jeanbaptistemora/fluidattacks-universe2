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
from tap_gitlab.intervals.alias import (
    NTuple,
)
from tap_gitlab.intervals.interval import (
    IntervalPoint,
    MAX,
    MIN,
    OpenLeftInterval,
)
from typing import (
    final,
    Optional,
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
        endpoints: NTuple[IntervalPoint[_Point]],
    ) -> None:
        super().__init__(
            {
                "endpoints": endpoints,
            }
        )

    @property
    def endpoints(self) -> NTuple[IntervalPoint[_Point]]:
        return self._inner_value["endpoints"]

    @property
    def intervals(self) -> NTuple[OpenLeftInterval[_Point]]:
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

    def to_json(self) -> JSON:
        return {
            "type": "FragmentedInterval",
            "obj": {
                "endpoints": self.endpoints,
            },
        }
