from __future__ import (
    annotations,
)

from returns.primitives.container import (
    BaseContainer,
)
from returns.primitives.hkt import (
    SupportsKind1,
    SupportsKind2,
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
    Callable,
    final,
    Tuple,
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


_State = TypeVar("_State")


@final
class ProcessStatus(
    BaseContainer,
    SupportsKind2["ProcessStatus", _DataType, _State],
):
    def __init__(
        self,
        p_intervals: NTuple[ProgressInterval[_DataType]],
        incomplete_is_present: bool,
        function_state: _State,
    ) -> None:
        super().__init__(
            {
                "p_intervals": p_intervals,
                "incomplete_is_present": incomplete_is_present,
                "function_state": function_state,
            }
        )

    @property
    def p_intervals(self) -> NTuple[ProgressInterval[_DataType]]:
        return self._inner_value["p_intervals"]

    @property
    def incomplete_is_present(self) -> bool:
        return self._inner_value["incomplete_is_present"]

    @property
    def function_state(self) -> _State:
        return self._inner_value["function_state"]


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

    def process_until_incomplete(
        self,
        function: Callable[
            [_State, ProgressInterval[_DataType]],
            Tuple[_State, NTuple[ProgressInterval[_DataType]]],
        ],
        init_state: _State,
    ) -> NTuple[ProgressInterval[_DataType]]:
        def _process(
            prev: ProcessStatus[_DataType, _State],
            interval: ProgressInterval[_DataType],
        ) -> ProcessStatus[_DataType, _State]:
            if prev.incomplete_is_present:
                return ProcessStatus(
                    prev.p_intervals + (interval,),
                    prev.incomplete_is_present,
                    prev.function_state,
                )
            state, results = function(prev.function_state, interval)
            incomplete = tuple(
                filter(lambda p_invl: p_invl.completed is False, results)
            )
            return ProcessStatus(
                prev.p_intervals + results, bool(incomplete), state
            )

        status: ProcessStatus[_DataType, _State] = ProcessStatus(
            tuple(), False, init_state
        )
        for interval in self.progress_intervals:
            status = _process(status, interval)
        return status.p_intervals

    def to_json(self) -> JSON:
        return {
            "type": "FragmentedProgressInterval",
            "obj": {
                "f_interval": self.f_interval.to_json(),
                "completeness": self.completeness,
            },
        }
