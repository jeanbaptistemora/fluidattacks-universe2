from __future__ import (
    annotations,
)

from returns.primitives.container import (
    BaseContainer,
)
from returns.primitives.hkt import (
    SupportsKind1,
)
from tap_gitlab.intervals.interval import (
    Interval,
)
from typing import (
    final,
    TypeVar,
)

_DataType = TypeVar("_DataType")


@final
class ProgressInterval(
    BaseContainer,
    SupportsKind1["ProgressInterval", _DataType],
):
    def __init__(self, interval: Interval[_DataType], completed: bool) -> None:
        super().__init__(
            {
                "interval": interval,
                "completed": completed,
            }
        )

    @property
    def interval(self) -> Interval[_DataType]:
        return self._inner_value["interval"]

    @property
    def completed(self) -> bool:
        return self._inner_value["completed"]
