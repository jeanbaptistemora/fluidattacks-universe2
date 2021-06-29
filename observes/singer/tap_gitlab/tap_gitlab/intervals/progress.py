from __future__ import (
    annotations,
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
from tap_gitlab.intervals.fragmented import (
    FragmentedInterval,
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


@final
class FragmentedProgressInterval(
    BaseContainer,
    SupportsKind1["FragmentedProgressInterval", _DataType],
):
    def __init__(
        self,
        f_interval: FragmentedInterval[_DataType],
        completeness: NTuple[bool],
    ) -> None:
        super().__init__(
            {
                "f_interval": f_interval,
                "completeness": completeness,
            }
        )

    @property
    def f_interval(self) -> FragmentedInterval[_DataType]:
        return self._inner_value["f_interval"]

    @property
    def completeness(self) -> NTuple[bool]:
        return self._inner_value["completeness"]

    @property
    def progress_intervals(
        self,
    ) -> NTuple[ProgressInterval[_DataType]]:
        intervals = zip(self.f_interval.intervals, self.completeness)
        return tuple(
            ProgressInterval(item, completed) for item, completed in intervals
        )

    def to_json(self) -> JSON:
        return {
            "type": "FragmentedProgressInterval",
            "obj": {
                "f_interval": self.f_interval.to_json(),
                "completeness": self.completeness,
            },
        }
